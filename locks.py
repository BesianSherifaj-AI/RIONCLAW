"""
Schema node: PROMPT QUEUE [OC: queue]
Role: NATIVE
See SCHEMA.excalidraw for position in the flow.
"""

from lib.openclaw_shim import queue

def dequeue() -> dict | None:
    return queue().dequeue()
def size() -> int:
    return queue().size()
