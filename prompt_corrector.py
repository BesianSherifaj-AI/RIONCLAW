"""
Schema node: QUESTION [OC: approval]
Role: GLUE
See SCHEMA.excalidraw for position in the flow.
"""

from lib.openclaw_shim import approval

def handle(ctx: dict, route: str = "user") -> dict:
    answer = approval().ask(ctx.get("question_text", ctx.get("unified_text", "")), route_to=route)
    ctx["answer"] = answer
    ctx["stage"] = "QUESTION"
    return ctx
