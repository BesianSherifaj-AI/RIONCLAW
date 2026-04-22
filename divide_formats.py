"""
Schema node: MAIN FILE / FILEPATHS (navigate)
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.schema_config import ROOT
from lib.md_io import read

def handle(ctx: dict) -> dict:
    """Read PROTOCOL/main_index.md and append it as navigation context."""
    idx = read(ROOT / "PROTOCOL" / "main_index.md")
    ctx["main_index"] = idx
    ctx["stage"] = "MAIN_FILE_NAVIGATE"
    return ctx
