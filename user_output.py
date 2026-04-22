"""
Schema node: SELF OUTPUT
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.openclaw_shim import queue

def handle(ctx: dict) -> dict:
    """Re-enqueue a self-prompt as a new turn in PROMPT_QUEUE."""
    for self_msg in ctx.get("splits", {}).get("self", []):
        queue().enqueue({"trace_id": ctx.get("trace_id"), "text": self_msg,
                         "origin": "SELF_OUTPUT"})
    ctx["stage"] = "SELF_OUTPUT"
    return ctx
