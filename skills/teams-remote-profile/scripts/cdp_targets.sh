#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-9223}"
MODE="${2:-all}"

BASE_URL="http://127.0.0.1:$PORT"

echo "# version"
curl -s "$BASE_URL/json/version"
echo
echo "# targets"

LIST_JSON="$(curl -s "$BASE_URL/json/list")"

if [[ "$MODE" == "teams" ]]; then
  printf '%s' "$LIST_JSON" | jq -r '
    .[]
    | select(
        (.title | test("Microsoft Teams|teams"; "i"))
        or (.url | test("teams\\.cloud\\.microsoft|teams\\.microsoft\\.com"; "i"))
      )
    | [.id, .type, .title, .url, .webSocketDebuggerUrl] | @tsv
  '
else
  printf '%s' "$LIST_JSON" | jq -r '
    .[]
    | [.id, .type, .title, .url, .webSocketDebuggerUrl] | @tsv
  '
fi
