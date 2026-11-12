import unittest,json
from processor import enrich
class SinglePreflight(unittest.TestCase):
 def test_duplicate_keys_rejected_before_call(self):
  calls=[]
  with self.assertRaises(ValueError):enrich('{"text":"first","text":"second"}',api_key='synthetic',evaluate=lambda *a:calls.append(a))
  self.assertEqual(calls,[])
 def test_nonfinite_values_rejected(self):
  with self.assertRaises(ValueError):enrich('{"text":"x","other":NaN}',api_key='synthetic')
 def test_utf8_byte_budget_not_character_count(self):
  payload=json.dumps({'text':'x','extra':'é'*60000},ensure_ascii=False)
  with self.assertRaises(ValueError):enrich(payload,api_key='synthetic')
