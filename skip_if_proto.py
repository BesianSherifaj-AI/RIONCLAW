"""
Schema node: SEND STATUS TO LLM TO CONVERT
Role: GLUE
See SCHEMA.excalidraw for position in the flow.
"""

from lib.openclaw_shim import llm

def handle(ctx: dict) -> dict:
    """Ask the LLM to produce a new conversion method for an unknown format."""
    prompt = (f"Produce a self-contained method to convert "
              f"{ctx['part']['kind']} (unknown sub-format) to text. "
              f"Return a single code block.")
    resp = llm().complete(prompt, max_tokens=800)
    ctx["llm_method_draft"] = resp["text"]
    ctx["branch"] = "possible" if resp["text"].strip() else "not_possible"
    ctx["stage"] = "SEND_STATUS_TO_LLM"
    return ctx
