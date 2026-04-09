---
name: design-engineer
description: >-
  This skill manages the cross-repo design engineering workflow for implementing
  designs on a dedicated design/ branch. It should be used when implementing
  designs from Figma, building components, working with design tokens,
  doing Figma-to-code translation, running visual QA, performing accessibility
  checks, working on the design system, building responsive layouts, or any
  design engineering task. Triggers on "implement design", "build component",
  "Figma to code", "design tokens", "design system", "visual QA",
  "accessibility check", "implement from Figma", "match the design",
  "component spec", "responsive layout", "spacing", "typography".
---

# Design Engineering Workflow

Implement designs on a `design/` branch. Bootstrap `.design/` for portable
context per repo.

## Shortcuts

| Trigger | Action |
|---------|--------|
| Start, Preflight, Prime | `references/bootstrap.md` (if needed) + steps 1-2, report readiness |
| Checkpoint | Verify build + lint pass → commit + changelog entry + update Current State, keep working |
| Design Review, Design QA | Step 5 only: verification checklist |
| Status | Read changelog + README, `git status`, check main divergence, report |
| Shutdown, Wrap-Up, Finish, Retro | Run Shutdown Procedure, report against Exit Criteria |

## Branching

1. Create `design/<feature-name>` from primary branch
2. All work on this branch — NEVER commit to primary branch directly
3. Subagents MUST use `isolation: "worktree"`

## Scope Boundary

This skill ends at commit and push. NEVER:
- Create PRs, MRs, or merge requests
- Suggest creating PRs, MRs, or merge requests
- Suggest backlog tickets or next steps beyond the current task
- Reference MR/PR workflows in output

The user initiates downstream skills (`design-to-mr`, `design-to-backlog`,
`design-update`) separately when ready.

## Principles

- `.design/` is branch-scoped portable context — it travels with the branch
- Build clean — use spikes as reference, do not migrate spike code forward
- Do not duplicate product-thinking docs inside implementation files
- Visual fidelity and accessibility are exit gates, not polish steps

## Workflow

If `.design/` does not exist: run `references/bootstrap.md` first.
If `.design/` exists: run migration check, read `.design/README.md`, start at step 1.

**Migration** — rename silently if old conventions found:

| Old | New |
|-----|-----|
| `.design/CLAUDE.md` | `.design/README.md` |
| `.design/changes/` | `.design/changelog/` |

Use `git mv`. Log in next changelog entry.

### 1. Inspect

- Read `.design/README.md` for knowledge routing
- Read `.design/changelog/` for prior session context
- Locate existing components, tokens, conventions
- If Figma MCP available: inspect target file/frame before coding

### 2. Scope

- Check phase/milestone in architecture docs or `.design/knowledge/`
- Check latest status in `.design/changelog/`
- Confirm what is in scope for this branch
- Do NOT pull future-phase work unless trivially small and directly unblocking

**On Status shortcut**, also run:
```bash
git status
git fetch origin && git rev-list HEAD..origin/main --count
```
If main is ahead: report count, flag rebase may be needed. Do NOT rebase automatically.

### 3. Landing Zone

- Prefer existing modules/files over new ones
- Prefer extending existing components over creating new ones
- Only create new structure when architecture requires it and scope demands it
- Use `.design/artifacts/` for prototypes, spikes, and exploratory work worth keeping
- Use `.design/tmp/` for throwaway scratch files only (gitignored)

### 4. Source-of-Truth Layer

Work bottom-up through the design dependency stack:

1. Design tokens (colors, spacing, typography, elevation, motion)
2. Base/primitive components (buttons, inputs, icons, badges)
3. Composed components (cards, forms, navigation, modals)
4. Page layouts/views

NEVER hardcode raw color, spacing, or font values when a token exists.
If a needed token is missing: flag it, document in `.design/artifacts/`.

### 5. Verify and Document

**Verify** against design spec:
- Visual match: spacing, color, typography, alignment
- Responsive: key breakpoints
- Accessibility: contrast, focus order, semantic HTML, ARIA
- Dark mode / theme variants (if applicable)
- Component isolation: works standalone
- Build/test passes (see `.design/README.md` for commands)

**Output a numbered verification checklist.** Each item: exact command or action
(copy-pasteable) + expected outcome. No prose. Tailor to: browser inspection,
DevTools token checks, keyboard nav, Figma overlay.

**Write changelog entry** — dated, in `.design/changelog/` (see
`templates/changelog-entry.md`):
- Files, components, routes touched
- What changed
- What was deferred
- External references (Jira, Figma, Confluence) — downstream skills read these

**Graduate durable patterns.** Ask: "Would a future agent or developer on a
different branch benefit from this?" If yes, promote:
- `design-system.md` — component patterns, token conventions, icon strategies
- `standards.md` — process decisions, tooling conventions

