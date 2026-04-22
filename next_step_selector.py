"""
Schema node: CONVERT
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctx: dict) -> dict:
    """Execute the selected method on the part, producing text."""
    ctx["converted_text"] = (ctx.get("convert_input", {}) or {}).get("result") or ""
    if not ctx["converted_text"] and ctx["part"]["kind"] == "text":
        ctx["converted_text"] = ctx["part"].get("body", "")
    ctx["stage"] = "CONVERT"
    return ctx
