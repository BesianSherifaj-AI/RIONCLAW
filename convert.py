"""
Schema node: FORMAT FINDER (per kind)
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

"""
FILE / AUDIO / VIDEO / IMAGE / TEXT format finders share this code.
The caller passes `kind` and this node reads
ARCHIVE/codes/<kind>/*.md to find a working method. Unknown → route
to SEND_STATUS_TO_LLM.
"""
from pathlib import Path
from lib.schema_config import ROOT

def handle(ctx: dict, kind: str) -> dict:
    methods_dir = ROOT / "ARCHIVE" / "codes" / kind
    methods_dir.mkdir(parents=True, exist_ok=True)
    methods = sorted([p for p in methods_dir.glob("*.md")], reverse=True)
    if methods:
        # pick highest version (lexical sort with .v2, .v3 suffix)
        ctx["format_method"] = str(methods[0].relative_to(ROOT))
        ctx["branch"] = "known"
    else:
        ctx["branch"] = "unknown"
    ctx["stage"] = f"{kind.upper()}_FORMAT_FINDER"
    return ctx
