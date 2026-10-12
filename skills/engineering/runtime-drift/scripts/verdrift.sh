#!/usr/bin/env bash
# Run a pinned verdrift release against a directory and print its JSON report.
#
# Usage: verdrift.sh [dir] [extra verdrift flags, e.g. --ignore 'examples/**']
#
# Exit codes:
#   0  no drift                1  drift found (JSON on stdout)
#   2  verdrift usage error
#   3  could not run: Node.js >= 22 missing, or the package could not be fetched.
#      The reason goes to stderr; fall back to references/manual-checklist.md.
set -uo pipefail

VERDRIFT_REF="v0.1.0"
dir="${1:-.}"
shift || true

fail() { echo "verdrift.sh: $*" >&2; exit 3; }

command -v node >/dev/null 2>&1 || fail "node not found on PATH (verdrift needs Node.js >= 22)"
command -v npx >/dev/null 2>&1 || fail "npx not found on PATH"
major="$(node -p 'process.versions.node.split(".")[0]')"
[ "$major" -ge 22 ] 2>/dev/null || fail "Node.js $(node --version) found, verdrift needs >= 22"

# The release tarball installs without git, which some sandboxes block.
out="$(npx --yes "https://codeload.github.com/thanatchon36/verdrift/tar.gz/refs/tags/${VERDRIFT_REF}" "$dir" --format json "$@")"
code=$?

# Exit 1 means either "drift found" or "npx failed"; only the first prints a JSON report.
if [ "$code" -le 1 ] && printf '%s' "$out" | node -e 'JSON.parse(require("fs").readFileSync(0, "utf8"))' 2>/dev/null; then
  printf '%s\n' "$out"
  exit "$code"
fi
[ "$code" -eq 2 ] && exit 2
fail "could not run verdrift ${VERDRIFT_REF} via npx (exit $code); see the npm output above"
