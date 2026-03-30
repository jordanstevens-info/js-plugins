---
name: dev
description: |
  Generalized development workflow for projects with a knowledge infrastructure
  (knowledge/vision.md, knowledge/architecture.md, knowledge/standards.md,
  knowledge/log.md, CLAUDE.md). Use when implementing features, fixing bugs,
  building new functionality, refactoring code, or doing any development work
  in this project. Triggers on "implement", "build", "add feature", "fix",
  "work on", "code", "develop", "update", "refactor", or any request to make
  changes to the codebase.
---

# Development Workflow

Move the project forward in small, safe steps while keeping implementation
aligned with the knowledge infrastructure.

For product vision and rationale, consult `knowledge/vision.md`.
For architecture, structure, phases, and decisions, consult `knowledge/architecture.md`.
Do not duplicate that material here.

## Working Style

- Prefer the smallest useful increment
- Reuse existing repo conventions and tooling
- Keep new work isolated when possible
- Avoid broad refactors unless they directly unblock the current step
- Leave clear extension points instead of building future phases early

## Workflow

Follow these steps in order for any implementation task.

#### User Triggers:
- **Preflight, Prime** — Complete steps 0-2, report readiness
- **Shutdown, Wrap-Up, Finish, Retro** — Commit, merge, step 7, report doneness

### 0. Branch Before Coding

Per `knowledge/standards.md`, the primary branch is protected. Before writing
any code:

1. Create a feature branch from the primary branch
2. Do all work on the feature branch
3. When spawning subagents for implementation, always use `isolation: "worktree"`
   so each agent gets its own isolated copy and branch

### 1. Inspect Before Changing

Read before writing. Locate existing patterns, utilities, and conventions before
adding new ones.

Read `knowledge/standards.md` for established project standards.
Read `knowledge/log.md` for recent decisions and context from prior sessions.
Read `knowledge/architecture.md` for target structure and current phase/milestone.

### 2. Know Your Phase

Check which phase or milestone is current in `knowledge/architecture.md`. Confirm
in `knowledge/log.md` for the latest status.

Do not pull work from future phases into the current change unless it is trivially
small and unblocks something.

### 3. Pick the Smallest Landing Zone

Prefer an existing module, package, or file if the work fits there. Only create
new structure when the architecture calls for it and the current phase requires it.
Use a temporary area only if the repo structure does not support a cleaner placement.

### 4. Start from the Source-of-Truth Layer

Work from the bottom of the dependency stack upward. In a data-driven project:
data model first, then generation/transformation, then UI/surfaces. In a library:
core logic first, then adapters, then consumers.

Check `knowledge/architecture.md` for the project's specific dependency direction.

### 5. Verify Before Stopping

- Check the intended user flow end to end
- Check generated output or behavior manually
- Check that repo impact stayed scoped
- Run the build/test command (see `CLAUDE.md` for the exact command)

### 6. Present Verification Steps

After completing a task, always present the user with a numbered verification
checklist before committing. Each step should include:

- The exact command to run or action to take (copy-pasteable)
- What to expect (expected output, visual result, or behavior)

Keep it concise — no prose, just steps and expected outcomes. Tailor to what
changed: infrastructure work gets build/wiring checks, UI work gets browser
interaction steps.

### 7. Document the Delta

Update `knowledge/log.md` with a dated entry covering:

- Where the work lives
- What was added or changed
- What was intentionally deferred

Update `knowledge/standards.md` if new durable standards were established.

## Guardrails

Do not, unless the task explicitly calls for it:

- Refactor the whole project
- Add complexity from future phases
- Introduce dependencies not already in the project without discussing first
- Change the primary branch directly
- Remove existing tests or checks

## Decision Rules

- If the repo already has a working pattern, adapt it before inventing a new one
- If a change touches existing production code, choose the least invasive path
- If a feature can be deferred without blocking the current phase, defer it
- If there are two valid paths, choose the one that preserves optionality
- If uncertain about direction, read `knowledge/vision.md` for the product thesis

## Core Principles

- Prefer deterministic generation and easy-to-read output
- Do not duplicate product-thinking docs inside implementation files
- Build clean — use existing spikes as reference, do not migrate code forward
- Prefer the simplest orchestration that works; add complexity only when needed

## Exit Criteria

Stop when:

- The requested workflow works end to end
- The change is scoped and understandable
- The output is deterministic enough to build on
- The next step is clearer than before
