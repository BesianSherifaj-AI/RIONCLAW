"""
Schema node: SKIP IF PROTOCOL NOT MET
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctx: dict) -> dict:
    """Fast-path to LLM when no protocol/verification is needed."""
    ctx["stage"] = "SKIP_IF_PROTO_NOT_MET"
    return ctx
