"""
Schema node: UPDATES WHEN CHANGED
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

"""
Debounced watcher over the tree. In a real deployment this would use
watchdog; here it's a lightweight poll interface the dashboard can call.
"""
from pathlib import Path
from lib.schema_config import ROOT, FILES

def snapshot() -> dict:
    out = {}
    for rel in FILES:
        p = ROOT / rel
        out[rel] = p.stat().st_mtime if p.exists() else None
    return out
