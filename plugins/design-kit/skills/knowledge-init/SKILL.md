---
name: knowledge-init
description: |
  Bootstrap a project's knowledge infrastructure. Use when starting work on a new
  project that lacks knowledge files, when setting up agent infrastructure for an
  existing codebase, when a project has no CLAUDE.md or knowledge/ directory, or
  when the user says "init project", "bootstrap knowledge", "set up agent context",
  "create knowledge files", "initialize dev workflow", "set up dev", "knowledge init",
  "init knowledge", "dev init", "init dev", or "set up CLAUDE.md".
---

# Knowledge Init

Bootstrap a project with a knowledge infrastructure that agents can read and
maintain across sessions. Creates `knowledge/` files (vision, architecture,
standards, log), a `CLAUDE.md` entry point, and installs the `dev` workflow
skill into the project.

Templates live in `${CLAUDE_PLUGIN_ROOT}/skills/knowledge-init/templates/`. Read each template for
its section structure, then populate with real project data — never copy templates
verbatim.

---

## Phase 0 — Detect

Run silently before asking any questions. Never ask something detection can answer.

### What to detect

**Language / runtime** — scan for manifest files:
- `package.json` → Node.js / JavaScript / TypeScript
- `Cargo.toml` → Rust
- `pyproject.toml`, `setup.py`, `setup.cfg` → Python
- `go.mod` → Go
- `Gemfile` → Ruby
- `pubspec.yaml` → Dart / Flutter
- `composer.json` → PHP
- `mix.exs` → Elixir
- `build.gradle`, `pom.xml` → Java / Kotlin
- `.nvmrc`, `.python-version`, `.ruby-version`, `.tool-versions` → version pinning

**Package manager** — check lockfiles:
- `pnpm-lock.yaml` → pnpm
- `yarn.lock` → yarn
- `bun.lockb` → bun
- `package-lock.json` → npm
- `uv.lock` → uv
- `poetry.lock` → poetry
- `Pipfile.lock` → pipenv
- `requirements.txt` → pip
- `Cargo.lock` → cargo
- `go.sum` → go modules
- `Gemfile.lock` → bundler

**Monorepo signals**:
- `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`
- `workspaces` key in `package.json`
- `Cargo.toml` with `[workspace]` section
- Multiple manifest files in subdirectories

**Git**:
- `git rev-parse --abbrev-ref HEAD` → primary branch name
- `git log --oneline -5` → recent commits (is this a fresh repo or active?)
- `git remote -v` → remote URL (GitHub, GitLab, etc.)
- `git status --short` → current state

**Existing infrastructure**:
- `CLAUDE.md` → already has an agent entry point?
- `knowledge/` directory → already has knowledge files?
- `.claude/skills/` → already has skills?
- `README.md`, `docs/`, `CONTRIBUTING.md` → existing documentation
- `AGENTS.md` → existing agent instructions

**Build / test / CI**:
- `scripts` in `package.json` (or equivalent manifest)
- `Makefile`, `justfile`, `Taskfile.yml`
- `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`
- `Dockerfile`, `docker-compose.yml`
- Test configs: `vitest.config.*`, `jest.config.*`, `pytest.ini`, `phpunit.xml`, etc.

### Report preflight

Present findings to the user before proceeding:

```
Detected:
  Language:        [language(s)]
  Package manager: [manager] ([lockfile] found)
  Workspace:       [monorepo / single package] ([signal])
  Git:             [branch], [N] commits, origin: [remote]
  Existing docs:   [what exists / what's missing]
  Build:           [key commands from scripts]
  Tests:           [framework] ([config file] found)

  Existing infra:  [CLAUDE.md: yes/no] [knowledge/: yes/no] [skills/: yes/no]
```

If `knowledge/` or `CLAUDE.md` already exist, warn the user and ask how to
proceed (skip, overwrite, or merge).

---

## Phase 1 — Interview

Ask targeted questions in a single prompt. Skip questions that detection answered.

### Always ask

1. **What is this project?** — One-liner that will become the CLAUDE.md opening
   and vision tagline.
2. **What problem does it solve? Who is it for?** — Users, consumers, or audience.
3. **Current state?** — POC / MVP / production / maintenance / greenfield.
4. **What's the next milestone?** — The immediately actionable goal.
5. **What's explicitly out of scope?** — At least 2-3 things. This constrains
   future agents as much as in-scope items guide them.

### Ask only if detection couldn't determine

- Key technical decisions already made (if no README or docs)
- Main dev/build/test commands (if no scripts detected in manifest)
- Package naming convention (if monorepo detected but naming unclear)
- Branch protection / naming convention (if git history is ambiguous)
- Any domain-specific terminology that agents should know

Bundle all questions into one `AskUserQuestion` call. Number them clearly.

---

## Phase 2 — Generate

Create the directory structure:

```bash
mkdir -p knowledge
mkdir -p .claude/skills/dev
```

Read each template from `${CLAUDE_PLUGIN_ROOT}/skills/knowledge-init/templates/` for its section
structure. Generate each file populated with real data from detection and
interview answers.

### Generation order

1. **`knowledge/vision.md`** — from interview answers (freshest context)
2. **`knowledge/architecture.md`** — from project analysis + interview
3. **`knowledge/standards.md`** — from detected standards + interview
4. **`knowledge/log.md`** — bootstrap entry with today's date
5. **`CLAUDE.md`** — aggregates detection + interview into the agent entry point
6. **`.claude/skills/dev/SKILL.md`** — copy from `${CLAUDE_PLUGIN_ROOT}/skills/knowledge-init/templates/dev-SKILL.md` verbatim (no customization needed)

### Generation rules

- **CLAUDE.md must be accurate.** Extract real commands from `package.json`
  scripts (or equivalent), real directory structure from the filesystem, real
  stack from detected dependencies. If something can't be determined, use
  `[TODO: ...]` markers — never guess.
- **standards.md ships with branching pre-populated.** Use the detected primary
  branch name. Branching standards are the most consequential to get right from
  day one.
- **log.md bootstrap entry models the format.** A date heading, bullet points,
  current state + next milestone. Future agents will follow this pattern.
- **vision.md is the user's words.** Don't embellish or rewrite the interview
  answers beyond light formatting. The user's mental model is the source of truth.
- **architecture.md can be sparse.** If the project is early-stage, a minimal
  structure section + one or two decisions is fine. The file grows as the project
  grows.

---

## Phase 3 — Verify

After generating all files:

1. Confirm the file structure exists:
   ```bash
   ls knowledge/
   ls .claude/skills/dev/
   cat CLAUDE.md | head -5
   ```

2. Present a summary to the user:
   ```
   Created:
     knowledge/vision.md        — Product vision and rationale
     knowledge/architecture.md  — Project structure and decisions
     knowledge/standards.md     — Durable project standards
     knowledge/log.md           — Session log (bootstrap entry added)
     CLAUDE.md                  — Agent entry point
     .claude/skills/dev/SKILL.md — Dev workflow skill

   Review: [list any sections marked TODO or needing manual input]
   ```

3. Remind the user:
   - The `dev` skill is now installed — it activates on implementation tasks
   - Use "Preflight" / "Prime" to start a work session
   - Use "Shutdown" / "Wrap-Up" to end one
   - Knowledge files are meant to evolve — the dev skill updates them as work proceeds
