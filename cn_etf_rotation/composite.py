# SPDX-License-Identifier: MIT
"""Explicit legacy composite score, using the canonical original JS method."""
import hashlib,json,shutil,subprocess
from pathlib import Path

METHOD='legacy-four-dimension-js/1'

def calculate(spec):
    if not isinstance(spec,dict):raise ValueError('综合评分输入须为对象')
    if spec.get('inputSchema')!='etf-composite/1':raise ValueError('需etf-composite/1输入')
    if spec.get('sampleType') not in {'teaching','declared-snapshot'}:raise ValueError('需明确教学或使用者声明快照')
    from datetime import date
    asof=spec['asOf'];parsed=date.fromisoformat(asof)
    if parsed.isoformat()!=asof:raise ValueError('截止日期须YYYY-MM-DD')
    snapshot=spec['snapshot']
    if not isinstance(snapshot,dict):raise ValueError('快照须为对象')
    if snapshot.get('date')!=asof:raise ValueError('快照日期与截止日不一致')
    if not isinstance(snapshot.get('sectors'),list) or not 1<=len(snapshot['sectors'])<=200:raise ValueError('需1至200个板块')
    ids=[r['id'] for r in snapshot['sectors']]
    if len(set(ids))!=len(ids):raise ValueError('板块身份重复')
    selected=spec.get('selected',[])
    if not isinstance(selected,list) or len(set(selected))!=len(selected) or any(x not in ids for x in selected):raise ValueError('选择板块无效或重复')
    # This preserves the old top-three behavior instead of silently ignoring selection order.
    if len(selected)>3:raise ValueError('明确最多选择3个板块，避免旧接口隐式截断')
    node=shutil.which('node')
    if not node:raise ValueError('综合评分需Node.js；基础动量review不需要它，不自动安装或切回旧工作台')
    engine=Path(__file__).parent/'legacy/engine.js'
    runner=Path(__file__).parent/'composite_runner.js'
    raw=json.dumps(spec,ensure_ascii=False,allow_nan=False).encode('utf-8')
    if len(raw)>16*1024*1024:raise ValueError('输入超过16MiB')
    p=subprocess.run([node,str(runner)],input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,check=False)
    if p.returncode:raise ValueError('综合评分失败：'+p.stderr.decode('utf-8','replace')[:1000])
    result=json.loads(p.stdout)
    result.update(methodVersion=METHOD,methodSha256=hashlib.sha256(engine.read_bytes()).hexdigest(),asOf=asof,
        conclusion=('原创教学数据，不是真实行情。' if spec['sampleType']=='teaching' else '')+'按输入观察池和四维权重复现历史研究评分；分值不是收益预测，也不自动生成交易指令。',
        limitations=['沿用原研究评分，不声称策略有效性或全市场排名','事件核验标记由资料提供者填写，程序未独立核实原文','空事件清单在旧规则中对应中性50分，不证明没有相关消息或已完成检索','代理和原始指标不混池；陈旧、缺值板块不排名；缺北向指标保持原说明','实际数据刷新由数据来源入口负责，本入口只计算明确快照','Node.js仅为综合评分可选依赖，基础Python动量入口独立可用'],humanRows=[[r['name'],'数据不足' if r['total'] is None else round(r['total'],3)] for r in result['ranking']])
    return result

def main():
    import argparse,sys
    from .__main__ import pairs
    from html import escape
    p=argparse.ArgumentParser(description='明确快照的四维综合评分，保留原研究算法')
    p.add_argument('--input',type=Path,required=True);p.add_argument('--out-dir',type=Path,required=True);a=p.parse_args()
    try:
        if a.out_dir.exists():raise ValueError('输出已存在，历史结果不覆盖')
        if not a.input.is_file() or a.input.is_symlink() or a.input.stat().st_size>16*1024*1024:raise ValueError('需不超过16MiB的普通JSON输入')
        spec=json.loads(a.input.read_text('utf-8-sig'),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('非有限JSON')))
        r=calculate(spec);a.out_dir.mkdir(parents=True)
        for name,obj in [('input.json',spec),('result.json',r)]:
            (a.out_dir/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),'utf-8')
        engine=(Path(__file__).parent/'legacy/engine.js').read_text('utf-8')
        embedded=json.dumps(spec,ensure_ascii=False,allow_nan=False).replace('<',r'\u003c')
        page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ETF综合观察</title><style>body{max-width:960px;margin:30px auto;padding:0 18px;font:17px/1.7 system-ui}td,th{padding:8px;border-bottom:1px solid #ddd}table{width:100%}button,select{font:inherit}#table{overflow:auto}</style><h1>这个观察池值得继续研究哪些板块？</h1><p>分值反映输入指标和研究权重；不是收益预测。</p><p>切换为临时情景：<select id="preset"><option value="frozen">本次冻结权重</option><option value="equal">等权</option><option value="recovery">复苏</option><option value="overheat">过热</option><option value="stagflation">滞胀</option><option value="recession">衰退</option></select> <button id="save">另存情景参数</button></p><p id="status"></p><div id="table"></div><h2>依据与缺口</h2><ul>'''+''.join('<li>'+escape(x)+'</li>' for x in r['limitations'])+'''</ul><p>原始冻结结果保存在 result.json；网页切换不覆盖它。参数下载后用CLI另存新报告。</p><script>'''+engine+'\nconst spec='+embedded+''';let weights=spec.weights;const p=document.getElementById('preset');function draw(){const rows=ETFEngine.calculate(spec.snapshot,weights,spec.asOf);document.getElementById('status').textContent='权重：'+weights.join(' / ')+'；截止 '+spec.asOf+'；'+(p.value==='frozen'?'本次冻结参数':'临时情景，原报告保持不变');const table=document.createElement('table');for(const row of [['板块','综合分','资料状态'],...rows.map(r=>[r.name,r.total===null?'未知':r.total.toFixed(3),r.modelStatus])]){const tr=document.createElement('tr');for(const text of row){const td=document.createElement('td');td.textContent=text;tr.appendChild(td)}table.appendChild(tr)}document.getElementById('table').replaceChildren(table)}p.onchange=()=>{weights=p.value==='frozen'?spec.weights:ETFEngine.presets[p.value];draw()};document.getElementById('save').onclick=()=>{const data={...spec,weights:[...weights],parameterVersion:'composite-scenario/1',parentParameterSha256:'''+json.dumps(hashlib.sha256(json.dumps(spec,sort_keys=True,ensure_ascii=False).encode()).hexdigest())+'''};const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='etf-scenario.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};draw();</script></html>'''
        if spec['sampleType']=='teaching':page=page.replace('<p>分值反映','<p><strong>原创教学数据，不是真实板块行情。</strong></p><p>分值反映',1)
        (a.out_dir/'report.html').write_text(page,'utf-8')
        (a.out_dir/'receipt.json').write_text(json.dumps({'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in a.out_dir.iterdir()},'methodVersion':METHOD},indent=2),'utf-8')
        print('报告已保存：'+str(a.out_dir/'report.html'));return 0
    except (ValueError,OSError,KeyError,TypeError,subprocess.TimeoutExpired) as exc:
        print('未完成：'+str(exc),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
