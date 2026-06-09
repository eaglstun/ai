#!/usr/bin/env bash
# Source .env (for THREADS_ACCESS_TOKEN / THREADS_USER_ID), then snapshot metrics.
# Run from the repo root. Output goes to meta/metrics/ (override with an arg).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f .env ]] && { set -a; source .env; set +a; }
exec python3 "$DIR/snapshot_metrics.py" "$@"
