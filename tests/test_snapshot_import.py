import copy,hashlib,json,unittest
from cn_etf_rotation.snapshot_import import build

class Tests(unittest.TestCase):
    def sample(self):
        from datetime import date,timedelta
        dates=[(date(2025,1,1)+timedelta(days=i)).isoformat() for i in range(30)]
        items=[]
        for code,index in [('510000','declared-a'),('510001','declared-b')]:
            raw=json.dumps({'data':{'code':code,'market':1,'klines':[d+',1,1,1,1,1,1' for d in dates]}})
            snap={'schemaVersion':'cn-market-daily-archive/1.0','status':'success','request':{'kind':'etf','code':code,'market':'SSE'},'rawSha256':hashlib.sha256(raw.encode()).hexdigest(),'priceBasis':'unadjusted','retrievedAt':'2025-02-01T00:00:00+00:00','sourceUrl':'https://example.org/a','data':[{'date':d,'close':'1'} for d in dates]}
            items.append({'snapshot':snap,'rawResponseText':raw,'comparability':'declared-no-distribution-or-split','eventEvidence':'synthetic fixture declaration','indexId':index,'category':'industry'})
        return {'inputSchema':'etf-frozen-pool/1','sampleType':'teaching','asOf':'2025-02-01','instruments':items}
    def test_no_sibling_repo_required(self):self.assertEqual(len(build(self.sample())['engineInput']['rows']),2)
    def test_missing_day_not_hidden_by_intersection(self):
        s=self.sample();item=s['instruments'][1];obj=json.loads(item['rawResponseText']);obj['data']['klines'].pop(0);item['rawResponseText']=json.dumps(obj);item['snapshot']['rawSha256']=hashlib.sha256(item['rawResponseText'].encode()).hexdigest();item['snapshot']['data'].pop(0)
        with self.assertRaisesRegex(ValueError,'日历'):build(s)
    def test_changed_price_even_with_same_response_is_rejected(self):
        s=self.sample();s['instruments'][0]['snapshot']['data'][0]['close']='2'
        with self.assertRaisesRegex(ValueError,'价格'):build(s)
    def test_unknown_events_do_not_become_comparable(self):
        s=self.sample();s['instruments'][0]['comparability']='unknown'
        with self.assertRaisesRegex(ValueError,'事件'):build(s)
    def test_malformed_input_produces_actionable_error(self):
        for s in [None,[],{'inputSchema':'etf-frozen-pool/1','sampleType':'teaching','asOf':'2025-02-01','instruments':[None,None]}]:
            with self.assertRaises(ValueError):build(s)
    def test_original_utf8_bom_is_preserved_in_digest(self):
        s=self.sample();item=s['instruments'][0];item['rawResponseText']='\ufeff'+item['rawResponseText'];item['snapshot']['rawSha256']=hashlib.sha256(item['rawResponseText'].encode()).hexdigest()
        result=build(s);self.assertEqual(result['bindings'][0]['rawSha256'],item['snapshot']['rawSha256'])
