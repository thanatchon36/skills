---
type: regex
pattern: '10,?000 (daily )?users|10k (daily )?users'
flags: i
match: not_contains
target: { source: file, path: launch/linkedin.md }
---
