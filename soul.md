#!/usr/bin/env python3
"""Checks every file in config/schema.yaml exists."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.schema_config import ROOT, FILES

missing = [f for f in FILES if not (ROOT / f).exists()]
if missing:
    print("MISSING:")
    for m in missing: print(" -", m)
    sys.exit(1)
print(f"OK — {len(FILES)} files present")
