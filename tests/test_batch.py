import unittest,json
from processor import enrich_batch
class BatchTests(unittest.TestCase):
 def test_preflight_all_before_calls(self):
  calls=[]
  with self.assertRaises(ValueError):enrich_batch([b'{"text":"ok"}',b'{"text":"later","jev":{}}'],evaluate=lambda *_:calls.append(1),api_key='synthetic')
  self.assertEqual(calls,[])
 def test_duplicate_text_rejected(self):
  with self.assertRaises(ValueError):enrich_batch([b'{"text":"first","text":"second"}'],api_key='synthetic')
 def test_order_and_source_preserved(self):
  raw=[b'{"id":1,"text":"a"}',b'{"id":2,"text":"b"}'];x=enrich_batch(raw,evaluate=lambda t,*_:{'outcome':t},api_key='synthetic');self.assertEqual([json.loads(p)['id']for p in x],[1,2]);self.assertNotIn(b'jev',raw[0])
