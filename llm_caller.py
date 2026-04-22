"""
Schema node: ADD AS TASK / SEND TO QUEUE
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.schema_config import ROOT
from lib.md_io import append

def handle(ctx: dict, reason: str = "not possible") -> dict:
    """Record a stuck task; do not retry silently."""
    append(ROOT / "MEMORY" / "self" / "tasks.md",
           f"- [ ] {reason}: trace={ctx.get('trace_id')} part={ctx.get('part')}",
           writer="ADD_AS_TASK", reason=reason)
    ctx["stage"] = "ADD_AS_TASK"
    return ctx
