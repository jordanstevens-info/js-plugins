---
name: design-to-mr
description: >-
  Cut a clean merge request branch from a design branch. Use when the user
  wants to submit design work for code review. Triggers on "cut MR",
  "create merge request", "submit for review", "branch for review",
  "ship this", "push for review". Presents scope options (code only,
  code + artifacts, everything), drafts an MR title and description for
  user approval, pushes the branch, and provides a pre-filled MR link.
---

# Design to Merge Request

Cut a clean branch from a `design/` branch for merge request submission.
The design branch stays intact — this creates a delivery branch with only
the files the user wants reviewed.

## Workflow

### 1. Read Context

- Read `.design/README.md` to understand the project and branch scope
- Read `.design/changelog/` entries to understand what was built and what was deferred
- Collect external references from change log entries (Jira tickets, Figma URLs,
  Confluence pages) — include these in the MR description
- Run `git diff --stat main..<design-branch>` to see all changed files

### 2. Choose Scope

Present three options to the user:

- **Code only** — production files only, no `.design/` directory. Cleanest MR
  for teams that treat `.design/` as scaffolding.
- **Code + selected artifacts** — production files plus user-selected `.design/`
  files (e.g., change log, design-system.md). Useful when reviewers want context.
- **Everything** — all files from the design branch including `.design/`. For
  internal teams that want full visibility.

Wait for the user to choose before proceeding.

### 3. Cut Branch

1. Identify the primary branch (`main` or `master`)
2. `git checkout <primary> && git checkout -b <branch-name>`
3. `git checkout <design-branch> -- <selected files>` for additions and modifications
4. `git diff --diff-filter=D --name-only <primary>..<design-branch>` to find deletions
5. `git rm` any deleted files that fall within the selected scope
6. Commit with a descriptive message summarizing the design work

### 4. Review Before Push

Present to the user for approval before pushing:

- **MR title** — short, under 70 characters
- **MR description** — structured markdown with:
  - Summary (what changed and why)
  - What changed (new/modified/removed files grouped by area)
  - Design decisions (key choices and rationale)
  - Test plan (verification steps)
- **File list** — all files included in the branch

Format the description as a fenced code block so the user can copy-paste
directly into the MR form. Wait for approval or edits before pushing.

### 5. Push and Link

Push the branch with `-u`. Detect the platform from `git remote get-url origin`
and construct a pre-filled new MR URL:

**GitLab:**
```
<remote>/-/merge_requests/new?merge_request[source_branch]=<branch>&merge_request[title]=<url-encoded-title>
```

**GitHub:**
```
<remote>/compare/main...<branch>?expand=1&title=<url-encoded-title>
```

Present the link so the user can click to open the MR form with the branch
and title pre-filled, then paste the description. Stop.

## Rules

- The design branch stays intact — never modify, rebase, or delete it
- Do not create MRs directly — push the branch and provide the link
- Do not suggest backlog tickets, follow-up work, or next steps
- Ask before including any `.design/tmp/` contents
- If the design branch has no `.design/changelog/` entries, flag this and ask
  the user for context before drafting the MR description
