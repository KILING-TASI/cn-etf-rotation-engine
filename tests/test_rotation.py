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
    def test_repeat_cli_results_exclude_runtime_paths(self):
        from cn_etf_rotation.__main__ import publish
        with TemporaryDirectory() as tmp:
            data=teaching();result=backtest(data)
            first,second=Path(tmp)/'a',Path(tmp)/'b';publish(data,result,first);publish(data,result,second)
            self.assertEqual((first/'result.json').read_bytes(),(second/'result.json').read_bytes())
            self.assertEqual((first/'receipt.json').read_bytes(),(second/'receipt.json').read_bytes())
