"""
Schema node: MODEL
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctx: dict) -> dict:
    """Chooses provider/model; real selection reads LLMS/providers.md."""
    ctx["model_choice"] = "default"
    ctx["stage"] = "MODEL"
    return ctx
