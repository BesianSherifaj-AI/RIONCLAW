"""
Schema node: USER (entry into your flow)
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(payload: dict) -> dict:
    """
    Entry point. Receives the untouched payload from OC channels_inbound.
    Attaches an internal trace id and forwards to SEND.
    """
    import uuid
    return {"trace_id": uuid.uuid4().hex, "payload": payload, "stage": "USER"}
