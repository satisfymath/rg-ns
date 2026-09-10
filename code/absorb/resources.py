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
    """Peak resident size of this process and its finished children."""
    me = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    kids = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024.0
    return max(me, kids)


def safe_workers(peak_worker_mb: float,
                 requested: int | None = None,
                 safety_margin_mb: float = SAFETY_MARGIN_MB) -> int:
    """How many workers of a given measured peak size fit right now."""
    if peak_worker_mb <= 0:
        raise ValueError("peak_worker_mb must be positive")
    avail = mem_available_mb()
    total = mem_total_mb()
    margin = max(safety_margin_mb, FREE_FRACTION_TARGET * total)
    usable = avail - margin
    by_memory = int(usable // peak_worker_mb)
    by_cores = os.cpu_count() or 1
    n = min(requested or by_cores, by_cores, by_memory)
    return max(1, n)


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
    t0 = time.time()
    before = mem_available_mb()
    rss0 = peak_rss_mb()
    try:
        yield
    finally:
        rec = RunRecord(name=name, seconds=time.time() - t0,
                        peak_rss_mb=max(peak_rss_mb(), rss0),
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
