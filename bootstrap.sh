"""
Schema node: LLM [OC: provider]
Role: NATIVE
See SCHEMA.excalidraw for position in the flow.
"""

from lib.openclaw_shim import llm

def handle(ctx: dict) -> dict:
    parts = [p for p in (ctx.get("protocol_context", ""), ctx.get("main_index", ""),
                          ctx.get("unified_text", "")) if p]
    prompt = "\n\n".join(parts)
    resp = llm().complete(prompt, model=ctx.get("model_choice", "default"))
    ctx["llm_output"] = resp["text"]
    ctx["stage"] = "LLM"
    return ctx
