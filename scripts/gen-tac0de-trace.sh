#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

INPUT_JSON="$ROOT_DIR/assets/tac0de/example.input.json"
OUTPUT_JSON="$ROOT_DIR/assets/tac0de/example.trace.json"

if command -v tac0de-cascade >/dev/null 2>&1; then
  tac0de-cascade trace "$INPUT_JSON" > "$OUTPUT_JSON"
elif [[ -n "${TAC0DE_CASCADE_MANIFEST:-}" ]]; then
  cargo run --quiet --manifest-path "$TAC0DE_CASCADE_MANIFEST" -- trace "$INPUT_JSON" > "$OUTPUT_JSON"
else
  echo "tac0de-cascade not found on PATH." >&2
  echo "Install it, or set TAC0DE_CASCADE_MANIFEST to the Cargo.toml path for tac0de-cascade." >&2
  exit 1
fi

printf "Generated %s\n" "$OUTPUT_JSON"
