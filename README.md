# js-plugins

A Claude Code plugin marketplace with design and development workflow tools.

## Install

```shell
/plugin marketplace add <owner>/js-plugins
/plugin install design-kit@js-plugins
```

## Plugins

### design-kit

Two skills for design-oriented development workflows.

#### `/live-canvas`

An infinite canvas with live iframe artboards of your running dev server at multiple viewports and branches. Use it to:

- Compare responsive layouts across breakpoints (desktop, tablet, mobile)
- Visually diff branches side-by-side using git worktrees
- Walk through user flows across multiple routes
- Annotate with sticky notes and callout markers
- Tweak design tokens (colors, spacing, typography) with live hot-reload

#### `/knowledge-init`

Bootstrap a project's knowledge infrastructure. Creates a `knowledge/` directory with vision, architecture, standards, and session log files, plus a `CLAUDE.md` agent entry point tailored to the repo. Use it to:

- Set up agent context for a new or existing project
- Generate a `CLAUDE.md` grounded in real project detection (language, package manager, scripts, git state)
- Install the `/dev` workflow skill for ongoing development sessions

### design-update

Compose Slack update messages summarizing work done across tools for team visibility.

#### `/design-update`

Gathers context from all tools used in a session — git branches, Figma files,
Confluence pages, and more — and composes a formatted, copy-pasteable Slack message.

- Summarizes git branch work with emoji categories and repo links
- Includes links to Figma files, Confluence pages, or other artifacts touched
- Casual, team-friendly tone with scannable bullet points
