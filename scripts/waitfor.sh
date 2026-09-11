#!/bin/bash
# Wait for a background job by PID file, not by pgrep pattern.
#
# The pattern form deadlocks on itself: a shell running
#     until ! pgrep -f "run_map.py"; do sleep 20; done
# has "run_map.py" in its own command line, so pgrep matches the waiter and the
# condition never becomes true. Thirteen such shells accumulated in one session,
# each holding memory and never firing.
#
# Usage:
#   scripts/waitfor.sh start <name> <command...>   # runs it, records the PID
#   scripts/waitfor.sh wait  <name> [interval]     # blocks until it exits
set -euo pipefail
DIR="${TMPDIR:-/tmp}/rgns-pids"; mkdir -p "$DIR"

case "${1:-}" in
  start)
    name="$2"; shift 2
    setsid nohup "$@" > "logs/${name}.log" 2>&1 < /dev/null &
    echo $! > "$DIR/$name.pid"
    echo "started $name as pid $(cat "$DIR/$name.pid")"
    ;;
  wait)
    name="$2"; interval="${3:-20}"
    pidfile="$DIR/$name.pid"
    [ -f "$pidfile" ] || { echo "no pid file for $name"; exit 1; }
    pid=$(cat "$pidfile")
    while kill -0 "$pid" 2>/dev/null; do sleep "$interval"; done
    echo "$name (pid $pid) finished"
    ;;
  *) echo "usage: $0 {start|wait} <name> [...]"; exit 2 ;;
esac
