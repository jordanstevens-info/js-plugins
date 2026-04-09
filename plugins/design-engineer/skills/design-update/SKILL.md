---
name: design-update
description: |
  This skill composes a copy-pasteable Slack update message summarizing work done
  in a session across any tools — without auto-publishing. It should be used when
  the user asks to "compose an update", "write a slack message", "draft a team update",
  "write a branch update", "design update", "write an update", "wrap up with an update",
  "share progress", "post an update", or any request to summarize recent work as a
  message for team visibility.
---

# Design Update

Compose a copy-pasteable Slack message summarizing all work done in the current
session. Gather context from every tool touched — git branches, Figma files,
Confluence pages, and other services — then compile into a single formatted update
the user can review, edit, and share with their team.

**Final authorship:** Never auto-publish via Slack MCP or any messaging API. Always
present the message inline in a fenced code block. The user owns what they share.

---

## Gathering Context

Before composing, check each source in order. Skip any that do not apply.

### Git

Run the following to collect branch context:

```bash
git branch --show-current
git remote get-url origin
```

Check for structured change logs (a per-branch session log convention used by some
workflow skills). Check in priority order:
- If `.design/changelog/` exists, read the most recent entry for this branch.
- If `.design/artifacts/` exists, scan for additional context.
- Else if `branch-log/changes/` exists, read the most recent entry for this branch.
- Else if `branch-log/artifacts/` exists, scan for additional context.
- If none exist, fall back to commit history:
  ```bash
  git log --oneline --no-merges HEAD...$(git merge-base HEAD main)
  ```

Derive the git hosting platform from the remote URL and construct branch/compare
URLs using standard GitHub or GitLab patterns.

### Figma

If Figma MCP tools were used during the session, note which files or frames were
modified. Extract Figma file URLs from tool call context or responses.

### Confluence

If Atlassian MCP tools were used, note which pages were created or updated. Extract
page URLs from tool responses.

### Other Services

If files were uploaded or created in SharePoint, OneDrive, Box, or other services,
note what was done and include any available URLs.

### Change Log References

If `.design/changelog/` entries contain external references (Jira tickets, Figma URLs,
Confluence pages), include them in the Links section. These are captured during
`design-engineer` sessions and save re-discovery.

### No External Tools

If only local file edits or git work occurred, the update focuses on git context only.

---

## Branch Prefix Mapping

Derive the emoji and category from the git branch prefix. When work spans multiple
tools and no single prefix fits, default to `:memo: Update`.

| Prefix | Emoji | Category |
|--------|-------|----------|
| `design/` | `:rainbow:` | Design |
| `feat/` | `:sparkles:` | Feature |
| `fix/` | `:wrench:` | Fix |
| `refactor/` | `:recycle:` | Refactor |
| `chore/` | `:broom:` | Chore |
| `docs/` | `:books:` | Docs |
| `plugin/` | `:claude:` | Plugin Dev |
| *(no prefix / unknown)* | `:memo:` | Update |

---

## Message Format

```
**:<emoji>: <Category> - <Feature Name> (AB-1234)**

**Notes**
- <bullet 1>
- <bullet 2>
- ...

**Links**
- Branch: <branch URL>
- Ticket: <jira URL>
- Figma: <figma URL>
- Confluence: <confluence URL>
- Log: <log URL>
```

Only include link lines for sources actually touched in the session. Omit any that
do not apply. The Links header is always `**Links**` — not platform-specific.

If a Jira ticket is associated with the work (found in `.design/changelog/` entries,
MCP tool activity, or user context), append the ticket key to the title in
parentheses and include a Ticket link. Omit both if no ticket exists.

---

## Composing Each Section

| Section | How to Derive |
|---------|---------------|
| Emoji + Category | From the branch prefix table above. For multi-tool sessions without a clear git prefix, use `:memo: Update`. |
| Feature Name | Human-readable name derived from the branch suffix (strip hyphens/underscores, title-case), plan title, or primary task description. If a Jira ticket key is known, append it in parentheses: `Feature Name (AX-1369)`. |
| Notes | Distill from change logs, git commits, and MCP tool activity into casual, first-person bullets. Focus on what changed and why it matters to the team — not implementation details. |
| Links | One line per source touched. Branch URL derived from the git remote using standard platform patterns. Figma and Confluence URLs taken from MCP tool responses. Log URL points to the most recent `.design/changelog/` or `branch-log/changes/` entry if one exists. |

---

## Notes Tone Guidance

- Write conversationally, not formally — "Added X" not "Implemented X functionality"
- Lead with what the team will see or notice, not how it was built
- Flag things that need discussion or feedback explicitly
- Include known limitations or follow-ups ("don't love X, should follow up with Y")
- Keep notes scannable — 3-7 bullets, no sub-bullets

---

## Fallbacks

| Scenario | Behavior |
|----------|----------|
| No `.design/changelog/` or `branch-log/changes/` directory | Derive notes from `git log` commits. Omit the Log link. |
| No git work (pure Figma/Confluence session) | Skip branch info entirely. Use `:memo: Update` as category. Derive notes from MCP tool activity. |
| Unknown git host (not GitHub or GitLab) | Ask the user for the base URL. |

---

## Output Rule

Present the composed message in a **single fenced code block** with no prose before
it, so it is immediately copy-pasteable.

Never send the message via Slack MCP, messaging APIs, or any auto-publish mechanism.
The user has final authorship — they review, edit, and decide when to share.

