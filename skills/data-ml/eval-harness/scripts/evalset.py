#!/usr/bin/env python3
"""Check an eval set and compare two runs of it. Standard library only.

Usage:
  evalset.py check <cases.jsonl>
  evalset.py compare <baseline.jsonl> <candidate.jsonl>

cases.jsonl: one case per line, {"id", "input", "expected" or "criteria", "source", "tags"?}.
  source is one of: real, failure, synthetic.
results.jsonl: one result per line, {"id", "pass": true|false, "tags"?}.

check exits 1 on errors (bad JSON, missing fields, duplicate ids). compare exits 1 if the two runs
don't cover the same case ids, since a comparison over different cases means nothing.
"""

import json
import sys
from collections import Counter
from math import comb

SOURCES = ("real", "failure", "synthetic")
MIN_CASES = 30


def load(path):
    rows, errors = [], []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"{path}:{n}: invalid JSON ({e.msg})")
                continue
            if not isinstance(row, dict):
                errors.append(f"{path}:{n}: not a JSON object")
                continue
            row["_line"] = n
            rows.append(row)
    return rows, errors


def check(path):
    rows, errors = load(path)
    warnings = []
    ids = Counter(str(r.get("id")) for r in rows if r.get("id") is not None)
    for r in rows:
        where = f"{path}:{r['_line']}"
        if r.get("id") is None:
            errors.append(f"{where}: missing id")
        elif ids[str(r["id"])] > 1:
            errors.append(f"{where}: duplicate id {r['id']!r}")
        if not r.get("input"):
            errors.append(f"{where}: missing input")
        if not r.get("expected") and not r.get("criteria"):
            errors.append(f"{where}: needs expected or criteria")
        if r.get("source") not in SOURCES:
            errors.append(f"{where}: source must be one of {', '.join(SOURCES)}")
    sources = Counter(r.get("source") for r in rows)
    tags = Counter(t for r in rows for t in r.get("tags", []))
    if len(rows) < MIN_CASES:
        warnings.append(f"{len(rows)} cases: below {MIN_CASES}, one case moves the pass rate by "
                        f"{100 / max(len(rows), 1):.0f} points, so small differences are noise")
    if rows and sources["synthetic"] == len(rows):
        warnings.append("every case is synthetic: replace some with real inputs as soon as they exist")
    if rows and not sources["failure"]:
        warnings.append("no known-failure cases: add the inputs that prompted this change")
    for e in errors:
        print(f"error: {e}")
    for w in warnings:
        print(f"warning: {w}")
    print(f"{len(rows)} cases: " + ", ".join(f"{sources[s]} {s}" for s in SOURCES))
    if tags:
        print("tags: " + ", ".join(f"{t} {n}" for t, n in sorted(tags.items())))
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def sign_test(a, b):
    """Two-sided exact binomial test on the discordant pairs (a fixed vs b regressed)."""
    n = a + b
    if n == 0:
        return 1.0
    k = min(a, b)
    p = 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(p, 1.0)


def compare(base_path, cand_path):
    base, e1 = load(base_path)
    cand, e2 = load(cand_path)
    errors = e1 + e2
    b = {str(r["id"]): r for r in base if "id" in r}
    c = {str(r["id"]): r for r in cand if "id" in r}
    for r in base + cand:
        if not isinstance(r.get("pass"), bool):
            errors.append(f"id {r.get('id')!r}: pass must be true or false")
    only_b, only_c = sorted(set(b) - set(c)), sorted(set(c) - set(b))
    if only_b:
        errors.append(f"only in baseline: {', '.join(only_b)}")
    if only_c:
        errors.append(f"only in candidate: {', '.join(only_c)}")
    if errors:
        for e in errors:
            print(f"error: {e}")
        return 1

    ids = sorted(b)
    n = len(ids)
    bp = sum(b[i]["pass"] for i in ids)
    cp = sum(c[i]["pass"] for i in ids)
    fixed = [i for i in ids if not b[i]["pass"] and c[i]["pass"]]
    regressed = [i for i in ids if b[i]["pass"] and not c[i]["pass"]]
    p = sign_test(len(fixed), len(regressed))

    print(f"Baseline: {bp}/{n} ({100 * bp / n:.1f}%)")
    print(f"Candidate: {cp}/{n} ({100 * cp / n:.1f}%)")
    print(f"Delta: {100 * (cp - bp) / n:+.1f} points")
    print(f"Flips: {len(fixed)} fixed, {len(regressed)} regressed (sign test p={p:.2f})")
    if fixed:
        print("fixed: " + ", ".join(fixed))
    if regressed:
        print("regressed: " + ", ".join(regressed))
    tags = sorted({t for i in ids for t in b[i].get("tags", []) + c[i].get("tags", [])})
    for t in tags:
        tagged = [i for i in ids if t in b[i].get("tags", []) + c[i].get("tags", [])]
        tb = sum(b[i]["pass"] for i in tagged)
        tc = sum(c[i]["pass"] for i in tagged)
        print(f"  tag {t}: {tb}/{len(tagged)} -> {tc}/{len(tagged)}")
    return 0


def main(argv):
    if len(argv) == 3 and argv[1] == "check":
        return check(argv[2])
    if len(argv) == 4 and argv[1] == "compare":
        return compare(argv[2], argv[3])
    print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
