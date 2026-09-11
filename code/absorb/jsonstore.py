"""Read-modify-write of a shared results file, without losing a concurrent run.

Every long script here updates one key of a JSON file that other scripts also
update. The obvious implementation -- read at the start, write at the end --
loses whatever a concurrent run wrote in between, and it did: two profile runs
launched minutes apart produced two results and the file kept one, silently,
with the survivor's copy of the other key being the stale version it had read
hours earlier.

The fix is to merge at write time under a lock rather than at read time, so a
writer only ever replaces the keys it computed.
"""
from __future__ import annotations

import fcntl
import json
import os
import tempfile
from pathlib import Path


def update(path: Path, entries: dict) -> dict:
    """Merge ``entries`` into the JSON object at ``path`` and return the result.

    The file is locked for the whole read-modify-write, and replaced by an
    atomic rename, so a reader never sees a half-written file and two writers
    never lose each other's keys. The lock is held on a sidecar rather than on
    the file itself, because the atomic rename would otherwise replace the
    inode the lock is on.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix(path.suffix + ".lock")
    with open(lock, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            current = json.loads(path.read_text()) if path.exists() else {}
            if not isinstance(current, dict):
                raise TypeError(f"{path} does not hold a JSON object")
            current.update(entries)
            fd, tmp = tempfile.mkstemp(dir=str(path.parent),
                                       prefix=path.name + ".", suffix=".tmp")
            try:
                with os.fdopen(fd, "w") as out:
                    json.dump(current, out, indent=2, sort_keys=True)
                    out.flush()
                    os.fsync(out.fileno())
                os.replace(tmp, path)
            except BaseException:
                os.unlink(tmp)
                raise
            return current
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)
