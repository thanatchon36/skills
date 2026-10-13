#!/usr/bin/env bash
# Usage: seed.sh <support-bot|results|file>...  Copy eval-harness fixtures into the eval workspace.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$here"
while [ ! -d "$root/fixtures" ] && [ "$root" != "/" ]; do root="$(dirname "$root")"; done
src="$root/fixtures/eval-harness"
for what in "$@"; do
  case "$what" in
    support-bot) cp -R "$src/support-bot/." . ;;
    results) mkdir -p results && cp "$src/results/"*.jsonl results/ ;;
    *) cp "$src/snippets/$what" . ;;
  esac
done
