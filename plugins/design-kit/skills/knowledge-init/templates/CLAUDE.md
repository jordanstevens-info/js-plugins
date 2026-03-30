# [Project Name]

[One-line description — the elevator pitch from vision.md]

## Quick Reference

**Key principle:** [The single most important architectural constraint or design
decision. One sentence that orients every agent touching this codebase.]

## Commands

```bash
[dev command]      # [description]
[build command]    # [description]
[test command]     # [description]
[lint command]     # [description — omit if not detected]
```

## Repo Layout

```
[project-root]/
  [detected top-level structure with brief annotations]
```

## Stack

- **[Category]:** [Technology + version if relevant]

## Context Files

Before implementation work, read:

| File | Purpose |
|------|---------|
| `.claude/skills/dev/SKILL.md` | Workflow rules, guardrails, decision framework |
| `knowledge/architecture.md` | Project structure, phases, technical decisions |
| `knowledge/vision.md` | Product vision, rationale, out-of-scope |
| `knowledge/standards.md` | Durable project standards |
| `knowledge/log.md` | Running log of decisions, gotchas, deferred work |

After working, update `knowledge/log.md` (and `knowledge/standards.md` if new standards were established).
