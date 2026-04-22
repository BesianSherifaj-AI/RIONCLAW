"""
Schema node: DIVIDE FORMATS INDIVIDUALLY
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctx: dict) -> list[dict]:
    """Yield one sub-ctx per part for the format pipeline."""
    return [{**ctx, "part": part, "stage": "DIVIDE_FORMATS"} for part in ctx.get("parts", [])]
