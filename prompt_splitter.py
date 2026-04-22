"""
Schema node: USER OUTPUT
Role: YOURS
See SCHEMA.excalidraw for position in the flow.
"""

from lib.openclaw_shim import channels_outbound

def dispatch(ctx: dict, channel: str = "chat_gui") -> None:
    """Send the user-facing parts to the chosen Windows channel."""
    for msg in ctx.get("splits", {}).get("user", []):
        channels_outbound().send(channel, {"text": msg, "trace_id": ctx.get("trace_id")})
