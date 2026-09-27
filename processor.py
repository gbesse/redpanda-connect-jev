"""Redpanda Connect RPC processor for JSON messages."""
import json
import os
from pathlib import Path
from jev_core import decide

POLICY = json.loads((Path(__file__).with_name("policy.json")).read_text())

def enrich(payload, *, evaluate=decide, api_key=None):
    record = json.loads(payload)
    if not isinstance(record, dict): raise ValueError("JSON object required")
    field = os.getenv("JEV_TEXT_FIELD", "text")
    text = record.get(field)
    record["jev"] = evaluate(text, POLICY, api_key or os.environ["TYPESAFE_API_KEY"])
    return json.dumps(record, separators=(",", ":")).encode()

def process_message(message, *, evaluate=decide, api_key=None):
    message.payload = enrich(message.payload, evaluate=evaluate, api_key=api_key)
    return message

if __name__ == "__main__":
    import asyncio
    import redpanda_connect
    @redpanda_connect.processor
    def jev_processor(message):
        return process_message(message)
    asyncio.run(redpanda_connect.processor_main(jev_processor))
