---
type: regex
pattern: 'node:\s*\[[^\]]*\b18\b'
match: not_contains
target: { source: file, path: .github/workflows/ci.yml }
---
