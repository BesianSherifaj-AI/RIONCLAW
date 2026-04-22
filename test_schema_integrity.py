"""
Advisory file locking via fcntl.flock.
On timeout, raises LockFailed — the caller's schema rule is:
    lock failure → ADD_AS_TASK (queue), never silently retry.
"""
from __future__ import annotations
import fcntl, os, time, contextlib
from pathlib import Path

class LockFailed(RuntimeError):
    pass

@contextlib.contextmanager
def file_lock(target: Path, timeout: float = 0.25):
    """
    Acquire an exclusive lock on `target`.lock; yield; release.
    timeout is in seconds.
    """
    lock_path = Path(str(target) + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o644)
    deadline = time.monotonic() + timeout
    try:
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() > deadline:
                    raise LockFailed(f"could not lock {target} in {timeout}s")
                time.sleep(0.01)
        yield
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)
