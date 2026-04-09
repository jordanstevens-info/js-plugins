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

- **`.design/changelog/`** — write a dated entry after every session (see `templates/changelog-entry.md`)
- **`standards.md`** — update when new durable standards are established
- **`.design/README.md`** — update only when knowledge source routing changes
- **`.design/knowledge/design-system.md`** — update when tokens, components, or conventions change

## Design Decisions

Durable design decisions graduated from session changelogs. These persist across
branches and inform future work.

[Decisions are added here as they emerge from design work. Examples:]
[- "Use DS Tooltip over Flowbite Tooltip for all new tooltip usage"]
[- "Inline SVGs for icons when type declarations are missing"]

[Remove these bracketed hints once real decisions are established.]

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
