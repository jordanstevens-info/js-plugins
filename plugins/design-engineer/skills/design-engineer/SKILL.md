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

Move design work forward in small, safe steps on a `design/` branch. This skill
bootstraps a `.design/` context directory on each repo so it has the knowledge it
needs — regardless of whether the repo has existing documentation. All templates
are bundled in `templates/`.

## Working Style

- Prefer the smallest useful increment
- Reuse existing repo conventions, components, and tokens
- Keep new work isolated on a `design/` branch
- Avoid broad refactors unless they directly unblock the current step
- Leave clear extension points instead of building future phases early

## Trigger Shortcuts

- **Preflight, Prime** — Run bootstrap (if needed) + steps 1–2, report readiness
- **Checkpoint** — Commit current work + write `.design/changes/` entry, keep working
- **Design Review, Design QA** — Run steps 5–6 only: visual QA, accessibility, token compliance, verification checklist
- **Status** — Read `.design/changes/` and `.design/CLAUDE.md`, report what's done and what's pending
- **Shutdown, Wrap-Up, Finish, Retro** — Commit, push, update change log, step 7, report doneness

## Workflow

If `.design/` does not exist, run the **Bootstrap** section (bottom of this file)
before starting step 1. If `.design/` already exists, read `.design/CLAUDE.md` to
re-prime and begin at step 1.

### 1. Inspect Before Changing

Read before writing. Locate existing patterns, components, and tokens before adding
new ones.

- Read knowledge sources via routing in `.design/CLAUDE.md`
- Read `.design/changes/` for prior session context on this branch
- Locate existing components, design tokens, and conventions in the repo
- If Figma MCP is available, inspect the relevant file or frame before coding

### 2. Know Your Scope

Check the current phase or milestone in architecture docs (repo's own or
`.design/knowledge/`). Check latest status in `.design/changes/`.

Confirm what is in scope for this design branch. Do not pull work from future
phases unless it is trivially small and directly unblocking.

### 3. Pick the Smallest Landing Zone

Prefer existing modules and files if the work fits there. For design work: prefer
extending existing components over creating new ones.

Only create new structure when the architecture calls for it and the current scope
requires it. Use `.design/tmp/` for exploratory work that isn't ready for the repo
proper.

### 4. Start from the Source-of-Truth Layer

Work from the bottom of the design dependency stack upward:

1. **Design tokens** — colors, spacing, typography, elevation, motion
2. **Base / primitive components** — buttons, inputs, icons, badges
3. **Composed components** — cards, forms, navigation, modals
4. **Page layouts / views** — full pages assembled from composed components

If tokens exist in the repo, use them. Never hardcode raw color, spacing, or font
values when a token exists. If a token doesn't exist for a needed value, flag it
and document in `.design/artifacts/` — do not silently hardcode.

### 5. Verify Before Stopping

- Verify visual match against the Figma spec (spacing, color, typography, alignment)
- Test responsive behavior at key breakpoints
- Verify accessibility basics: contrast ratio, focus order, semantic HTML, ARIA
- Test dark mode / theme variants if applicable
- Verify component isolation (works standalone, not dependent on page context)
- Run the build/test command (see repo `CLAUDE.md` or `.design/CLAUDE.md` for commands)

### 6. Present Verification Checklist

After completing a task and before committing, output a numbered verification
checklist. For each step, include:

- The exact command to run or action to take (copy-pasteable)
- What to expect (expected output, visual result, or behavior)

Tailor to design work:

- Browser inspection steps (specific viewports, interactions, hover/focus states)
- DevTools checks (computed styles match tokens, no hardcoded values in output)
- Accessibility audit steps (keyboard navigation, screen reader, contrast check)
- Figma overlay comparison if relevant

Keep it concise — no prose, just steps and expected outcomes.

### 7. Document the Delta

Write a dated entry in `.design/changes/` covering:

- Where the work lives (files, components, routes)
- What was added or changed
- What was intentionally deferred

Update `.design/knowledge/` files if new durable patterns were established (new
tokens, new component conventions, new naming patterns).

Save relevant artifacts (specs, screenshots, token maps) to `.design/artifacts/`.

Ask the user before removing anything from `.design/tmp/` — never delete without
confirmation.

## Guardrails

