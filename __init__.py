"""
Schema node: ORDER AND UNIFY PROMPT TO TEXT
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctxs: list[dict]) -> dict:
    """Join converted fragments in source order into one text blob."""
    texts = [c.get("converted_text", "") for c in ctxs]
    base = ctxs[0] if ctxs else {}
    return {**base, "unified_text": "\n\n".join(t for t in texts if t),
            "stage": "ORDER_AND_UNIFY"}
