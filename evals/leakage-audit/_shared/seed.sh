#!/usr/bin/env bash
# Usage: seed.sh <leaky|clean> [file...]  Copy fixture pipelines into the eval workspace root.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$here"
while [ ! -d "$root/fixtures" ] && [ "$root" != "/" ]; do root="$(dirname "$root")"; done
src="$root/fixtures/leakage/$1"; shift
if [ "$#" -eq 0 ]; then cp "$src"/*.py .; else for f in "$@"; do cp "$src/$f" .; done; fi
