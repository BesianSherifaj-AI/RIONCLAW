"""
Schema node: USE CODE [OC: skill]
Role: GLUE
See SCHEMA.excalidraw for position in the flow.
"""

from lib.openclaw_shim import skills

def handle(ctx: dict) -> dict:
    """Load the method code and run it via OC skill runner."""
    result = skills().run(ctx["format_method"], {"part": ctx["part"]})
    ctx["convert_input"] = result
    ctx["stage"] = "USE_CODE"
    return ctx