Graduate: "Use FgtTooltip over Flowbite Tooltip", "Inline SVGs for Heroicons
due to TS7016", "Commit format: type(scope): description".
Do NOT graduate: one-time design choices, implementation details, session preferences.

**Update Current State** in `.design/README.md` on Checkpoint and Shutdown.
Cumulative 1-3 line summary of total branch progress. Replace, do not append.

Update `.design/knowledge/` if new durable patterns established.
Save artifacts to `.design/artifacts/`.
NEVER remove from `.design/tmp/` without user confirmation.

## Rules

NEVER do these unless the task explicitly requires it:
- Refactor broadly or add future-phase complexity
- Introduce new dependencies without discussion
- Commit to primary branch
- Remove existing tests or checks
- Deviate from Figma specs without flagging
- Hardcode raw color/spacing/font values — use tokens
- Override component library defaults without justification
- Skip accessibility verification
- Commit `.design/tmp/` contents
- Create empty directories — create `changelog/`, `artifacts/`, `tmp/` on first use
- Leave dead code, commented-out blocks, or unused imports behind — when new code replaces old code, remove the old code completely
- Rewrite a file from scratch — prefer targeted edits. Never rewrite a full file without flagging it first.
- Fix, refactor, or improve code you encounter unless it is blocking the current task
- Create a new function, type, or utility without searching the repo first — if it exists, use it

**Commit sizing:** prefer small commits scoped to a single logical change. Use the Checkpoint shortcut to commit incrementally during the session — this protects work if the session is interrupted. Squash-on-merge handles the clean history.

**Reading strategy:** understand file structure before reading implementations. Do not rely on a single linear pass — ensure you have full understanding of the file regardless of length.

**Build early, build often:** run the build after any structural change. Do not stack work on broken code.

**No commit without green build:** run the project's build and lint commands (see `.design/README.md`) and confirm they pass BEFORE every commit — Checkpoint or Shutdown. This is a hard gate: if build or lint fails, fix first, then commit.

**Code volume check:** if you are adding significantly more lines than you are removing, stop and question the approach. Prefer reusing and extending existing code over writing net-new code. High line counts usually signal duplication, over-engineering, or failure to remove what was replaced.

**Decision rules:**
- Repo has a pattern → adapt it, do not invent a new one
- Change touches production code → least invasive path
- Feature can be deferred without blocking scope → defer
- Two valid paths → choose the one that preserves optionality
- Uncertain about direction → consult `.design/README.md` knowledge sources
- Uncertain about visual intent → consult Figma before guessing
- Token missing → flag, do not hardcode
- Component exists in library → extend/compose, do not rebuild
- Repo has knowledge files → reference them, do not duplicate into `.design/knowledge/`
- Search the repo before creating anything new — functions, types, utilities, components

## Shutdown Procedure

### Phase 1 — Verify (loop until green)

Run ALL of these checks. If ANY fail, fix and re-run ALL from the top.
Do NOT proceed to Phase 2 until every check passes.

1. **Build** — run the project's build command. MUST pass.
2. **Lint** — run the project's lint command. MUST pass.
3. **Visual match** — spacing, color, typography, alignment vs design spec
4. **Responsive** — key breakpoints
5. **Accessibility** — contrast, focus order, semantic HTML, ARIA
6. **Component isolation** — works standalone
7. **No dead code** — no commented-out blocks, unused imports, or leftover spike code

Output a numbered pass/fail checklist. On ANY failure: fix, then restart from check 1.

### Phase 2 — Document (once, after Phase 1 is green)

8. **Changelog** — write dated `.design/changelog/` entry (changed, deferred, references)
9. **Graduate** — promote durable patterns to `design-system.md` or `standards.md`
10. **Current State** — replace `## Current State` in `.design/README.md` with cumulative summary

### Phase 3 — Ship (once, after Phase 2)

11. **Commit** — stage and commit with descriptive message
12. **Push** — if a git remote exists, push design branch to remote; otherwise skip silently
13. **Report** — show `git diff main..HEAD` for full session overview, then report doneness against each Exit Criteria item; flag unsatisfied items

## Exit Criteria

ALL must be true:

1. Requested work functions end to end
2. Change is scoped — no unrelated modifications
3. Visual output matches design spec (spacing, color, typography, alignment)
4. Accessibility basics pass (contrast, focus order, semantic HTML, ARIA)
5. `.design/changelog/` entry documents changes and deferrals
6. `## Current State` in `.design/README.md` reflects cumulative branch progress
7. Durable patterns graduated to knowledge files where appropriate
8. Next step is clearer than before

Items 3 and 4 are hard gates. Do not mark work done until verified.

## References

- `references/bootstrap.md` — one-time repo setup: branch, detection, `.design/` creation, interview