Do not, unless the task explicitly calls for it:

- Refactor the whole project
- Add complexity from future phases
- Introduce dependencies not already in the project without discussing first
- Change the primary branch directly
- Remove existing tests or checks
- Deviate from Figma specs without flagging to the user
- Introduce raw color, spacing, or font values — use design tokens
- Override component library defaults without justification
- Skip accessibility verification
- Commit `.design/tmp/` contents
- Create empty directories — create `changes/`, `artifacts/`, `tmp/` on first use
- Create PRs/MRs or suggest creating them — commit and push only
- Suggest next steps related to PRs, MRs, or code review workflows

## Decision Rules

- If the repo already has a working pattern, adapt it before inventing a new one
- If a change touches existing production code, choose the least invasive path
- If a feature can be deferred without blocking the current scope, defer it
- If there are two valid paths, choose the one that preserves optionality
- If uncertain about direction, consult the knowledge sources in `.design/CLAUDE.md`
- If uncertain about visual intent, consult Figma (via MCP if available) before guessing
- If a design token doesn't exist for a needed value, flag it rather than hardcoding
- If a component exists in the library, extend or compose it rather than building from scratch
- If the repo has existing knowledge files, reference them — don't duplicate into `.design/knowledge/`

## Core Principles

- Prefer deterministic generation and easy-to-read output
- Do not duplicate product-thinking docs inside implementation files
- Build clean — use existing spikes as reference, do not migrate code forward
- Prefer the simplest orchestration that works; add complexity only when needed
- Visual fidelity to the design spec is a first-class requirement, not a polish step
- Accessibility is built in from the start, not bolted on after
- `.design/` is the skill's portable context — it travels with the branch

## Exit Criteria

Stop when:

- The requested workflow works end to end
- The change is scoped and understandable
- Visual output matches the design spec
- Accessibility basics pass
- The next step is clearer than before

---

## Bootstrap

Run once per repo when `.design/` does not yet exist. Triggered automatically on
first use or via "Preflight" / "Prime".

### Branch

1. Create a `design/<feature-name>` branch from the primary branch
2. Do all work on this branch
3. When spawning subagents for implementation, always use `isolation: "worktree"`
   so each agent gets its own isolated copy and branch

### Detect

Run silently before asking questions. Scan for:

- Language/runtime (manifest files: `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.)
- Package manager (lockfiles: `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, etc.)
- Monorepo signals (`pnpm-workspace.yaml`, `turbo.json`, `nx.json`, workspaces config)
- Git state (primary branch, recent commits, remote URL)
- Existing infrastructure: `CLAUDE.md`, `knowledge/`, `docs/`, `doc/`,
  `CONTRIBUTING.md`, `ARCHITECTURE.md`, `README.md`, `.github/`
- Design system files: token definitions, component libraries, theme configs

### Create `.design/`

Resolve knowledge sources in priority order:

1. **Repo's own `CLAUDE.md`** — if it points to knowledge/context files, reference those
2. **Repo's existing docs** — scan `knowledge/`, `docs/`, `doc/`, `CONTRIBUTING.md`,
   `ARCHITECTURE.md`, `README.md`, or any path referenced in `CLAUDE.md`
3. **Buttress with `.design/knowledge/`** — for anything the repo doesn't provide,
   create from bundled `templates/` (vision.md, architecture.md, standards.md, log.md)
4. **Standalone fallback** — if the repo has nothing, create the full knowledge set
   in `.design/knowledge/` using all bundled templates

Then:

- Create `.design/CLAUDE.md` from `templates/CLAUDE.md` — document which sources
  were found (and where) vs. created
- Create `.design/knowledge/design-system.md` from `templates/design-system.md` —
  populate with tokens, components, and conventions discovered during detection

Do NOT create empty directories. Create `changes/`, `artifacts/`, and `tmp/` only
when there is content to put in them.

### Interview (only if no existing knowledge)

If the repo has no `CLAUDE.md`, no `knowledge/` directory, and no meaningful docs,
ask in a single prompt:

1. What is this project? (one-liner)
2. What problem does it solve and who is it for?
3. Current state? (POC / MVP / production / maintenance / greenfield)
4. What's the next milestone?
5. What's explicitly out of scope?

If repo already has knowledge files, skip the interview — read what exists.
