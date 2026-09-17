#!/usr/bin/env bash
# Sensors for the harness. Hooks call this script, and so can you.
cd "$(git rev-parse --show-toplevel)" || exit 1

# A missing tool is your problem and not Claude's, so exit 1. Claude Code shows that to you only.
need() {
  for tool in "$@"; do
    if ! command -v "$tool" >/dev/null; then
      echo "$tool is not on the PATH. Activate the virtual environment, then start claude again." >&2
      exit 1
    fi
  done
}

case "${1:-}" in
  lint)
    need ruff
    if ! out="$(ruff check . 2>&1)"; then
      echo "$out" >&2
      echo "Fix each problem in the file. Do not add noqa comments and do not edit pyproject.toml." >&2
      exit 2
    fi
    ;;
  check)
    need pyright pytest
    if ! out="$(pyright 2>&1 && pytest -q 2>&1)"; then
      echo "$out" | tail -n 40 >&2
      echo "Fix the code, not the tests, then finish." >&2
      exit 2
    fi
    echo "check passed, pyright and pytest" >&2
    ;;
  *)
    echo "usage: sensors.sh lint | check" >&2
    exit 1
    ;;
esac
