"""
Schema node: ADD NEW METHOD CODE ARCHIVE
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from pathlib import Path
from lib.schema_config import ROOT
from lib.md_io import append

def handle(ctx: dict) -> dict:
    """Append a new method file; never edit existing."""
    import hashlib, datetime
    kind = ctx["part"]["kind"]
    h = hashlib.sha1(ctx["llm_method_draft"].encode()).hexdigest()[:8]
    name = f"method_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{h}.md"
    p = ROOT / "ARCHIVE" / "codes" / kind / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(ctx["llm_method_draft"].rstrip() + "\n")
    # record the event
    append(ROOT / "ARCHIVE" / "system_archive_file_record.md",
           f"new method: {name} (kind={kind})",
           writer="ADD_NEW_METHOD", reason="method discovery")
    ctx["format_method"] = str(p.relative_to(ROOT))
    ctx["stage"] = "ADD_NEW_METHOD"
    return ctx
