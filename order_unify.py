"""
Schema node: PROMPT HANDLER
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctx: dict) -> dict:
    """
    - normalize whitespace
    - tag attachments with MIME (if channel wrapper had metadata)
    - strip channel-level wrappers
    - pass untouched payload body downstream
    """
    p = ctx["payload"]
    text = (p.get("text") or "").strip()
    text = " ".join(text.split())
    attachments = p.get("attachments") or []
    for a in attachments:
        if "mime" not in a and "filename" in a:
            import mimetypes
            a["mime"] = mimetypes.guess_type(a["filename"])[0] or "application/octet-stream"
    ctx["payload"] = {"text": text, "attachments": attachments}
    ctx["stage"] = "PROMPT_HANDLER"
    return ctx
