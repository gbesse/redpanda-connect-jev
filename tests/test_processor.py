import json
import unittest
from processor import enrich
class ProcessorTests(unittest.TestCase):
    def test_enrich(self):
        result = json.loads(enrich(b'{"text":"server down","id":42}', evaluate=lambda text, policy, key: {"outcome":"urgent","input":text}, api_key="test"))
        self.assertEqual(result["id"],42)
        self.assertEqual(result["jev"]["outcome"],"urgent")
    def test_non_object(self):
        with self.assertRaises(ValueError): enrich(b'[1]', api_key="test")

    def test_existing_decision_is_not_overwritten(self):
        with self.assertRaisesRegex(ValueError, "reserved jev field"):
            enrich(b'{"text":"server down","jev":{"user":"value"}}', evaluate=lambda *_: self.fail("Jev must not run"), api_key="test")

    def test_sdk_message(self):
        try: from redpanda_connect import Message
        except ImportError: self.skipTest("Redpanda SDK needs Python 3.12")
        message=Message(b'{"text":"Server down"}')
        result=__import__('processor').process_message(message,evaluate=lambda text,policy,key:{"outcome":"urgent"},api_key="test")
        self.assertEqual(json.loads(result.payload)["jev"]["outcome"],"urgent")
