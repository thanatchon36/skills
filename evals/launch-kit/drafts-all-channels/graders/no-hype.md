---
type: regex
pattern: 'blazing|revolutionary|game.?chang|seamless|next-generation'
flags: i
match: not_contains
target: { source: file, path: launch/show-hn.md }
---
