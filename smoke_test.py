"""
Schema node: SEND
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctx: dict) -> dict:
    """Synchronous pass-through. Not OC's async bus."""
    ctx["stage"] = "SEND"
    return ctx
