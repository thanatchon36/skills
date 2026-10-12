#!/usr/bin/env bash
# Copy the csvdiff fixture plus a finished README into the eval workspace as a git repo.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$here"
while [ ! -d "$root/fixtures" ] && [ "$root" != "/" ]; do root="$(dirname "$root")"; done
cp -R "$root/fixtures/readme/csvdiff/." .
cp "$root/fixtures/launch/README.md" README.md
git init -q -b main && git add -A && git -c user.name=eval -c user.email=eval@example.invalid commit -qm "v0.3.0"
