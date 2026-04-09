---
name: design-to-backlog
description: >
  This skill should be used when writing Jira tickets from design work,
  converting prototypes into backlog-ready stories, or when the user asks to
  "write up this design work", "create a ticket from this branch",
  "make this backlog-ready", "rewrite this ticket", or "write this up for
  the backlog". Produces outcome-focused tickets from design artifacts
  (branches, Figma files, Confluence specs) where the artifacts are the
  visual reference and the ticket describes what to build, not how.
  The team decides how to break down, assign, and implement.
---

# Design to Backlog Ticket

Convert design artifacts into backlog-ready Jira tickets. Design artifacts
are the visual spec — the ticket describes the desired end result. The team
decides everything else.

## Core Principle

**The ticket describes the outcome. The design artifacts show what it looks
like. The team decides everything else.**

The ticket doesn't tell eng how to implement, PM how to break down the work,
or QA how to test. It's a design artifact that's ready for grooming — the team
will groom it, size it, split it, assign it, and decide the approach.

## Workflow

### 1. Gather Design Artifacts

Before writing anything, understand what exists. Collect whatever is available:

**Design branches:**
- Read changelogs or design docs (`.design/changelog/`, `branch-log/`, or similar)
- Identify key files created or modified
- Note where the prototype cuts corners (accessibility gaps, hardcoded values,
  missing states)

**Figma files:**
- If a Figma URL is provided, use `get_design_context` or `get_screenshot` to
  capture the design intent
- Note component names, layout structure, and any annotations from the designer

**Confluence docs:**
- If a Confluence spec exists, fetch it with `getConfluencePage`
- Extract requirements, context, and any decisions already documented

**Other artifacts:**
- Slack threads, meeting notes, screenshots — anything the user provides as
  context for what the feature should be

Identify adjacent work that should be carved out as separate tickets.

**Design coverage checklist** — run through this for every artifact. If the
design covers it, capture it in the Feature Spec or AC. If it doesn't, flag
the gap so the team can discuss during grooming:

- **Interaction states** — hover, focus, active, disabled, loading, empty, error
- **Motion / animation** — duration, easing, trigger (or "none")
- **Responsive behavior** — reflow, truncate, hide, or scroll at breakpoints
- **Dark mode** — both themes covered, or only one?
- **Content edge cases** — long strings, zero state, single item, max limits
- **Accessibility** — focus order, contrast, reduced motion, screen reader
  announcements for dynamic content

### 2. Read the Existing Ticket (if any)

If a Jira ticket already exists, fetch it and compare against the artifacts:

- Is the title still accurate?
- Does the description match what was actually designed?
- Are there stale links or references?
- Is it written as a design changelog or as a feature spec?

### 3. Draft the Ticket

Structure the ticket using these sections (see `references/ticket-structure.md`
for detailed guidance on each):

1. **User Story** — Who benefits and why
2. **Design Reference** — Links to all available artifacts + framing
3. **Feature Specification** — What the feature is (placement, data, structure,
   behavior)
4. **Acceptance Criteria** — Observable outcomes grouped into 3-5 sections
5. **Out of Scope** — What NOT to build (with context for each)
6. **Known Constraints** — Gotchas, not solutions

### 4. Self-Review

Before presenting to the user, check:

- **Is it grooming-ready?** — Could a team pick this up in backlog refinement
  and have a productive conversation about it?
- **Is anything prescriptive?** — Remove specific CSS classes, hook names,
  library choices, architecture patterns, testing strategies, or breakdown
  suggestions. Use generic terms.
- **Is every AC an observable outcome?** — "Collapsed by default" is observable.
  "Should look good" is not.
- **Is the title accurate?** — Reflect what's actually being built, not an
  old working title.
- **Are follow-ups carved out?** — Anything adjacent but not in scope should
  be in Out of Scope.
- **Does it stay in its lane?** — The ticket describes the feature. It doesn't
  suggest how to split the work, what to test first, or which sprint to
  schedule it in.

## What to Avoid

### Implementation Prescriptions

| Prescriptive (avoid) | Outcome-focused (prefer) |
|---|---|
| "Use CSS grid with gridTemplateRows: 0fr/1fr" | "Collapsible with smooth animation" |
| "Implement with TanStack serverSide={false}" | "Client-side sorting" |
| "Build a useScanAggregateData hook" | "Derive aggregates from existing API response" |
| "Use inline SVG for the chevron" | (move to Known Constraints as a gotcha) |

**Exception — design system specifics are not prescriptions.** Token values,
DS components, and foundation patterns are design decisions that belong in the
ticket. There's a difference between telling eng how to code and telling the
team what the design is:

| Design spec (keep) | Implementation detail (remove) |
|---|---|
| "Use the `success` color token" | "Add `text-green-600`" |
| "Use the `Accordion` component from the DS" | "Use CSS grid with 0fr/1fr" |
| "Spacing follows the `space-4` token" | "Add `p-4` class" |
| "`border-radius` uses `radius-md` token" | "Add `rounded-md`" |

### Process Prescriptions

| Prescriptive (avoid) | Why |
|---|---|
| "Break this into 3 subtasks" | PM decides how to break down work |
| "This should be tested by..." | QA decides the test approach |
| "Estimate: 5 story points" | Team sizes during grooming |
| "Should be done in Sprint 12" | PM/team decides scheduling |
| "Deploy behind a feature flag" | Eng decides rollout strategy |

### Design Changelogs

The ticket is not a record of what changed during prototyping. Phrases like
"replaced the old X with Y" or "switched from amber to cyan" belong in the
design branch change logs, not the ticket. Write as if the reader has never
seen the old version.

### Non-Outcomes as AC

"Sparklines remain unchanged" is not an acceptance criterion. If something
should work a certain way, describe that behavior. If it's truly unchanged,
omit it.

## Jira Integration

Use the Atlassian MCP tools to read and update tickets:

- `getJiraIssue` — Fetch existing ticket for comparison
- `editJiraIssue` — Update title, description, and fields
- `createJiraIssue` — Create new tickets when needed

Set `contentFormat: "markdown"` when writing descriptions.

## Additional Resources

### Reference Files

- **`references/ticket-structure.md`** — Detailed guidance for each ticket
  section with examples of good and bad patterns