# Live Canvas Manifesto

The running app is the source of truth. Not a screenshot. Not a static mockup. Not a browser tab you resize by hand. The real, hot-reloading, data-connected application — rendered at every viewport that matters, on a single pannable surface, annotated by humans and agents alike.

Live Canvas is three ideas fused into one workspace:

1. **Live iframes** — the actual dev server, not a representation of it
2. **Infinite canvas** — spatial arrangement, not tabs or split panes
3. **Local files** — images, video, audio, and code files from disk, displayed and editable alongside live app views
4. **Agent-writable** — the canvas is data (JSON + render functions), so an AI agent can read it, modify it, and extend it

Each of these exists independently. The compound is what changes the workflow.

---

## The Core Use Cases

### Responsive QA

Desktop, tablet, mobile — side by side, simultaneously, from the same dev server. Not a resized browser window. Not toggling DevTools device mode. A persistent spatial layout where every breakpoint is visible at once, all the time, while you code.

This is the most frequent use. Every frontend developer resizes their browser dozens of times a day. The canvas eliminates the toggling.

### Branch Visual Comparison

Two git branches. Same routes. Same viewports. Running simultaneously on different ports via worktrees. Stacked as rows on the canvas so differences are immediately visible — not described in a PR comment, but rendered live in front of you.

Drop markers on regressions. Clip a region and paste it in the PR. The conversation about visual changes happens on a surface where the changes are actually visible.

### User Flow Storyboards

Login, dashboard, settings, profile — laid out left to right like a comic strip. The real app at each step, not wireframes. Walk through the flow with a stakeholder, drop sticky notes on friction points. The canvas is the presentation.

### Design Token Tuning

A draggable panel with sliders and color pickers wired directly to CSS custom properties. Move a slider, the token file on disk updates, the dev server hot-reloads, every iframe refreshes. You see the impact of `--spacing-lg: 24px` vs `--spacing-lg: 32px` across every viewport simultaneously.

This is a GUI design system editor that writes real code. The feedback loop is measured in milliseconds.

### File Nodes as Spatial Context

The canvas now handles five file types alongside live iframes:

- **Images** — screenshots, mockups, reference designs placed next to the running app. Drop a Figma export next to the live implementation for pixel-level comparison.
- **Video** — screen recordings, prototype walkthroughs, QA captures playing inline. A bug reproduction video next to the artboard showing the fix.
- **Audio** — voiceover notes, user interview clips, notification sounds. Audio context that would otherwise live in a separate app, now adjacent to the visual work.
- **Code** — source files editable on-canvas with save-to-disk and hot-reload. Edit a component file while watching every viewport update in real time.
- **Text** — config files, markdown specs, JSON fixtures. Reference material that doesn't need a separate editor window.

File nodes participate in the same spatial system as iframes: drag, resize, annotate with sticky notes, include in clip captures. They're nodes, not attachments.

---

## The Niche Opportunities

### Internationalization Review

Same page, same viewport, different locales as separate rows. German text that overflows buttons. Japanese copy that needs different line-height. Arabic RTL layout. All visible at the same time on the same canvas. The overflow bugs reveal themselves instantly when languages are spatially adjacent.

### Theme Comparison

Light mode, dark mode, high-contrast — three rows, same routes, same breakpoints. Tweak a design token and see it propagate across all themes simultaneously. Theme bugs are almost always discovered late because developers work in one theme at a time. The canvas removes that constraint.

### A/B Variant Review

Two branches implementing two UX approaches. Same route, same viewports, stacked. Sticky notes scoring each variant. Clip both, share in a thread. The comparison happens on a surface where both variants are alive and interactive, not reduced to static screenshots in a slide deck.

### Multi-Service Dashboard

Each iframe can point to a different port. Auth service on 3001, dashboard on 3002, admin panel on 3003. For teams running micro-frontends or independent services, the canvas becomes the single surface where the entire product is visible at once.

### Email Template Development

Email rendering is notoriously inconsistent. Point iframes at different preview renderers — Outlook-style, Gmail-style, Apple Mail-style — at different widths. The canvas becomes a rendering matrix for email HTML without switching between tabs or services.

### Accessibility Auditing

