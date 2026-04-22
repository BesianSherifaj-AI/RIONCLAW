"""
Schema node: COMMAND OUTPUT → environments
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.openclaw_shim import runtime

def execute(ctx: dict) -> list[dict]:
    """Send each env-tagged command to its runtime; collect results."""
    results = []
    for item in ctx.get("splits", {}).get("env", []):
        r = runtime().execute(item["runtime"], item["command"])
        results.append({**r, "runtime": item["runtime"], "command": item["command"]})
    ctx["env_results"] = results
    return results
