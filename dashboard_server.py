"""
Schema node: FORMAT IDENTIFIER
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctx: dict) -> dict:
    """
    Decide: text-only vs multi-format.
    Emits ctx["mode"] = "text_only" | "multi_format"
    and ctx["parts"] = list of {kind, ...} for the pipeline.
    """
    p = ctx["payload"]
    parts = []
    if p.get("text"):
        parts.append({"kind": "text", "body": p["text"]})
    for a in p.get("attachments") or []:
        mime = (a.get("mime") or "").lower()
        if mime.startswith("image/"):  parts.append({"kind": "image", "ref": a})
        elif mime.startswith("audio/"):parts.append({"kind": "audio", "ref": a})
        elif mime.startswith("video/"):parts.append({"kind": "video", "ref": a})
        elif mime.startswith("text/"): parts.append({"kind": "text",  "body": a.get("body", "")})
        else:                          parts.append({"kind": "file",  "ref": a})
    kinds = {p["kind"] for p in parts}
    ctx["mode"] = "text_only" if kinds == {"text"} else "multi_format"
    ctx["parts"] = parts
    ctx["stage"] = "FORMAT_IDENTIFIER"
    return ctx
