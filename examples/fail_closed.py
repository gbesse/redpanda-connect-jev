"""Exercise malformed and reserved-field input without a broker or Jev call."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from processor import enrich

calls = []
def fake_evaluate(text, policy, api_key):
    calls.append(text)
    return {'outcome': 'review', 'choice': 'other'}

for payload in ['[]', '{"text":"message","jev":{"outcome":"ready"}}']:
    try:
        enrich(payload, evaluate=fake_evaluate, api_key='offline-fixture')
    except ValueError:
        pass
    else:
        raise AssertionError('Unsafe payload was accepted')
assert calls == []
accepted = json.loads(enrich('{"text":"message"}', evaluate=fake_evaluate, api_key='offline-fixture'))
assert accepted['jev']['outcome'] == 'review' and calls == ['message']
print(json.dumps({'synthetic': True, 'rejectedBeforeInference': 2, 'acceptedOutcome': 'review', 'providerCalls': len(calls)}))
