#!/usr/bin/env python3
"""Check every SKILL.md and the plugin manifest against this repo's rules. Standard library only.

Usage: python3 scripts/lint_frontmatter.py   (run from anywhere; exits 1 on any error)

Rules:
- frontmatter starts on line 1; `name` equals the directory name and is kebab-case
- `description` is present and the listing text stays under 1,536 characters
- body is at most 250 lines
- shipped skills (outside skills/in-progress/) are listed in plugin.json, and nothing else is
- skills in skills/in-progress/ carry `metadata: internal: true`
- user-invoked skills (USER_INVOKED below) set `disable-model-invocation: true`; others don't
- every shipped skill has at least 3 trigger and 3 near-miss eval cases under evals/<name>/
- every shipped skill is linked from README.md
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_INVOKED = {"mission-brief", "ship-oss", "launch-kit", "ask-thanatchon"}
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        return None, text
    end = text.index("\n---\n", 4)
    fm, body = text[4:end], text[end + 5:]
    data, parent = {}, None
    for line in fm.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^(\s*)([\w-]+):\s*(.*)$", line)
        if not m:
            continue
        indent, key, value = m.groups()
        value = value.strip().strip('"')
        if indent and parent:
            data[parent][key] = value
        else:
            data[key] = {} if value == "" else value
            parent = key if value == "" else None
    return data, body


def main():
    errors = []
    manifest = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))
    listed = {os.path.normpath(p) for p in manifest.get("skills", [])}
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read() if os.path.exists(os.path.join(ROOT, "README.md")) else ""
    shipped = set()

    for dirpath, _, files in os.walk(os.path.join(ROOT, "skills")):
        if "SKILL.md" not in files:
            continue
        rel = os.path.relpath(dirpath, ROOT)
        name = os.path.basename(dirpath)
        where = f"{rel}/SKILL.md"
        data, body = frontmatter(os.path.join(dirpath, "SKILL.md"))
        if data is None:
            errors.append(f"{where}: frontmatter must start on line 1")
            continue
        if data.get("name") != name:
            errors.append(f"{where}: name {data.get('name')!r} != directory {name!r}")
        if not KEBAB.match(name):
            errors.append(f"{where}: directory name is not kebab-case")
        desc = data.get("description", "")
        if not desc:
            errors.append(f"{where}: missing description")
        if len(desc) + len(data.get("when_to_use", "")) > 1536:
            errors.append(f"{where}: description + when_to_use over 1,536 characters")
        if body.count("\n") > 250:
            errors.append(f"{where}: body is {body.count(chr(10))} lines (max 250)")

        in_progress = rel.startswith(os.path.join("skills", "in-progress"))
        is_listed = os.path.normpath(rel) in listed
        if in_progress:
            if is_listed:
                errors.append(f"{where}: in-progress skill is listed in plugin.json")
            if str(data.get("metadata", {}).get("internal", "")).lower() != "true":
                errors.append(f"{where}: in-progress skill needs metadata.internal: true")
            continue

        shipped.add(name)
        if not is_listed:
            errors.append(f"{where}: shipped skill missing from plugin.json")
        dmi = str(data.get("disable-model-invocation", "")).lower() == "true"
        if (name in USER_INVOKED) != dmi:
            errors.append(f"{where}: disable-model-invocation must be {'true' if name in USER_INVOKED else 'unset'}")
        if readme and f"/{name}/SKILL.md" not in readme:
            errors.append(f"{where}: not linked from README.md")

        cases = os.path.join(ROOT, "evals", name)
        counts = {"trigger": 0, "near-miss": 0}
        for case in (os.listdir(cases) if os.path.isdir(cases) else []):
            p = os.path.join(cases, case, "prompt.md")
            if os.path.exists(p):
                tags = re.search(r"^tags:\s*\[(.*)\]", open(p, encoding="utf-8").read(), re.M)
                for t in (tags.group(1).split(",") if tags else []):
                    if t.strip() in counts:
                        counts[t.strip()] += 1
        for kind, n in counts.items():
            if n < 3:
                errors.append(f"evals/{name}: {n} {kind} cases (need at least 3)")

    for p in listed:
        if not os.path.exists(os.path.join(ROOT, p, "SKILL.md")):
            errors.append(f"plugin.json: {p} has no SKILL.md")

    for e in errors:
        print(f"error: {e}")
    print(f"{len(shipped)} shipped skills checked, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
