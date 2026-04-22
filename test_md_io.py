"""
Abstract interfaces for OpenClaw primitives. The local stubs let the
scaffold run end-to-end without OpenClaw installed. The agent replaces
each method body with the real OpenClaw SDK call at wire-up time.

Keep the method signatures identical — nodes/ depends on them.
"""
from __future__ import annotations
from typing import Any, Callable
from collections import deque
import threading

# ─── Channels ────────────────────────────────────────────────────
class ChannelInbound:
    """Receives messages from Windows channels (Telegram/WhatsApp/etc)."""
    def __init__(self):
        self._handlers: list[Callable[[dict], None]] = []

    def register(self, handler: Callable[[dict], None]) -> None:
        self._handlers.append(handler)

    def receive(self, payload: dict) -> None:
        # AGENT: replace — OpenClaw pushes inbound payloads here from
        # its channel subsystem. In real wiring, subscribe to OC
        # channel events and call each handler for this schema.
        for h in self._handlers:
            h(payload)

class ChannelOutbound:
    """Delivers a payload to a named Windows channel."""
    def send(self, channel: str, payload: dict) -> None:
        # AGENT: replace with real OC SDK call — e.g.
        #     oc.channels.send(channel=channel, payload=payload)
        print(f"[oc_shim] outbound → {channel}: {payload}")

# ─── Runtimes ────────────────────────────────────────────────────
class Runtime:
    """Executes a command against a named runtime. Returns stdout/stderr/rc."""
    def execute(self, runtime: str, command: str, env: dict | None = None) -> dict:
        # AGENT: replace with real OC runtime call.
        return {"runtime": runtime, "command": command,
                "stdout": "", "stderr": "shim", "returncode": 0}

# ─── Skills ──────────────────────────────────────────────────────
class SkillRunner:
    """Runs a user-defined skill (a piece of method code from ARCHIVE)."""
    def run(self, skill_name: str, args: dict) -> dict:
        # AGENT: replace — invoke the OC skill registry.
        return {"skill": skill_name, "args": args, "result": None, "error": "shim"}

# ─── Queue ───────────────────────────────────────────────────────
class Queue:
    """FIFO queue. The schema's PROMPT_QUEUE sits on top of this."""
    def __init__(self):
        self._q = deque()
        self._lock = threading.Lock()

    def enqueue(self, item: Any) -> None:
        with self._lock:
            self._q.append(item)

    def dequeue(self) -> Any | None:
        with self._lock:
            return self._q.popleft() if self._q else None

    def size(self) -> int:
        return len(self._q)

# ─── Secret store ────────────────────────────────────────────────
class SecretStore:
    """Get/set credentials. Backed by OS keychain in real OC."""
    def __init__(self):
        self._kv: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        # AGENT: replace with OC secret store read.
        return self._kv.get(key)

    def set(self, key: str, value: str) -> None:
        # AGENT: replace with OC secret store write.
        self._kv[key] = value

# ─── Approval gate ───────────────────────────────────────────────
class ApprovalGate:
    """Used ONLY by the QUESTION node. Blocks until user or self answers."""
    def ask(self, prompt: str, route_to: str = "user",
            timeout_sec: float = 300.0) -> str:
        # AGENT: replace with OC approval/elicitation call.
        return f"[shim-answer to: {prompt[:60]}]"

# ─── LLM provider ────────────────────────────────────────────────
class LLMProvider:
    """The ONLY entry point to an LLM."""
    def complete(self, prompt: str, *, model: str = "default",
                 max_tokens: int = 1024, stream: bool = False) -> dict:
        # AGENT: replace with OC LLM provider call (Ollama / LMStudio / API).
        return {"model": model, "text": f"[shim LLM output for prompt len={len(prompt)}]"}

    def status(self) -> dict:
        """Return {"state": "working"|"idle"|"waiting", ...}"""
        # AGENT: replace with real provider health check.
        return {"state": "idle", "providers": []}

# ─── Singleton accessors ────────────────────────────────────────
_channels_in   = ChannelInbound()
_channels_out  = ChannelOutbound()
_runtime       = Runtime()
_skills        = SkillRunner()
_queue         = Queue()
_secrets       = SecretStore()
_approval      = ApprovalGate()
_llm           = LLMProvider()

def channels_inbound()   -> ChannelInbound:  return _channels_in
def channels_outbound()  -> ChannelOutbound: return _channels_out
def runtime()            -> Runtime:         return _runtime
def skills()             -> SkillRunner:     return _skills
def queue()              -> Queue:           return _queue
def secrets()            -> SecretStore:     return _secrets
def approval()           -> ApprovalGate:    return _approval
def llm()                -> LLMProvider:     return _llm
