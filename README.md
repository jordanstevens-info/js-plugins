# js-plugins

A Claude Code plugin marketplace with design and development workflow tools.

## Install

```shell
claude plugin marketplace add https://github.com/jordanstevens-info/js-plugins
claude plugin install design-engineer@js-plugins
```

## Plugins

### design-engineer

Cross-repo design engineering workflow that bootstraps a `.design/` context directory on a dedicated `design/` branch. Handles the full lifecycle from project detection through implementation to verification.

- Bootstraps `.design/` with knowledge files (vision, architecture, standards, design system)
- Figma-to-code implementation with visual QA and accessibility checks
- Design token compliance — flags hardcoded values, uses existing tokens
- Responsive layout verification across breakpoints
- Structured verification checklists before committing
- Session change logs in `.design/changes/`

### live-canvas

An infinite canvas with live iframe artboards of your running dev server at multiple viewports and branches.

#### `/live-canvas`

- Compare responsive layouts across breakpoints (desktop, tablet, mobile)
- Visually diff branches side-by-side using git worktrees
- Walk through user flows across multiple routes
- Annotate with sticky notes and callout markers
- Tweak design tokens (colors, spacing, typography) with live hot-reload
- Embed local files (images, video, audio, code) alongside live artboards

### design-update

Compose Slack update messages summarizing work done across tools for team visibility.

#### `/design-update`

- Summarizes git branch work with emoji categories and repo links
- Includes links to Figma files, Confluence pages, or other artifacts touched
- Casual, team-friendly tone with scannable bullet points
