---
name: launch-kit
description: Draft launch posts for a repo (Show HN, X thread, LinkedIn, Reddit, Thai developer communities) plus GitHub topics and a social-preview brief, written to launch/. Never posts anything.
disable-model-invocation: true
argument-hint: "[repo path or owner/name]"
---

# launch-kit

Write honest, channel-appropriate launch drafts for an open-source repo and save them to `launch/`
for the user to edit and post themselves.

## When NOT to use

- The repo isn't public yet, or doesn't install from its public source. Launch after it does: a
  post that sends people to a broken install burns the launch.
- Paid ads, press releases, or email campaigns.
- Posting. This skill only drafts. It never posts, schedules, or submits anything.

## Workflow

Do the steps in order. Do not skip ahead.

### 1. Gather facts

Read the README, `CHANGELOG.md`, the license, the manifests, recent commits, and the release. If
the repo is on GitHub and `gh` is available, run
`gh repo view <repo> --json name,description,url,repositoryTopics,stargazerCount,latestRelease`.
Write down:

- The problem in the user's words (from the README's first sentence).
- The install command, and whether it was verified (look for "(untested)" labels).
- One real example: a command and its real output, from the README or from running it now.
- Limitations, straight from the README.
- The author's real links, from the repo or the user. Never invent a handle or URL.

### 2. Gate: launch readiness

Check each item and report the result:

- [ ] The repo is public, and the install works from the public source (run it in a scratch
      directory if possible).
- [ ] The README's first screen shows the problem, the install, and a real example.
- [ ] CI is green on the default branch.
- [ ] A license file exists.

If any item fails, list it and ask whether to continue. Drafts for a repo that isn't ready get a
`NOT READY:` line at the top of every file.

### 3. Draft each channel

Follow `references/channels.md` for each channel's norms. Write each file in `launch/`:

| File | Contents |
| --- | --- |
| `launch/show-hn.md` | title, URL, and the first comment |
| `launch/x-thread.md` | 3 to 6 numbered posts, each within the character limit |
| `launch/linkedin.md` | one post, 120 to 250 words |
| `launch/reddit.md` | 2 or 3 subreddit suggestions, each with a reason, its rule to check, and a tailored post |
| `launch/thai-communities.md` | venue suggestions, plus a post in natural Thai with code and commands in English |
| `launch/github-metadata.md` | description, 5 to 15 topics, and a `gh repo edit` command to apply them (not run) |
| `launch/social-preview.md` | a brief for the 1280×640 image |
| `launch/README.md` | a checklist with the posting order, the channel rules to re-check, and what to watch for in replies |

Every draft uses the same facts from step 1. Adapt the wording to each channel; don't paste one
text everywhere.

### 4. Self-check

For every file, verify:

- No claim the repo can't back up (speed, users, stars, adoption). Remove it or add the evidence.
- No superlatives or hype words, and no exclamation-mark marketing.
- Install commands and output are copied exactly from step 1.
- The author is disclosed as the author where a channel expects it (Reddit, HN).
- Links are real and point to the public repo.

### 5. Report

List the files written, the readiness result, and anything the user must fill in (`TBD:` items
such as their own handles). Remind them that nothing was posted.

## Output contract

- The eight files above, under `launch/` at the repo root (or the path the user gives).
- A final message: `Drafts in launch/ (<n> files). Readiness: <ok | NOT READY: ...>. TBD: <list>.
  Nothing was posted.`

## Operating rules

- Never post, schedule, submit, or call any social or forum API, even if credentials are present.
- Never invent metrics, testimonials, quotes, or links. Leave `TBD:` instead.
- Never suggest vote manipulation, sockpuppets, or mass cross-posting.
- The drafts promote the user's repo only. Don't add links to this skill or its author.

## Done-check

- [ ] All eight files exist, and each passes the step 4 self-check.
- [ ] The readiness gate result is stated.
- [ ] Every number and link in the drafts traces back to the repo or the user.
- [ ] Nothing was posted.
