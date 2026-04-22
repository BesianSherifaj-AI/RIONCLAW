"""
Schema node: LLM STATUS CHECK
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.openclaw_shim import llm

def handle(ctx: dict) -> dict:
    s = llm().status()
    state = s.get("state", "idle")
    ctx["llm_state"] = state
    ctx["stage"] = "LLM_STATUS_CHECK"
    return ctx
