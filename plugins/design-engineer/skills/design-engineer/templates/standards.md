# Project Standards

Durable standards for this project. Agents: consult before making structural
decisions. Update when new patterns are established.

---

## Branching

- `[primary-branch]` is a **protected branch** — never commit directly to it
- All work happens on feature branches; changes arrive via merge only
- Do not force-push to the primary branch
- Branch naming: `design/<desc>`, `feat/<desc>`, `fix/<desc>`, `refactor/<desc>`, `chore/<desc>`
- Keep branches short-lived — one milestone or logical unit per branch

## Package Management

- **Package manager:** [detected: pnpm / npm / yarn / cargo / uv / pip / etc.]
- [Lock file committed: yes/no]
- [Any workspace or monorepo conventions]

## Documentation Updates

- **`.design/changes/`** — write a dated entry after every task (decisions, gotchas, deferred work)
- **`standards.md`** — update when new durable standards are established
- **`.design/CLAUDE.md`** — update only when knowledge source routing changes
- **`.design/knowledge/design-system.md`** — update when tokens, components, or conventions change

## [Additional Sections]

[Add sections here as standards emerge. Examples of sections that commonly
develop over time:]

[- Naming conventions (files, variables, functions, classes)]
[- Import / module organization]
[- Test placement and patterns]
[- Error handling patterns]
[- API design conventions]
[- Commit message format]
[- Code review expectations]
[- Design token naming conventions]
[- Component file structure]

[Remove these bracketed hints once real standards are established.]
