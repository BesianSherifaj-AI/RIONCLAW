"""
Schema node: PROMPT CORRECTOR
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.schema_config import ROOT
from lib.md_io import read, patch

def handle(ctx: dict) -> dict:
    """
    If the prompt seems ambiguous OR confidence is low, patch soul.md
    with a refinement note (named section 'refinements') and flag
    that a QUESTION may be needed.
    """
    soul = read(ROOT / "PROTOCOL" / "soul.md")
    ctx["soul"] = soul
    # very simple heuristic; replace with your real one
    prompt = ctx.get("unified_text", "")
    ctx["correction_needed"] = len(prompt) < 8
    ctx["stage"] = "PROMPT_CORRECTOR"
    return ctx
