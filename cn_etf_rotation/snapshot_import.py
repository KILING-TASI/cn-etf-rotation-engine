# SPDX-License-Identifier: MIT
"""Frozen daily archive to an explicit ETF pool, with no data-repo import."""
import argparse,hashlib,json,math,sys
from datetime import date,datetime
from decimal import Decimal
from pathlib import Path
from .review import validate


def build(spec):
    if not isinstance(spec,dict):raise ValueError('冻结快照组合输入须为对象')
    if spec.get('inputSchema')!='etf-frozen-pool/1':raise ValueError('需etf-frozen-pool/1')
    if spec.get('sampleType') not in {'teaching','declared-archive'}:raise ValueError('须声明教学或使用者已有归档')
    asof=date.fromisoformat(spec['asOf']);items=spec['instruments']
    if not isinstance(items,list) or not 2<=len(items)<=100:raise ValueError('需2至100个明确ETF快照')
    dates=None;rows=[];bindings=[]
    for item in items:
        if not isinstance(item,dict) or not isinstance(item.get('snapshot'),dict) or not isinstance(item.get('rawResponseText'),str):raise ValueError('每项需要快照对象与原始JSON响应文字')
        snap=item['snapshot'];raw=item['rawResponseText'].encode('utf-8')
        if len(raw)>16*1024*1024:raise ValueError('冻结原响应超过16MiB')
        if snap.get('schemaVersion')!='cn-market-daily-archive/1.0' or snap.get('status')!='success':raise ValueError('失败或其他格式快照不能用于排名')
        if snap.get('rawSha256')!=hashlib.sha256(raw).hexdigest():raise ValueError('冻结原响应摘要不符')
        request=snap['request']
        if request['kind']!='etf' or request['market'] not in {'SSE','SZSE'}:raise ValueError('需明确沪深ETF身份')
        if snap.get('priceBasis')!='unadjusted' or item.get('comparability')!='declared-no-distribution-or-split' or not isinstance(item.get('eventEvidence'),str) or not item['eventEvidence'].strip():raise ValueError('未复权价格需明确事件核查声明，不猜复权或无分红')
        acquired=datetime.fromisoformat(snap['retrievedAt'])
        if acquired.tzinfo is None:raise ValueError('原取得时间缺时区')
        from .__main__ import pairs
        obj=json.loads(raw.decode('utf-8-sig'),object_pairs_hook=pairs)
        data=obj.get('data')
        if not isinstance(data,dict) or data.get('code')!=request['code'] or str(data.get('market'))!=('1' if request['market']=='SSE' else '0'):raise ValueError('原响应证券身份不同')
        observed=snap['data'];lines=data['klines']
        if len(observed)!=len(lines):raise ValueError('冻结快照行数与原响应不同')
        ds=[];closes=[]
        for row,line in zip(observed,lines):
            parts=line.split(',')
            if len(parts)!=7 or row['date']!=parts[0] or Decimal(row['close'])!=Decimal(parts[2]):raise ValueError('原响应日期或价格与快照不同')
            day=date.fromisoformat(row['date'])
            if day>asof or day>acquired.date():raise ValueError('日期晚于截止或取得时点')
            price=float(row['close'])
            if not math.isfinite(price) or price<=0:raise ValueError('价格须正有限数值')
            ds.append(row['date']);closes.append(price)
        if dates is None:dates=ds
        elif dates!=ds:raise ValueError('ETF日历不一致；不取交集、补齐或缩短窗口')
        if not isinstance(item.get('indexId'),str) or not item['indexId'].strip() or item.get('category')!='industry':raise ValueError('需明确行业指数身份与category=industry；不把其他ETF默认为行业ETF')
        rows.append(dict(symbol=request['code'],index=item['indexId'],market=request['market'],type='industry',eligible=True,closes=closes))
        bindings.append(dict(symbol=request['code'],sourceUrl=snap['sourceUrl'],rawSha256=snap['rawSha256'],retrievedAt=snap['retrievedAt'],historicalAvailability='unknown',comparability=item['comparability'],eventEvidence=item['eventEvidence']))
    result=dict(asOf=spec['asOf'],dates=dates,rows=rows,origin='teaching' if spec['sampleType']=='teaching' else 'declared-history',currency='CNY',priceBasis='provided-price')
    validate(result)
    return {'engineInput':result,'bindings':bindings,'methodVersion':'frozen-daily-to-etf-pool/1','limitations':['原响应摘要、日期和价格一致，不认证来源真实性、指数类别或事件完整性','未复权价格只接受使用者明确可比声明，不认证成总收益','全部日历必须一致，不用交集掩盖缺日；交易日历与历史可得时点仍未知']}


def main(argv=None):
    from .__main__ import pairs
    p=argparse.ArgumentParser(description='冻结行情快照转ETF观察池，不联网，不依赖其他作者仓库')
    p.add_argument('--input',type=Path,required=True);p.add_argument('--out-dir',type=Path,required=True);a=p.parse_args(argv)
    try:
        if a.out_dir.exists():raise ValueError('输出已存在，历史结果不覆盖')
        if not a.input.is_file() or a.input.is_symlink() or a.input.stat().st_size>32*1024*1024:raise ValueError('需要不超过32MiB的普通JSON组合输入')
        spec=json.loads(a.input.read_text('utf-8-sig'),object_pairs_hook=pairs);result=build(spec);a.out_dir.mkdir(parents=True)
        for name,obj in [('input.json',spec),('result.json',result),('engine-input.json',result['engineInput'])]:(a.out_dir/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),'utf-8')
        print('已保存ETF观察池：'+str(a.out_dir/'engine-input.json'));return 0
    except (ValueError,KeyError,TypeError,OSError) as exc:print('未完成：'+str(exc),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
