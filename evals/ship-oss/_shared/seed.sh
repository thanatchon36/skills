#!/usr/bin/env bash
# Usage: seed.sh <fixture-name>  Copy fixtures/ship-oss/<name> into the eval workspace as a git repo.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$here"
while [ ! -d "$root/fixtures" ] && [ "$root" != "/" ]; do root="$(dirname "$root")"; done
cp -R "$root/fixtures/ship-oss/$1/." .
git init -q -b main && git add -A && git -c user.name=eval -c user.email=eval@example.invalid commit -qm "initial"
