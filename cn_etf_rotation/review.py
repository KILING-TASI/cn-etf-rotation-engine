# SPDX-License-Identifier: MIT
import datetime as dt
import math
from .rotation import rank, exposure, may_replace, CONFIG, valid_prices

def validate(spec):
    if not isinstance(spec,dict) or set(spec)-{'asOf','dates','rows','marketCloses','origin','rebalanceEvery','costBps','topN'}:raise ValueError('输入字段不支持')
    cutoff=dt.date.fromisoformat(spec['asOf']);dates=spec['dates'];rows=spec['rows']
    if not isinstance(dates,list) or not 26<=len(dates)<=5000:raise ValueError('需要26至5000个共同日期')
    if dates!=sorted(set(dates)) or any(dt.date.fromisoformat(d)>cutoff for d in dates):raise ValueError('日期重复、乱序或晚于截止')
    if not isinstance(rows,list) or not 2<=len(rows)<=500:raise ValueError('需要2至500个已声明观察对象')
    for row in rows:
        if not isinstance(row,dict) or not isinstance(row.get('symbol'),str) or not isinstance(row.get('index'),str) or not row['symbol'] or not row['index']:raise ValueError('需明确ETF与指数身份')
        if not isinstance(row.get('closes'),list) or len(row['closes'])!=len(dates) or not valid_prices(row['closes'],len(dates)):raise ValueError('全部价格需同一日历正有限值；不填补缺项')
    if len({r['symbol'] for r in rows})!=len(rows) or len({r['index'] for r in rows})!=len(rows):raise ValueError('ETF或指数映射重复')
    market=spec.get('marketCloses',[])
    if market and (len(market)!=len(dates) or not valid_prices(market,len(dates))):raise ValueError('市场价格日历不一致')
    if spec.get('origin') not in ('teaching','declared-history'):raise ValueError('来源须为teaching或declared-history；不是历史池认证')
    return spec

def calculate(spec):
    d=validate(spec);ranked=rank(d['rows']);market=exposure(d.get('marketCloses',[]))
    return {'methodVersion':'etf-rotation-legacy-20d/1','asOf':d['asOf'],'ranking':ranked,'marketExposure':market,'config':CONFIG,
            'limitations':['排名是声明观察池20个区间相对动量，不是全市场择优或未来收益预测','市场风险档位是旧研究规则，不是组合优化','价格复权与指数身份依赖提供资料，未自动认证']}

def backtest(spec):
    d=validate(spec);rows=d['rows'];dates=d['dates'];n=d.get('topN',2);every=d.get('rebalanceEvery',5);cost=d.get('costBps',10)
    if type(n) is not int or not 1<=n<=len(rows) or type(every) is not int or not 1<=every<=60:raise ValueError('持有数量或调仓间隔不符')
    if isinstance(cost,bool) or not isinstance(cost,(int,float)) or not math.isfinite(cost) or not 0<=cost<=1000:raise ValueError('成本须为0至1000基点')
    weights={};entered={};pending=None;wealth=1.;path=[];trades=[];peak=1.;maxdd=0.
    for t in range(25,len(dates)):
        # Signal at t-1 close executes at t close. The t-1->t return uses old weights.
        gross=sum(w*(next(r for r in rows if r['symbol']==symbol)['closes'][t]/next(r for r in rows if r['symbol']==symbol)['closes'][t-1]-1) for symbol,w in weights.items())
        wealth*=1+gross
        # Drift risky weights; cash has zero return. Do not silently rebalance daily.
        if weights:
            weights={symbol:w*(next(r for r in rows if r['symbol']==symbol)['closes'][t]/next(r for r in rows if r['symbol']==symbol)['closes'][t-1])/(1+gross) for symbol,w in weights.items()}
        if pending is not None:
            proposed,signal_date=pending;turnover=sum(abs(proposed.get(s,0)-weights.get(s,0)) for s in set(proposed)|set(weights))
            wealth*=1-turnover*cost/10000
            for symbol in proposed:
                if symbol not in weights:entered[symbol]=t
            entered={s:entered[s] for s in proposed};weights=proposed
            trades.append({'signalDate':signal_date,'executionDate':dates[t],'turnover':turnover,'costBps':cost,'weights':dict(weights)})
            pending=None
        peak=max(peak,wealth);maxdd=max(maxdd,1-wealth/peak);path.append({'date':dates[t],'wealthIndex':wealth,'cashWeight':1-sum(weights.values())})
        if (t-25)%every==0 and t+1<len(dates):
            ranked=rank([dict(r,closes=r['closes'][:t+1]) for r in rows]);rank_by={r['symbol']:r['rank01'] for r in ranked}
            if not ranked:continue
            chosen=list(weights)
            if not chosen:chosen=[r['symbol'] for r in ranked[:n]]
            else:
                candidate=next((r for r in ranked if r['symbol'] not in chosen),None)
                holding=min(chosen,key=lambda s:rank_by.get(s,-1))
                if candidate and may_replace(holdingRank=rank_by[holding],candidateRank=candidate['rank01'],heldTradingDays=t-entered[holding],isRebalance=True):chosen=[candidate['symbol'] if s==holding else s for s in chosen]
            risk=exposure(d.get('marketCloses',[])[:t+1]);target=risk['target'] if risk['ready'] else 1
            pending=({s:target/len(chosen) for s in chosen},dates[t])
    return {'methodVersion':'etf-fixed-pool-next-close-scenario/1','asOf':d['asOf'],'path':path,'trades':trades,'totalReturn':wealth-1,'maxDrawdown':maxdd,
            'parameters':{'topN':n,'rebalanceEvery':every,'costBps':cost,'execution':'next_observed_close'},
            'limitations':['固定声明池历史情景，未取得历史成分或退市全集，不宣称无幸存者偏差','信号只用当时及以前价格，下一观察日收盘执行；不是下一开盘成交','成本是统一假设，不含真实交易税费、滑点和流动性','未提供市场价格时不应用市场风险档位；不推定完整交易日历']}
