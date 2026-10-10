import unittest,json,subprocess,shutil
from tempfile import TemporaryDirectory
from pathlib import Path
from cn_etf_rotation.__main__ import teaching
from cn_etf_rotation.rotation import rank,exposure
from cn_etf_rotation.review import calculate,backtest

class RotationTests(unittest.TestCase):
    def test_legacy_javascript_equivalence(self):
        node=shutil.which('node')
        if not node:self.skipTest('Node仅用于迁移前后比对，不是运行依赖')
        data=teaching();code="const fs=require('fs'),vm=require('vm');const d=JSON.parse(fs.readFileSync(0,'utf8')),ctx={};vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8')+';this.model=ETFRotationModel;',ctx);console.log(JSON.stringify({ranking:ctx.model.rank(d.rows),marketExposure:ctx.model.exposure(d.marketCloses)}));"
        p=subprocess.run([node,'-e',code,str(Path(__file__).resolve().parents[1]/'cn_etf_rotation/legacy/engine.js')],input=json.dumps(data),capture_output=True,text=True,check=True)
        old=json.loads(p.stdout);new=calculate(data)
        self.assertEqual(old['ranking'],new['ranking'])
        self.assertAlmostEqual(old['marketExposure']['volatility'],new['marketExposure']['volatility'],places=12)
        self.assertEqual(old['marketExposure']['target'],new['marketExposure']['target'])
    def test_duplicate_and_missing_history(self):
        data=teaching();data['rows'][1]['index']=data['rows'][0]['index']
        with self.assertRaises(ValueError):calculate(data)
        self.assertEqual(rank([dict(symbol='a',index='a',eligible=True,type='industry',closes=[1]*20)]),[])
    def test_signal_uses_past_and_executes_next_day(self):
        data=teaching();a=backtest(data)
        data['rows'][0]['closes'][-1]*=3;b=backtest(data)
        self.assertEqual(a['trades'],b['trades'])
        self.assertEqual(a['path'][:-1],b['path'][:-1])
        self.assertTrue(all(t['signalDate']<t['executionDate'] for t in a['trades']))
    def test_cost_and_unknown_market(self):
        data=teaching();zero=backtest(dict(data,costBps=0));fee=backtest(dict(data,costBps=20))
        self.assertLess(fee['totalReturn'],zero['totalReturn']);self.assertFalse(exposure([])['ready'])
    def test_declared_history_requires_cn_market_and_price_basis(self):
        data=teaching();data['origin']='declared-history'
        calculate(data)
        for key,value in [('currency','USD'),('priceBasis','unknown')]:
            with self.assertRaises(ValueError):calculate(dict(data,**{key:value}))
        data['rows'][0]['market']='CN'
        with self.assertRaises(ValueError):calculate(data)
    def test_replacement_boundaries_and_tied_ranks(self):
        from cn_etf_rotation.rotation import may_replace
        args=dict(holdingRank=.4,candidateRank=.5,heldTradingDays=9,isRebalance=True)
        self.assertTrue(may_replace(**args))
        for key,value in [('heldTradingDays',8),('isRebalance',False),('swaps',1),('candidateRank',.499)]:
            self.assertFalse(may_replace(**dict(args,**{key:value})))
        rows=[dict(symbol=s,index=s,eligible=True,type='industry',closes=[1]*21) for s in ['b','a']]
        self.assertEqual(rank(rows),[dict(symbol=s,momentum=0.,rank01=.5) for s in ['a','b']])
    def test_repeat_cli_results_exclude_runtime_paths(self):
        from cn_etf_rotation.__main__ import publish
        with TemporaryDirectory() as tmp:
            data=teaching();result=backtest(data)
            first,second=Path(tmp)/'a',Path(tmp)/'b';publish(data,result,first);publish(data,result,second)
            self.assertEqual((first/'result.json').read_bytes(),(second/'result.json').read_bytes())
            self.assertEqual((first/'receipt.json').read_bytes(),(second/'receipt.json').read_bytes())
