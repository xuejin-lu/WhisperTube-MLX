#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$SCRIPT_DIR/scripts/launch_macos.sh"

if [[ ! -x "$SCRIPT_DIR/.venv/bin/python" ]]; then
  echo "WhisperTube needs one-time setup first."
  echo "Run: $SCRIPT_DIR/scripts/setup_macos.sh"
  echo
  read -r -p "Press Return to close..." _ || true
  exit 1
fi

set +e
"$LAUNCHER" "$@"
STATUS=$?
set -e
echo
if [[ "$STATUS" -eq 0 ]]; then
  echo "Download finished."
else
  echo "Download failed with exit code $STATUS."
fi
read -r -p "Press Return to close..." _ || true
exit "$STATUS"
