#!/usr/bin/env bash
# Source .env (for THREADS_ACCESS_TOKEN / THREADS_USER_ID), then pull the replies you left
# on OTHER people's threads - the reach that /threads and snapshot-metrics.sh never see.
# Run from the repo root. Output goes to meta/replies/inbound/ (override with --outdir).
#
# The pull is NOT finished when this exits: the API cannot return the parent posts, so the
# .md work-list it writes has an unresolved parent slot per reply. Fill those from the
# logged-in browser. See ../SKILL.md, "Pulling your own replies."
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f .env ]] && { set -a; source .env; set +a; }
exec python3 "$DIR/pull_replies.py" "$@"
