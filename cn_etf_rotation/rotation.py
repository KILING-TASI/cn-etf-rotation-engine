# SPDX-License-Identifier: MIT
"""The historical ETF rotation rules, moved to an independently installable module."""
import math
import statistics

CONFIG={'lookback':20,'rebalanceDays':5,'minHoldDays':9,'rankGap':.10,'maxSwaps':1}

def valid_prices(prices,n):
    return isinstance(prices,list) and len(prices)>=n and all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) and x>0 for x in prices[-n:])

def rank(rows):
    valid=[r for r in rows if r.get('eligible') is True and r.get('type')=='industry' and r.get('symbol') and r.get('index') and valid_prices(r.get('closes'),21)]
    if len({r['index'] for r in valid})!=len(valid) or len({r['symbol'] for r in valid})!=len(valid):raise ValueError('重复ETF或指数映射')
    out=[{'symbol':r['symbol'],'momentum':r['closes'][-1]/r['closes'][-21]-1} for r in valid]
    if len(out)<2:return []
    for row in out:
        less=sum(x['momentum']<row['momentum'] for x in out);equal=sum(x['momentum']==row['momentum'] for x in out)
        row['rank01']=(less+(equal-1)/2)/(len(out)-1)
    return sorted(out,key=lambda x:(-x['rank01'],x['symbol']))

def exposure(closes):
    if not valid_prices(closes,26):return {'ready':False,'volatility':None,'target':None}
    def vol(end):
        p=closes[end-21:end];returns=[b/a-1 for a,b in zip(p,p[1:])]
        return math.sqrt(statistics.variance(returns))*math.sqrt(252)*100
    value=(vol(len(closes))+vol(len(closes)-5))/2
    return {'ready':True,'volatility':value,'target':.1 if value>=40 else .4 if value>=30 else .7 if value>=25 else 1,'effective':'next_trading_day'}

def may_replace(*,holdingRank,candidateRank,heldTradingDays,isRebalance,swaps=0):
    return isRebalance is True and type(swaps) is int and 0<=swaps<CONFIG['maxSwaps'] and type(heldTradingDays) is int and heldTradingDays>=CONFIG['minHoldDays'] and all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) and 0<=x<=1 for x in (holdingRank,candidateRank)) and candidateRank-holdingRank>=CONFIG['rankGap']-1e-12
