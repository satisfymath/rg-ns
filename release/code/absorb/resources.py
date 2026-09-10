"""Memory-aware sizing of parallel work, and peak-usage recording.

The rule this module enforces is simple and deliberately conservative:

    usable  = MemAvailable - SAFETY_MARGIN_MB
    workers = floor(usable / measured_peak_worker_MB)

with a safety margin of at least 1.5 GB, and never more workers than cores.
A long MCMC chain shares this machine; a simulation that triggers the OOM
killer and takes the chain with it is a failure of the project, not a tuning
issue, so the sizing errs low and the measured peak, not the size at fork, is
what is budgeted against.
"""
from __future__ import annotations

import json
import os
import resource
import time
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
USAGE_LOG = ROOT / "results" / "resource_usage.json"

#: Never let MemAvailable fall below this.
SAFETY_MARGIN_MB = 1500.0
#: Additionally try to keep this fraction of total memory free.
FREE_FRACTION_TARGET = 0.20


def _meminfo() -> dict[str, float]:
    out: dict[str, float] = {}
    with open("/proc/meminfo") as fh:
        for line in fh:
            key, _, rest = line.partition(":")
            parts = rest.split()
            if parts:
                out[key] = float(parts[0]) / 1024.0     # MiB
    return out


def mem_available_mb() -> float:
    return _meminfo().get("MemAvailable", float("inf"))


def mem_total_mb() -> float:
    return _meminfo().get("MemTotal", float("inf"))


def peak_rss_mb() -> float:
    """High-water resident size of this process and its *reaped* children.

    Two limitations make this unfit for measuring a block, and both were found
    the hard way.  ``ru_maxrss`` is a monotone high-water mark for the lifetime
    of the process, so a process that touched 320 MB and freed it still reports
    the peak afterwards, which makes ``max(peak_rss_mb(), rss0)`` around a
    ``with`` block a no-op.  And ``RUSAGE_CHILDREN`` is the maximum over
    children of one child's peak, not the sum, and is populated only once a
    child has been reaped -- so for a pool of ``n`` workers it under-reports
    the aggregate by roughly a factor of ``n``, which is precisely the case
    this module exists to size.  Use :func:`tree_rss_mb` to measure, and this
    only for a single-process lifetime figure.
    """
    me = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    kids = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024.0
    return max(me, kids)


def _rss_of(pid: int) -> float:
    """Resident size of one process in MiB, or 0.0 if it has gone."""
    try:
        with open(f"/proc/{pid}/statm") as fh:
            pages = int(fh.read().split()[1])
        return pages * os.sysconf("SC_PAGE_SIZE") / 1024.0 / 1024.0
    except (OSError, IndexError, ValueError):
        return 0.0


def _descendants(pid: int) -> list[int]:
    """Every live descendant of ``pid``, via /proc/<pid>/task/*/children."""
    out, stack = [], [pid]
    while stack:
        cur = stack.pop()
        try:
            tasks = os.listdir(f"/proc/{cur}/task")
        except OSError:
            continue
        for t in tasks:
            try:
                with open(f"/proc/{cur}/task/{t}/children") as fh:
                    kids = [int(x) for x in fh.read().split()]
            except (OSError, ValueError):
                continue
            out.extend(kids)
            stack.extend(kids)
    return out


def tree_rss_mb(pid: int | None = None) -> float:
    """Summed resident size of a process and every live descendant, in MiB.

    This is the quantity that matters for a pool: what the machine is holding
    right now on behalf of this run.  It counts shared pages once per process,
    so for a forked pool it over-states demand -- the error is in the safe
    direction, and correcting it would mean parsing every smaps_rollup.
    """
    root = os.getpid() if pid is None else pid
    return _rss_of(root) + sum(_rss_of(p) for p in _descendants(root))


def safe_workers(peak_worker_mb: float,
                 requested: int | None = None,
                 safety_margin_mb: float = SAFETY_MARGIN_MB) -> int:
    """How many workers of a given measured peak size fit right now.

    Returns **0** when not even one fits, and callers are expected to decline
    rather than proceed.  An earlier version ended in ``max(1, n)``, which made
    the floor it advertises unenforceable: asked for room for a 100 GB worker
    with 1.8 GB available it still answered "one", so a caller that trusted it
    would start work below the reserve it exists to protect.  The reserve is
    the larger of ``safety_margin_mb`` and a fifth of total memory, which on
    this machine is the fifth, about 3 GB.
    """
    if peak_worker_mb <= 0:
        raise ValueError("peak_worker_mb must be positive")
    avail = mem_available_mb()
    total = mem_total_mb()
    margin = max(safety_margin_mb, FREE_FRACTION_TARGET * total)
    usable = avail - margin
    by_memory = int(usable // peak_worker_mb)
    by_cores = os.cpu_count() or 1
    return max(0, min(requested or by_cores, by_cores, by_memory))


def require_workers(peak_worker_mb: float, requested: int | None = None,
                    what: str = "this run") -> int:
    """:func:`safe_workers`, refusing to proceed when nothing fits."""
    n = safe_workers(peak_worker_mb, requested)
    if n == 0:
        raise MemoryError(
            f"not enough memory for {what}: {describe_budget(peak_worker_mb)}. "
            f"Wait for the running work to finish rather than starting below "
            f"the reserve.")
    return n


def describe_budget(peak_worker_mb: float) -> str:
    total, avail = mem_total_mb(), mem_available_mb()
    margin = max(SAFETY_MARGIN_MB, FREE_FRACTION_TARGET * total)
    return (f"{avail:.0f} MB available of {total:.0f} MB, reserving "
            f"{margin:.0f} MB, at {peak_worker_mb:.0f} MB per worker "
            f"-> {safe_workers(peak_worker_mb)} worker(s)")


@dataclass
class RunRecord:
    """What an experiment cost, recorded so the paper can quote it."""

    name: str
    seconds: float
    peak_rss_mb: float
    mem_available_before_mb: float
    mem_available_after_mb: float
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@contextmanager
def record(name: str, notes: str = ""):
    """Time a block, capture its peak resident size, and append it to the log."""
    import threading

    t0 = time.time()
    before = mem_available_mb()
    # Sample the whole process tree while the block runs.  ru_maxrss cannot do
    # this: it is a lifetime high-water mark, and for children it is the
    # maximum over one child rather than the sum over the pool.
    peak = [tree_rss_mb()]
    stop = threading.Event()

    def _watch() -> None:
        while not stop.wait(0.25):
            peak[0] = max(peak[0], tree_rss_mb())

    watcher = threading.Thread(target=_watch, daemon=True)
    watcher.start()
    try:
        yield
    finally:
        stop.set()
        watcher.join(timeout=1.0)
        peak[0] = max(peak[0], tree_rss_mb())
        rec = RunRecord(name=name, seconds=time.time() - t0,
                        peak_rss_mb=peak[0],
                        mem_available_before_mb=before,
                        mem_available_after_mb=mem_available_mb(),
                        notes=notes)
        USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
        log = []
        if USAGE_LOG.exists():
            try:
                log = json.loads(USAGE_LOG.read_text())
            except json.JSONDecodeError:               # pragma: no cover
                log = []
        log.append(rec.to_dict())
        USAGE_LOG.write_text(json.dumps(log, indent=2))
        print(f"[resources] {name}: {rec.seconds:.1f} s, "
              f"peak RSS {rec.peak_rss_mb:.0f} MB, "
              f"MemAvailable {before:.0f} -> {rec.mem_available_after_mb:.0f} MB")
