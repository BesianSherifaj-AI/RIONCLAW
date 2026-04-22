"""
Schema node: OUTPUT
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctx: dict) -> dict:
    """Receive LLM stream, forward to splitter."""
    ctx["stage"] = "OUTPUT"
    return ctx
