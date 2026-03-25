import json


def emit_event(event: dict):
    print(json.dumps(event), flush=True)