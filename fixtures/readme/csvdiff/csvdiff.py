#!/usr/bin/env python3
"""Compare two CSV files by a key column and print added, removed, and changed rows."""

import argparse
import csv
import sys


def load(path, key):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if rows and key not in rows[0]:
        sys.exit(f"csvdiff: key column '{key}' not found in {path}")
    return {row[key]: row for row in rows}


def diff(old, new):
    added = [k for k in new if k not in old]
    removed = [k for k in old if k not in new]
    changed = []
    for k in old.keys() & new.keys():
        cols = [c for c in new[k] if old[k].get(c) != new[k][c]]
        if cols:
            changed.append((k, cols))
    return added, removed, sorted(changed)


def main(argv=None):
    p = argparse.ArgumentParser(prog="csvdiff", description=__doc__)
    p.add_argument("old")
    p.add_argument("new")
    p.add_argument("--key", default="id", help="column that identifies a row (default: id)")
    args = p.parse_args(argv)

    old, new = load(args.old, args.key), load(args.new, args.key)
    added, removed, changed = diff(old, new)
    for k in added:
        print(f"+ {args.key}={k}")
    for k in removed:
        print(f"- {args.key}={k}")
    for k, cols in changed:
        detail = ", ".join(f"{c}: {old[k][c]!r} -> {new[k][c]!r}" for c in cols)
        print(f"~ {args.key}={k}  {detail}")
    print(f"{len(added)} added, {len(removed)} removed, {len(changed)} changed")
    return 1 if (added or removed or changed) else 0


if __name__ == "__main__":
    sys.exit(main())
