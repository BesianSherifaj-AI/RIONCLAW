"""
Schema node: VERIFIER
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

def handle(ctx: dict) -> dict:
    """
    Enter the protocol-navigation + correction subgraph.
    The yaml wires this to SMALL_CONTEXT_PROTO next.
    """
    ctx["stage"] = "VERIFIER"
    return ctx
