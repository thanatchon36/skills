#!/usr/bin/env bash
# Maintainer dev loop only, not an installer. Symlink every skill in this repo (including
# in-progress drafts) into ~/.claude/skills and ~/.agents/skills, so edits here take effect
# without reinstalling. Users should install the plugin or use `npx skills add` instead.
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
for dest in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
  mkdir -p "$dest"
  find "$repo/skills" -name SKILL.md -print0 | while IFS= read -r -d '' f; do
    src="$(dirname "$f")"; target="$dest/$(basename "$src")"
    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "skip $target (exists and is not a symlink)" >&2; continue
    fi
    ln -sfn "$src" "$target" && echo "linked $(basename "$src") -> $dest"
  done
done
