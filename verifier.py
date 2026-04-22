"""
Schema node: CHECK RULE (memory/tools needed?)
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.schema_config import ROOT
from lib.md_io import read

def handle(ctx: dict) -> dict:
    """
    Decide whether VERIFIER is needed.
    Scans the prompt for tool triggers and memory references.
    """
    prompt = ctx.get("unified_text", "") or ""
    tool_record = read(ROOT / "TOOLS" / "tool_record.md")
    mem_index   = read(ROOT / "MEMORY" / "index.md")
    needs_tool = any(tok.lower() in prompt.lower()
                     for tok in _extract_names(tool_record) if tok)
    needs_mem  = any(tok.lower() in prompt.lower()
                     for tok in _extract_names(mem_index) if tok)
    ctx["needs"] = {"tools": needs_tool, "memory": needs_mem}
    ctx["branch"] = "needed" if (needs_tool or needs_mem) else "not_needed"
    ctx["stage"] = "CHECK_RULE"
    return ctx

def _extract_names(md: str) -> list[str]:
    import re
    # pull anything that looks like a name/identifier in bullet or table rows
    return [m.group(1) for m in re.finditer(r"[-*]\s+`?([A-Za-z0-9_.\-/]+)`?", md)]
