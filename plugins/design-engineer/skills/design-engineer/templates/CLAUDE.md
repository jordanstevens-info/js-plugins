# [Project Name]

[One-line description — from repo CLAUDE.md, README, or interview]

## Design Context

**Branch:** `design/[feature-name]`
**Figma:** [URL if known, otherwise omit this line]
**Scope:** [What this design branch is implementing]

## Knowledge Sources

Sources resolved during `.design/` bootstrap. **Found** = referenced from repo.
**Created** = generated in `.design/knowledge/` from templates.

| File | Path | Status |
|------|------|--------|
| Vision | [path or `.design/knowledge/vision.md`] | [found / created] |
| Architecture | [path or `.design/knowledge/architecture.md`] | [found / created] |
| Standards | [path or `.design/knowledge/standards.md`] | [found / created] |
| Design System | `.design/knowledge/design-system.md` | created |

**Repo CLAUDE.md:** [yes — path / no]
**Repo docs:** [list paths found, or "none"]

## Commands

```bash
[dev command]      # [description]
[build command]    # [description]
[test command]     # [description]
[lint command]     # [description — omit if not detected]
```

## Working With This Context

Before implementation, read the knowledge sources listed above.

After working:
- Write a dated entry in `.design/changes/`
- Update `.design/knowledge/design-system.md` if new tokens or components were established
- Update `.design/knowledge/standards.md` if new durable standards emerged
