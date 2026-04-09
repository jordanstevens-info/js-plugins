# Bootstrap

Run once per repo when `.design/` does not yet exist. Triggered automatically on
first use or via "Preflight" / "Prime".

## Branch

1. Create a `design/<feature-name>` branch from the primary branch
2. Do all work on this branch
3. When spawning subagents for implementation, always use `isolation: "worktree"`
   so each agent gets its own isolated copy and branch

## Detect

Run silently before asking questions. Scan for:

- Language/runtime (manifest files: `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.)
- Package manager (lockfiles: `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, etc.)
- Monorepo signals (`pnpm-workspace.yaml`, `turbo.json`, `nx.json`, workspaces config)
- Git state (primary branch, recent commits, remote URL)
- Existing infrastructure: `CLAUDE.md`, `knowledge/`, `docs/`, `doc/`,
  `CONTRIBUTING.md`, `ARCHITECTURE.md`, `README.md`, `.github/`
- Design system files: token definitions, component libraries, theme configs

## Create `.design/`

Resolve knowledge sources in priority order:

1. **Repo's own `CLAUDE.md`** — if it points to knowledge/context files, reference those
2. **Repo's existing docs** — scan `knowledge/`, `docs/`, `doc/`, `CONTRIBUTING.md`,
   `ARCHITECTURE.md`, `README.md`, or any path referenced in `CLAUDE.md`
3. **Buttress with `.design/knowledge/`** — for anything the repo doesn't provide,
   create from bundled `templates/` (vision.md, architecture.md, standards.md)
4. **Standalone fallback** — if the repo has nothing, create the full knowledge set
   in `.design/knowledge/` using all bundled templates

Then:

- Create `.design/README.md` from `templates/README.md` — document which sources
  were found (and where) vs. created
- Create `.design/knowledge/design-system.md` from `templates/design-system.md` —
  populate with tokens, components, and conventions discovered during detection

Do NOT create empty directories. Create `changelog/`, `artifacts/`, and `tmp/` only
when there is content to put in them.

When `tmp/` is first created, add `.design/tmp/` to the repo's `.gitignore`.

## Interview (only if no existing knowledge)

If the repo has no `CLAUDE.md`, no `knowledge/` directory, and no meaningful docs,
ask in a single prompt:

1. What is this project? (one-liner)
2. What problem does it solve and who is it for?
3. Current state? (POC / MVP / production / maintenance / greenfield)
4. What's the next milestone?
5. What's explicitly out of scope?

If repo already has knowledge files, skip the interview — read what exists.
