import copy,json,shutil,subprocess,unittest
from pathlib import Path
from unittest.mock import patch
from cn_etf_rotation.composite import calculate

class Tests(unittest.TestCase):
    def sample(self):return json.loads((Path(__file__).resolve().parents[1]/'examples/composite-teaching.json').read_text('utf-8'))
    def test_canonical_original_equivalence(self):
        if not shutil.which('node'):self.skipTest('Optional Node not installed')
        s=self.sample();r=calculate(s)
        original=Path(__file__).resolve().parents[1]/'cn_etf_rotation/legacy/engine.js'
        code="const fs=require('fs'),E=require(process.argv[1]),s=JSON.parse(fs.readFileSync(0,'utf8'));const rows=E.calculate(s.snapshot,s.weights,s.asOf);process.stdout.write(JSON.stringify({ranking:rows,allocation:E.allocate(rows,s.selected)}))"
        p=subprocess.run([shutil.which('node'),'-e',code,str(original)],input=json.dumps(s).encode(),capture_output=True,check=True)
        expected=json.loads(p.stdout);self.assertEqual(r['ranking'],expected['ranking']);self.assertEqual(r['allocation'],expected['allocation'])
    def test_missing_observation_stays_unknown(self):
        if not shutil.which('node'):self.skipTest('Optional Node not installed')
        s=self.sample();s['snapshot']['sectors'][0]['raw']['roe']=None;r=calculate(s)
        row=next(x for x in r['ranking'] if x['id']=='a');self.assertIsNone(row['total']);self.assertIsNone(row['rank'])
    def test_node_missing_is_actionable(self):
        with patch('cn_etf_rotation.composite.shutil.which',return_value=None):
            with self.assertRaisesRegex(ValueError,'基础动量'):calculate(self.sample())
    def test_cutoff_and_selection_rejected(self):
        for mutate in [lambda s:s.update(asOf='2026-10-10'),lambda s:s.update(selected=['a','a'])]:
            s=self.sample();mutate(s)
            with self.assertRaises(ValueError):calculate(s)
