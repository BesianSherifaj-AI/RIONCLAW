"""
Schema node: NEXT STEP OR STEPS SELECTOR
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.schema_config import ROOT
from lib.md_io import read

def pick() -> dict | None:
    """Read MEMORY/self/actual_tasks.md and return the top unchecked task."""
    md = read(ROOT / "MEMORY" / "self" / "actual_tasks.md")
    for line in md.splitlines():
        line = line.strip()
        if line.startswith("- [ ]"):
            return {"task": line[5:].strip()}
    return None
