"""
Schema node: SUPER DETAILED SMALL CONTEXT PROTOCOL
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.schema_config import ROOT
from lib.md_io import read

def handle(ctx: dict) -> dict:
    """Pull only the addressed sections of PROTOCOL/tiny/*.md."""
    pieces = []
    for p in (ROOT / "PROTOCOL" / "tiny").glob("*.md"):
        if p.name.startswith("_"):
            continue
        body = read(p)
        if body:
            pieces.append(f"# from {p.name}\n{body.strip()}")
    ctx["protocol_context"] = "\n\n".join(pieces)
    ctx["stage"] = "SMALL_CONTEXT_PROTO"
    return ctx
