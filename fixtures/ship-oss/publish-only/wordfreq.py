#!/usr/bin/env python3
"""Print the most common words in a text file."""

import collections
import re
import sys


def top_words(text, n=10):
    words = re.findall(r"[a-z']+", text.lower())
    return collections.Counter(words).most_common(n)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: wordfreq.py <file>")
    with open(sys.argv[1], encoding="utf-8") as fh:
        for word, count in top_words(fh.read()):
            print(f"{count:6d}  {word}")
