#!/usr/bin/env bash
#
# post-draft.sh — pull a chosen draft block out of an inbox/meta markdown file and
# publish it to Threads (two-step create → publish). Dry-run by default; only sends
# with --post. See ../SKILL.md for the API details.
#
# Usage:
#   post-draft.sh [options] <draft.md>
#
# Options:
#   --pick <LETTER>     Which block to post: A, B, C... (default: the "## ✅ Pick:" block)
#   --reply-to <ID>     Publish as a reply under this Threads media id
#   --post              Actually publish. Without this, prints a preview and exits.
#   -h, --help          Show this help.
#
# Env (required only with --post):
#   THREADS_ACCESS_TOKEN   60-day long-lived token
#   THREADS_USER_ID        numeric Threads user id
#
# Block format it understands (see inbox/graelanf.md, inbox/yugshende94.md):
#   ## ✅ Pick: A — the rep          <- the chosen block
#   > line one                       (leading "> " is stripped; un-quoted lines work too)
#   > line two
#   (339)                            <- char-count line, ends the block
#
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
API="https://graph.threads.net/v1.0"
MAXLEN=500

PICK=""
REPLY_TO=""
DO_POST=0
FILE=""

usage() { sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pick)     PICK="${2:?--pick needs a letter}"; shift 2 ;;
    --reply-to) REPLY_TO="${2:?--reply-to needs a media id}"; shift 2 ;;
    --post)     DO_POST=1; shift ;;
    -h|--help)  usage 0 ;;
    -*)         echo "unknown option: $1" >&2; usage 1 ;;
    *)          FILE="$1"; shift ;;
  esac
done

[[ -n "$FILE" ]] || { echo "error: no draft file given" >&2; usage 1; }
[[ -f "$FILE" ]] || { echo "error: no such file: $FILE" >&2; exit 1; }

# --- extract the chosen block's text -----------------------------------------
# extract_pick.py finds the heading (the ✅ Pick block, or "## <LETTER> —" with
# --pick), collects its body, unwraps soft line-wraps, and warns on markdown.
TEXT="$(PICK="$PICK" python3 "$DIR/extract_pick.py" "$FILE")"

LEN=${#TEXT}

# --- preview -----------------------------------------------------------------
echo "── draft: $FILE${PICK:+  (pick $PICK)}${REPLY_TO:+  reply→$REPLY_TO}"
echo "────────────────────────────────────────────────────────"
printf '%s\n' "$TEXT"
echo "────────────────────────────────────────────────────────"
echo "chars: $LEN / $MAXLEN"

if (( LEN > MAXLEN )); then
  echo "✗ over the $MAXLEN-char Threads limit — trim before posting." >&2
  exit 1
fi

if (( DO_POST == 0 )); then
  echo "(dry run — re-run with --post to publish as Eric)"
  exit 0
fi

# --- publish (two-step) ------------------------------------------------------
: "${THREADS_ACCESS_TOKEN:?set THREADS_ACCESS_TOKEN to publish}"
: "${THREADS_USER_ID:?set THREADS_USER_ID to publish}"

echo "→ creating container…"
create_args=( -s -X POST "$API/${THREADS_USER_ID}/threads"
  -d "media_type=TEXT"
  --data-urlencode "text=${TEXT}"
  -d "access_token=${THREADS_ACCESS_TOKEN}" )
[[ -n "$REPLY_TO" ]] && create_args+=( -d "reply_to_id=${REPLY_TO}" )

CREATE="$(curl "${create_args[@]}")"
CONTAINER_ID="$(printf '%s' "$CREATE" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("id",""))' 2>/dev/null || true)"
if [[ -z "$CONTAINER_ID" ]]; then
  echo "✗ container create failed: $CREATE" >&2
  exit 1
fi
echo "  container: $CONTAINER_ID"

echo "→ publishing…"
PUBLISH="$(curl -s -X POST "$API/${THREADS_USER_ID}/threads_publish" \
  -d "creation_id=${CONTAINER_ID}" \
  -d "access_token=${THREADS_ACCESS_TOKEN}")"
MEDIA_ID="$(printf '%s' "$PUBLISH" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("id",""))' 2>/dev/null || true)"
if [[ -z "$MEDIA_ID" ]]; then
  echo "✗ publish failed: $PUBLISH" >&2
  exit 1
fi
echo "✓ live — media id: $MEDIA_ID"
