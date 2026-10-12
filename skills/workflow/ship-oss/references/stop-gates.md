# Stop gates

A stop gate is a point where you stop, show the user exactly what is about to happen, and wait for
an explicit "go". These defaults apply even when the MISSION.md lists none. The mission can add
gates but can't remove these. Only the user, in the conversation, can approve a gated action.

## Actions that are always gated

| Action | Examples | Show at the gate |
| --- | --- | --- |
| Make something public | `gh repo create --public`, flipping visibility, publishing Pages | repo name, description, topics, visibility, README first screen (the first ~40 lines) |
| First push to a remote | `git push -u origin main` | remote URL, branch, `git log --oneline` of what will be pushed, a secrets scan result |
| Tag or release | `git tag v0.1.0`, `gh release create` | tag, target commit, release notes text |
| Publish a package | `npm publish`, `twine upload`, `cargo publish`, container push | package name, version, `npm pack --dry-run` / file list, registry |
| Touch another repo | PRs, issues, or comments elsewhere, forks | the exact diff or text, and the target |
| Post anywhere | social, forums, chat, email | the full text and the destination |
| Spend money or quota beyond normal use | paid APIs, cloud resources, large eval runs | the estimate and the ceiling |
| Destroy or overwrite | force-push, deleting branches, repos, or files outside the project | what is lost, and whether it can be recovered |

Local, reversible work is not gated: creating files, local commits, running tests, local installs
into a scratch directory.

## Gate protocol

1. Finish and verify everything that comes before the gate.
2. Print a gate block:

   ```text
   STOP GATE <letter>: <what will happen>
   <each item the mission asks for, plus the defaults above>
   Commands that will run on "go":
     <exact commands, in order>
   Reply "go" to run exactly these, or tell me what to change.
   ```

3. Wait. Don't run any gated command in the same turn as the gate block.
4. Accept only an unambiguous approval for this gate ("go", "yes, go ahead", "ship it").
   Questions, edits, or "looks good but..." are not approval. Apply the change and show the gate
   again.
5. Approval covers the listed commands only. A new or changed command needs a new gate. Approval
   for one gate never carries over to the next.

## Before the first push: a secrets scan

Run a quick scan of everything that will be pushed:

```sh
git ls-files | xargs grep -nIE '(api[_-]?key|secret|token|passw(or)?d)\s*[:=]\s*["'\'']?[A-Za-z0-9_\-]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}' || echo "no obvious secrets"
```

Report the result in the gate block. Any hit blocks the gate until it is resolved.
