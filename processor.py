"""Redpanda Connect RPC processor for JSON messages."""
import json
import os
from pathlib import Path
from jev_core import decide

POLICY = json.loads((Path(__file__).with_name("policy.json")).read_text())

def enrich(payload, *, evaluate=decide, api_key=None):
    return enrich_batch([payload],evaluate=evaluate,api_key=api_key)[0]

def process_message(message, *, evaluate=decide, api_key=None):
    message.payload = enrich(message.payload, evaluate=evaluate, api_key=api_key)
    return message

def enrich_batch(payloads, *, evaluate=decide, api_key=None):
    error="Lot invalide / Invalid batch / Lote inválido"
    if not isinstance(payloads,list)or not 1<=len(payloads)<=100:raise ValueError(error)
    field=os.getenv("JEV_TEXT_FIELD","text");records=[]
    def unique(pairs):
        out={}
        for key,value in pairs:
            if key in out:raise ValueError(error)
            out[key]=value
        return out
    def invalid_constant(value):raise ValueError(error)
    for payload in payloads:
        if not isinstance(payload,(bytes,str))or len(payload.encode('utf8')if isinstance(payload,str)else payload)>100000:raise ValueError(error)
        record=json.loads(payload,object_pairs_hook=unique,parse_constant=invalid_constant)
        if isinstance(record,dict)and'jev'in record:raise ValueError('Champ réservé jev existant / reserved jev field already exists / Campo reservado jev existente')
        if not isinstance(record,dict) or not isinstance(record.get(field),str)or not record[field].strip()or len(record[field])>16000:raise ValueError(error)
        records.append(record)
    key=api_key or os.environ['TYPESAFE_API_KEY'];output=[]
    for record in records:
        record['jev']=evaluate(record[field],POLICY,key);output.append(json.dumps(record,separators=(',',':'),allow_nan=False).encode())
    return output

if __name__ == "__main__":
    import asyncio
    import redpanda_connect
    @redpanda_connect.processor
    def jev_processor(message):
        return process_message(message)
    asyncio.run(redpanda_connect.processor_main(jev_processor))


