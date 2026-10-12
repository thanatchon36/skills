#!/usr/bin/env bash
# Copy the drifted fixture into the empty eval workspace as a git repo.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$here"
while [ ! -d "$root/fixtures" ] && [ "$root" != "/" ]; do root="$(dirname "$root")"; done
cp -R "$root/fixtures/runtime-drift/drifted/." .
git init -q && git add -A && git -c user.name=eval -c user.email=eval@example.invalid commit -qm fixture
