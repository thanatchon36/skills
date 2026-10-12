#!/usr/bin/env python3
"""List lines worth checking for data leakage in Python ML code.

Usage: python3 find_candidates.py <file-or-dir> [...]

Prints one line per candidate: path:line  KIND  [before-split]  code
This is a reading aid, not a verdict. Every candidate must be confirmed by tracing the data flow,
and leaks it can't see (a feature defined in SQL, a split in another module) still need reading.
Standard library only.
"""

import os
import re
import sys

SPLIT = re.compile(
    r"\b(train_test_split|randomSplit|KFold|StratifiedKFold|GroupKFold|TimeSeriesSplit"
    r"|ShuffleSplit|cross_val_score|cross_validate|GridSearchCV|RandomizedSearchCV)\b"
)
CHECKS = [
    ("FIT", re.compile(r"\.(fit|fit_transform|fit_resample)\s*\(")),
    ("TARGET-AGG", re.compile(r"groupby\(.*\)\s*\[.*\]\s*\.transform\(|\.agg\(|TargetEncoder|target_encod", re.I)),
    ("FUTURE-WINDOW", re.compile(r"center\s*=\s*True|\.shift\(\s*-\d|bfill|backfill|method\s*=\s*['\"]b")),
    ("SHUFFLE", re.compile(r"shuffle\s*=\s*True|\.sample\(\s*frac\s*=\s*1")),
    ("TEST-SCORE", re.compile(r"\b\w+\(\s*y_test\b|\.score\(\s*X_test|evaluate\(.*test")),
    ("POST-OUTCOME-NAME", re.compile(
        r"['\"]\w*(after|post|future|next|outcome|resolved|refund|cancel|chargeback|final)\w*['\"]", re.I)),
    ("DEDUP", re.compile(r"drop_duplicates|dropDuplicates|distinct\(\)")),
]


def python_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {"venv", ".venv", "node_modules", "__pycache__"}]
                for f in sorted(files):
                    if f.endswith(".py"):
                        yield os.path.join(root, f)
        elif p.endswith(".py"):
            yield p


def scan(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    first_split = next((i for i, l in enumerate(lines, 1) if SPLIT.search(l) and not l.lstrip().startswith(("#", "from ", "import "))), None)
    out = []
    for i, line in enumerate(lines, 1):
        code = line.strip()
        if not code or code.startswith(("#", "from ", "import ")):
            continue
        if SPLIT.search(code):
            out.append((i, "SPLIT", "", code))
        for kind, rx in CHECKS:
            if rx.search(code):
                before = "before-split" if first_split and i < first_split and kind in {"FIT", "TARGET-AGG"} else ""
                out.append((i, kind, before, code))
    if first_split is None:
        out.insert(0, (0, "NO-SPLIT-FOUND", "", "no split call in this file; find where the split happens"))
    return out


def main(argv):
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    for path in python_files(argv):
        for line, kind, before, code in scan(path):
            print(f"{path}:{line}\t{kind}\t{before}\t{code[:120]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
