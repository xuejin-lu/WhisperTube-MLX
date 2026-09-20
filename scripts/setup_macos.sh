#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_PATH="$PROJECT_ROOT/.venv"
VENV_PYTHON="$VENV_PATH/bin/python"

cd "$PROJECT_ROOT"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "ERROR: $PYTHON_BIN was not found; install a native Python 3.10+ and retry." >&2
  exit 1
fi

if ! "$PYTHON_BIN" -m whispertube.release --check; then
  echo "Setup stopped before changing the project environment." >&2
  exit 1
fi

if [[ ! -x "$VENV_PYTHON" ]]; then
  if [[ -e "$VENV_PATH" ]]; then
    echo "ERROR: $VENV_PATH exists but has no executable Python; move it aside and retry." >&2
    exit 1
  fi
  "$PYTHON_BIN" -m venv "$VENV_PATH"
fi

"$VENV_PYTHON" -m pip install --require-virtualenv \
  -r "$PROJECT_ROOT/requirements-macos.txt" \
  -r "$PROJECT_ROOT/requirements-ui.txt"

if [[ -f "$PROJECT_ROOT/WhisperTube.command" ]]; then
  chmod u+x "$PROJECT_ROOT/WhisperTube.command"
fi

echo "Setup complete. Double-click WhisperTube.command in Finder, or run: ./scripts/launch_macos.sh"
