#!/bin/bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
LAUNCHER="$PROJECT_ROOT/scripts/launch_macos.sh"

if [[ ! -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
  echo "WhisperTube needs one-time setup first."
  echo "Run: ./scripts/setup_macos.sh"
  echo
  read -r -p "Press Return to close..."
  exit 1
fi

cd "$PROJECT_ROOT"
exec "$LAUNCHER"
