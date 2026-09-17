#!/usr/bin/env bash
# Sensors for the harness. Hooks call this script, and so can you.
cd "$(git rev-parse --show-toplevel)" || exit 1

case "${1:-}" in
  lint)
    if ! out="$(ruff check . 2>&1)"; then
      echo "$out" >&2
      echo "Fix each problem in the file. Do not add noqa comments and do not edit pyproject.toml." >&2
      exit 2
    fi
    ;;
  check)
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
