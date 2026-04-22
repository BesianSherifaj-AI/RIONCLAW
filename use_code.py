"""
Schema node: INJECTION GUARD
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctx: dict) -> dict:
    """
    Ensure any self-prompt does not impersonate the user.
    If a self-prompt includes 'As the user', 'the user says', or
    similar impersonation markers, re-route to QUESTION → USER.
    """
    text = (ctx.get("unified_text") or "") + " " + (ctx.get("self_prompt") or "")
    markers = ["as the user", "user says", "user wants", "speaking as user"]
    ctx["injection_risk"] = any(m in text.lower() for m in markers)
    ctx["stage"] = "INJECTION_GUARD"
    return ctx
