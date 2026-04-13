# js-plugins

A Claude Code plugin marketplace with design and development workflow tools.

## Install

```shell
claude plugin marketplace add https://github.com/jordanstevens-info/js-plugins
claude plugin install design-engineer@js-plugins
```

## Plugins

### design-engineer

Cross-repo design engineering workflow that bootstraps a `.design/` context directory on a dedicated `design/` branch. Handles the full lifecycle from project detection through implementation, delivery, and team communication.

**Skills:**

- **design-engineer** — Figma-to-code implementation with visual QA, accessibility checks, design token compliance, responsive layout verification, and structured changelogs in `.design/changelog/`
- **design-to-backlog** — Convert design artifacts (branches, Figma files, Confluence specs) into grooming-ready Jira tickets with outcome-focused acceptance criteria
- **design-to-mr** — Cut a clean merge request branch from a design branch with scoped file selection, MR description drafting, and pre-filled MR links
- **design-update** — Compose copy-pasteable Slack updates summarizing session work across git, Figma, Confluence, and other tools

### live-canvas

An infinite canvas with live iframe artboards of your running dev server at multiple viewports and branches.

#### `/live-canvas`

- Compare responsive layouts across breakpoints (desktop, tablet, mobile)
- Visually diff branches side-by-side using git worktrees
- Walk through user flows across multiple routes
- Annotate with sticky notes and callout markers
- Tweak design tokens (colors, spacing, typography) with live hot-reload
- Embed local files (images, video, audio, code) alongside live artboards

### caveman-output-style

Ultra-compressed communication mode based on [caveman](https://github.com/JuliusBrussee/caveman) — cuts output tokens while keeping full technical accuracy. Ships as output styles selectable via `/config` → Output style.

**Levels:**

| Level | What it does |
|-------|-------------|
| **Caveman Lite** | No filler/hedging. Keep articles + full sentences. Professional but tight |
| **Caveman** | Drop articles, fragments OK, short synonyms. Classic caveman |
| **Caveman Ultra** | Abbreviate (DB/auth/config/req/res/fn/impl), strip conjunctions, arrows for causality (X → Y), one word when one word enough |

```shell
claude plugin install caveman-output-style@js-plugins
```

Select a level via `/config` → Output style. Always-on once selected — no skill invocation needed. Switch to Default to turn off.
