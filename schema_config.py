#!/usr/bin/env bash
# One-time setup after unzip. Safe to re-run.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "[bootstrap] working dir: $(pwd)"

if ! command -v python3 >/dev/null; then
    echo "[bootstrap] python3 not found — install it first"
    exit 2
fi

echo "[bootstrap] installing requirements"
python3 -m pip install --user -q pyyaml \
    || python3 -m pip install --user -q --break-system-packages pyyaml \
    || echo "[bootstrap] WARNING: could not install pyyaml — install manually"

echo "[bootstrap] running integrity check"
python3 scripts/verify_integrity.py

echo "[bootstrap] running unit tests (pytest if available, else unittest)"
if python3 -c "import pytest" 2>/dev/null; then
    python3 -m pytest -q tests/
else
    python3 -m unittest discover -s tests -v 2>&1 | tail -20
fi

echo "[bootstrap] DONE. Next: paste BOOT_PROMPT.md to your OpenClaw agent."
