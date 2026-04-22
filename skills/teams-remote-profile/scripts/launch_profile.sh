#!/usr/bin/env bash
set -euo pipefail

SRC_ROOT="${1:-$HOME/.config/google-chrome}"
PROFILE_DIR="${2:-Default}"
PORT="${3:-9223}"
TEMP_DIR="${4:-/tmp/codex-chrome-remote-profile}"
CHROME_BIN="${CHROME_BIN:-/usr/bin/google-chrome}"

if [[ ! -d "$SRC_ROOT" ]]; then
  echo "missing profile root: $SRC_ROOT" >&2
  exit 1
fi

if [[ ! -d "$SRC_ROOT/$PROFILE_DIR" ]]; then
  echo "missing profile directory: $SRC_ROOT/$PROFILE_DIR" >&2
  exit 1
fi

if [[ ! -x "$CHROME_BIN" ]]; then
  echo "missing chrome binary: $CHROME_BIN" >&2
  exit 1
fi

mkdir -p "$TEMP_DIR"
rsync -a --delete "$SRC_ROOT/" "$TEMP_DIR/"
rm -f "$TEMP_DIR/SingletonLock" "$TEMP_DIR/SingletonSocket" "$TEMP_DIR/SingletonCookie"

setsid -f "$CHROME_BIN" \
  --user-data-dir="$TEMP_DIR" \
  --profile-directory="$PROFILE_DIR" \
  --remote-debugging-port="$PORT" \
  --remote-allow-origins="*" \
  --no-first-run \
  about:blank

sleep 2

echo "temp_dir=$TEMP_DIR"
echo "port=$PORT"
curl -s "http://127.0.0.1:$PORT/json/version"