Every iframe is a live DOM. A custom widget can run automated a11y checks against each artboard and surface violations inline — WCAG issues across all viewports on one canvas. The spatial layout reveals patterns: "this contrast issue only appears at mobile width."

---

## The Compound Workflows

These emerge from combining the core primitives in ways that are greater than the sum.

### Agent-Driven Design Iteration

The canvas JSON is a structured communication protocol between human and agent. Every sticky note has text and coordinates. Every marker has a label and coordinates. Every artboard has a route, viewport, branch, and bounding box. Spatial proximity links annotations to the views they describe.

The loop:

1. The agent edits code. Artboard iframes hot-reload across every viewport.
2. The human reviews the canvas. Drops a sticky note — "padding is way too tight here" — next to the Mobile artboard on `/dashboard`. Drops a marker on the Desktop view where the header overlaps.
3. The human tells the agent: "check my canvas for feedback."
4. The agent reads the canvas JSON. For each note and marker, it computes which artboard is nearest. It now knows: this feedback is about `/dashboard` at 390px on the `main` branch. That marker is pointing at the header area of the Desktop view.
5. The agent makes the fixes. The canvas updates.

No screenshots. No copy-pasting error descriptions. No "can you look at the mobile view" back-and-forth. The feedback is structured data with spatial context — richer than a screenshot (which is pixels) and more precise than a chat message (which lacks positional reference).

Sticky notes become agent instructions. Markers become bug reports. The canvas is a visual conversation layer between human and machine — and the conversation is machine-readable.

### The War Room

The `+ Add > URL / Embed` button accepts any iframe-able URL. Embed a Figma file next to the running app next to a Grafana dashboard next to the CI pipeline next to a Notion spec. The canvas becomes the surface where the product and all its context coexist — not spread across browser tabs, but spatially arranged and annotated.

File nodes add local media to the war room surface — screen recordings of bugs playing inline, reference screenshots for comparison, source files open for editing. Combined with iframe embeds for Loom, YouTube, Figma, Grafana, and CI dashboards, the canvas holds both live external services and local project artifacts on the same spatial surface.

### Bug Reproduction Board

The artboard showing the bug at the relevant viewport. A screen recording of the reproduction steps playing inline beside it. The source file where the fix needs to happen, open in an editable code node. Sticky notes describing the steps to reproduce, expected behavior, and actual behavior. Everything spatial, everything live. Fix the code on the canvas, watch the artboard hot-reload with the fix, compare against the recording.

### Design Handoff Board

A Figma embed of the design spec next to the running implementation at matching viewports. Reference images exported from the design tool for pixel comparison. The component source file open for editing. The design token node showing the project's token values. Designer and developer looking at the same spatial surface — the conversation about implementation fidelity happens where both the design and the code are visible and interactive.

### Design System as a Live Document

Instead of showing components in isolation, show full pages using the design system at every breakpoint. The design token panel sits adjacent — demonstrating that changing `--radius-md` from 8px to 12px affects these specific pages in these specific ways. The canvas is the documentation. And it's never stale because it's running real code.

### Visual Regression Workspace

Clip captures include metadata: branch, route, viewport, zoom. A custom widget could store baseline captures and overlay them against the current state. Not a CI pixel-diff pipeline, but a lightweight visual comparison workspace during development — catch regressions before you push, not after.

### Performance-Aware Design

A custom widget that queries performance metrics from each embedded server and displays them alongside the rendered artboards. Move a design token slider, see the performance impact. The canvas holds the visual output and the numbers in the same spatial context.

### Teaching and Pair Programming

An instructor sets up a canvas with the student's app at multiple breakpoints. Markers pointing at issues. Sticky notes with lesson content. Export the canvas JSON, student imports it — same annotated view, fully async. Lighter than screen sharing, more persistent, more structured.

---

## Why This Compounds

The custom widget system is the extensibility mechanism. Each niche above — a11y auditing, perf monitoring, i18n review, regression tracking — is a JSON config and a render function. What would otherwise be a separate product is a canvas node that an agent can build in a single session.

The canvas is not a fixed tool. It is a platform that adapts per-project, per-team, per-workflow. The primitives are simple: iframes, draggable nodes, JSON persistence, a Python file server. The surface area of what you can build on those primitives is unbounded.

The running app is the source of truth. The canvas is where you see it clearly.
