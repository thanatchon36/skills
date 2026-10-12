#!/usr/bin/env bash
# List every SKILL.md in the repo, marking which ones the plugin ships.
set -euo pipefail
cd "$(dirname "$0")/.."
find skills -name SKILL.md | sort | while read -r f; do
  d="./$(dirname "$f")"
  if grep -q "\"$d\"" .claude-plugin/plugin.json; then echo "shipped      $f"; else echo "not shipped  $f"; fi
done
