"""
Schema node: RECEIVE
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.schema_config import ROOT
from lib.md_io import append

def handle(ctx: dict) -> dict:
    """Collect runtime results, record them, and branch on success/fail."""
    results = ctx.get("env_results", [])
    any_fail = any(r.get("returncode", 0) != 0 for r in results)
    ctx["branch"] = "fail" if any_fail else "works"
    append(ROOT / "ARCHIVE" / "system_archive_file_record.md",
           f"receive: trace={ctx.get('trace_id')} branch={ctx['branch']} results={len(results)}",
           writer="RECEIVE", reason="runtime results")
    ctx["stage"] = "RECEIVE"
    return ctx
