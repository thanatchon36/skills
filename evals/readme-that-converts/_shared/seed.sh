#!/usr/bin/env bash
# Usage: seed.sh [bad-readme]  Copy the csvdiff fixture project into the eval workspace as a git repo.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$here"
while [ ! -d "$root/fixtures" ] && [ "$root" != "/" ]; do root="$(dirname "$root")"; done
cp -R "$root/fixtures/readme/csvdiff/." .
if [ "${1:-}" = "bad-readme" ]; then cp "$root/fixtures/readme/bad-README.md" README.md; fi
git init -q && git add -A && git -c user.name=eval -c user.email=eval@example.invalid commit -qm fixture
