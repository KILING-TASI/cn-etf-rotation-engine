# SPDX-License-Identifier: MIT
import argparse,datetime as dt,hashlib,json,sys,tempfile,os,shutil
from html import escape
from pathlib import Path
from .review import calculate,backtest

def pairs(items):
    out={}
    for k,v in items:
        if k in out:raise ValueError('重复JSON字段')
        out[k]=v
    return out

def teaching():
    dates=[(dt.date(2026,1,5)+dt.timedelta(days=i)).isoformat() for i in range(60)]
    return dict(asOf=dates[-1],dates=dates,origin='teaching',rows=[dict(symbol='90000'+str(i+1),index='teaching-'+str(i),type='industry',eligible=True,closes=[100*(1+(i+1)*.0005)**t for t in range(60)]) for i in range(3)],marketCloses=[100*(1.0003)**t for t in range(60)],costBps=10,topN=2)

def publish(spec,result,out):
    if out.exists():raise ValueError('输出目录已存在；不覆盖历史结果')
    out.parent.mkdir(parents=True,exist_ok=True);stage=Path(tempfile.mkdtemp(prefix='.'+out.name+'-',dir=out.parent))
    try:
        for name,obj in [('input.json',spec),('result.json',result)]:
            (stage/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
        rows=''.join('<li>'+escape(r['symbol'])+'：历史动量 '+str(round(r['momentum']*100,3))+'%；相对位置 '+str(r['rank01'])+'</li>' for r in result.get('ranking',[]))
        gaps=''.join('<li>'+escape(s)+'</li>' for s in result['limitations'])
        stats='<p>固定池历史情景收益：'+str(round(result['totalReturn']*100,3))+'%；最大回撤：'+str(round(result['maxDrawdown']*100,3))+'%。不是实际账户收益或未来预测。</p>' if 'path' in result else ''
        (stage/'打开这里.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ETF轮动研究</title><style>body{max-width:1000px;margin:32px auto;padding:0 20px;font:17px/1.7 system-ui}</style><h1>这个观察池的相对表现怎样？</h1><p>资料类型：'+escape(spec['origin'])+'；研究截止：'+escape(spec['asOf'])+'。教学为原创虚构价格和日期，不是真实交易日历。</p><ul>'+rows+'</ul>'+stats+'<h2>结果的范围</h2><ul>'+gaps+'</ul><h2>下一步</h2><p>换成明确指数身份、共同交易日历和核对复权口径的历史资料；每次使用新目录。查看input.json与result.json复查参数和方法版本。</p></html>',encoding='utf-8')
        hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in stage.iterdir()}
        (stage/'receipt.json').write_text(json.dumps({'files':hashes,'scope':'文件完整性，不是来源认证'},ensure_ascii=False,indent=2),encoding='utf-8')
        os.rename(stage,out)
    finally:
        if stage.exists():shutil.rmtree(stage)

def main(argv=None):
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description='独立ETF相对强弱、轮动规则与固定池历史情景，不联网、不交易')
    p.add_argument('command',choices=['demo','review','backtest']);p.add_argument('--input',type=Path);p.add_argument('--out-dir',type=Path,required=True);a=p.parse_args(argv)
    try:
        if a.out_dir.exists():raise ValueError('输出目录已存在')
        if a.command=='demo':spec=teaching()
        else:
            if a.input is None or a.input.is_symlink() or a.input.stat().st_size>16*1024*1024:raise ValueError('需要不超过16MiB的普通JSON输入')
            spec=json.loads(a.input.read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('非有限JSON常量')))
        result=backtest(spec) if a.command=='backtest' else calculate(spec)
        publish(spec,result,a.out_dir);print('结果入口：'+str(a.out_dir/'打开这里.html'));return 0
    except (ValueError,OSError,KeyError,TypeError) as exc:print('未完成：'+str(exc)+'。下一步核对共同日历、身份和新目录。',file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
