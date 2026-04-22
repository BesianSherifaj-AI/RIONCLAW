#!/usr/bin/env python3
"""End-to-end dry run through the flow using the shim primitives."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nodes import (user_entry, send, prompt_handler, format_identifier,
                   order_unify, send_to_queue, prompt_queue, llm_status_check,
                   model, check_rule, verifier, small_context, main_file_nav,
                   prompt_corrector, injection_guard, llm_caller, output,
                   prompt_splitter, user_output, command_output)

def run():
    payload = {"text": "hello from smoke test", "attachments": []}
    ctx = user_entry.handle(payload)
    ctx = send.handle(ctx)
    ctx = prompt_handler.handle(ctx)
    ctx = format_identifier.handle(ctx)
    assert ctx["mode"] == "text_only", f"unexpected mode: {ctx['mode']}"
    # text-only skip to order-unify with a single part
    ctx = order_unify.handle([{**ctx, "converted_text": ctx["payload"]["text"]}])
    ctx = send_to_queue.handle(ctx)
    item = prompt_queue.dequeue()
    assert item is not None, "queue was empty"
    ctx["unified_text"] = item["text"]
    ctx = llm_status_check.handle(ctx)
    ctx = model.handle(ctx)
    ctx = check_rule.handle(ctx)
    # go through verifier path for completeness
    ctx = verifier.handle(ctx)
    ctx = small_context.handle(ctx)
    ctx = main_file_nav.handle(ctx)
    ctx = prompt_corrector.handle(ctx)
    ctx = injection_guard.handle(ctx)
    assert ctx.get("injection_risk") in (True, False)
    ctx = llm_caller.handle(ctx)
    ctx = output.handle(ctx)
    ctx = prompt_splitter.handle(ctx)
    user_output.dispatch(ctx, channel="chat_gui")
    _ = command_output.execute(ctx)
    print("smoke test passed")
    print(" trace_id:", ctx["trace_id"])
    print(" llm_output:", ctx.get("llm_output")[:100])

if __name__ == "__main__":
    run()
