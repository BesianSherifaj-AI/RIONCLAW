"""
Schema node: SEND TO QUEUE (text only)
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.openclaw_shim import queue

def handle(ctx: dict) -> dict:
    queue().enqueue({"trace_id": ctx["trace_id"], "text": ctx["unified_text"]})
    ctx["stage"] = "SEND_TO_QUEUE"
    return ctx
