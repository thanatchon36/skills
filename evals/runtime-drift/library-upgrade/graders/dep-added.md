---
type: regex
pattern: '"yaml"\s*:\s*"[\^~]?2\.9\.1"'
target: { source: file, path: package.json }
---
