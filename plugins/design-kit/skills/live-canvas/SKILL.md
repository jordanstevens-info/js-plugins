---
name: "live-canvas"
description: |
  Spin up an infinite canvas with live iframe artboards of the running app at
  multiple viewports and branches. Use when the user wants to compare responsive
  layouts, review design across breakpoints, visually diff branches side-by-side,
  walk through a user flow across screens, or when the user says to check their
  canvas notes/feedback (read annotations from the canvas JSON and act on them).
---

# Live Canvas

An infinite-canvas viewer that embeds **live iframes** of your running dev server — not static mockups, not screenshots, the real app. Each artboard renders at a specific viewport size, and branch rows let you stack git branches for visual comparison. Artboards are freely draggable, and you can annotate with sticky notes and design token nodes.

| Existing tool | What's missing |
|---|---|
| Figma / Paper | Static — not the real app |
| Browser DevTools | One viewport at a time, no canvas |
| Storybook | Components only, not full pages |

Live Canvas combines: **real running app** + **multi-artboard canvas** + **agent-driven code editing**.

See: `references/manifesto.md` for design philosophy and use cases.

> **Which file to edit:**
> - Changing visual styles (colors, spacing, sizing, layout) → `canvas.css`
> - Changing behavior, interactions, or data → `live-canvas.html`
> - Changing server API endpoints → `serve.py`

> **Always read before writing.** The canvas implementation evolves with user requests — functions get renamed, moved, refactored, or removed. Never assume a function name, variable, or structure described in this document still exists. Before making any change, read `live-canvas.html` (or `canvas.css` for style changes) and search for the *pattern* (e.g. "the function that renders sticky notes" or "where arrays are serialized to JSON"), confirm it matches what you expect, and adapt accordingly. The code snippets in this document are illustrative templates, not copy-paste targets.

---

## Server Management

The canvas server must be restarted whenever `live-canvas.html` or `serve.py` changes (including when copying updated templates from the skill). The server reads these files on each HTTP request, but Python caches the module — so `serve.py` changes require a full restart.

**Before launching or after any file changes:**

1. **Check for existing server on the port:**
   ```bash
   lsof -i :8888 -sTCP:LISTEN -P 2>/dev/null | awk 'NR>1{print $2}'
   ```

2. **Verify it's running from the right directory** (critical — stale servers from other directories are a common issue):
   ```bash
   lsof -p <pid> | grep cwd
   ```
   The `cwd` should point to the project's `live-canvas/` directory. If it points elsewhere (e.g., Trash, a different project), kill it.

3. **Restart:**
   ```bash
   # Kill any existing server on the port
   lsof -i :8888 -sTCP:LISTEN -P 2>/dev/null | awk 'NR>1{print $2}' | xargs kill 2>/dev/null
   sleep 0.5
   # Start fresh (os.chdir in serve.py handles the working directory)
   python3 {dir}/serve.py &
   # Verify it's up
   sleep 1 && curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/live-canvas.html
   ```

4. **After updating canvas files** (e.g., copying new templates, modifying HTML/JS), always restart the server so the browser loads the latest version. Tell the user to reload the canvas tab.

---

## Canvas Features Reference

Quick reference for what the canvas tool supports. Use this when answering user questions about capabilities. Feature names and behaviors described here reflect the canvas at the time of writing — verify against the actual `live-canvas.html` if anything seems off.

### Navigation

| Action | Input |
|---|---|
| Pan | Click + drag on canvas background |
| Zoom | Scroll wheel (zooms toward cursor) |
| Fit all | Double-click canvas / grid button in toolbar |
| Zoom to 100% | Click percentage in toolbar |
| Zoom in/out | `Cmd +` / `Cmd -` |
| Reset to 100% | `Cmd 0` |
| Fit all | `Cmd 1` |
| Filepath | P |
| Frame | F |
| URL / Embed | U |

### Dragging

Canvas nodes are freely draggable (this has historically included artboards, branch labels, sticky notes, and design token nodes — check the current implementation for the full list):
- Hover over an artboard or branch label to reveal the **⠿ drag grip** on the left
- Click and drag the grip to move the element
- Positions persist across reloads via the canvas JSON

### Inline Editing

Click any artboard label to edit it via popover:
- **Screen name** — click the name (e.g., "Desktop") to rename
- **Route** — click the route (e.g., "/dashboard") to change the URL path
- **Dimensions** — click the dims (e.g., "1440 x 900") to resize

Changes auto-save to the canvas JSON file via the server API.

### Deleting Nodes

Hover over any node to reveal the **×** close button. Some node types show a confirmation prompt before removing, others delete instantly. Check the current delete behavior in `live-canvas.html` if the exact behavior matters.

### Canvas Switcher

The dropdown in the titlebar lists all canvas JSON files in the `canvases/` directory. Users can:
- Switch between saved canvases
- Create a new canvas from the dropdown

### + Add Dropdown

The unified **+ Add** button in the titlebar provides five options:
- **Filepath** (P) — prompts for an absolute file path and adds a file node to the canvas (image, video, audio, or text/code editor)
- **Frame** (F) — prompts for port, route, label, and dimensions, then adds a standalone iframe to the canvas
- **Marker** (M) — enters marker placement mode (click canvas to place a numbered arrow flag)
- **Note** (N) — enters sticky note placement mode (click canvas to place)
- **URL / Embed** (U) — accepts a plain URL, an `<iframe>` embed code, or a Figma link that auto-converts to an embed URL. Parsed `<iframe>` attributes `allowfullscreen`, `allow`, and `sandbox` are preserved on the rendered iframe; `style` and `frameborder` are discarded (the canvas controls those).

All items have single-letter keyboard shortcuts (shown in parentheses above). Shortcuts are ignored when an input, textarea, or contenteditable element has focus.

### Prompt Button

The **Prompt** button in the titlebar (between Add and Clip) opens a panel for generating context-aware prompts for the agent. Type a freeform description of what you want to do — add a branch, create viewports, tweak tokens, add file nodes, etc. — and click **Copy Prompt**.

The generated prompt includes:
- A `/live-canvas` skill reference so the agent loads the full skill docs
- Your description as the request
- Canvas context summary: branches (with ports), routes, file node count and names, note and marker counts

This replaces the old "Branch" menu item, generalizing it from branch-only prompts to any canvas task.

### Sticky Notes

Yellow sticky notes for annotations on the canvas:
- Place via the **+ Add → Note** dropdown or the **note button** in the toolbar
- Keyboard shortcut: press **N** to toggle note placement mode
- Click anywhere on the canvas to place a note
- Type directly into the note (contenteditable)
- Drag by the header area
- Delete via the × button on hover
- Notes persist in the canvas JSON

### Callout Markers

Lightweight arrow flags for pointing at specific spots during design reviews:
- Place via **+ Add → Marker** or press **M** to toggle marker mode, then click
- Default label is auto-numbered (1, 2, 3...) — click the text to edit it to anything (a number, word, or short phrase)
- Small amber flag with a left-pointing arrow tip — the tip marks the exact spot
- Drag the flag body to reposition, hover to reveal × to delete (no confirm prompt)
- Persist in canvas JSON

### File Nodes

File nodes display local files directly on the canvas. Two modes based on file extension:

**Image mode** (`.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`, `.ico`, `.bmp`):
- Displays the image via `GET /api/file?path=...` with correct Content-Type
- Resize via the dimensions popover (click the W×H label in the header)
- Drag by the header, duplicate, or delete on hover
- Images use `Cache-Control: no-cache` so edits refresh immediately

**Text/code mode** (`.css`, `.ts`, `.js`, `.json`, `.py`, `.html`, `.md`, `.txt`, and many more):
- Monospace `<textarea>` editor with dark background
- **Save** button writes content to disk via `POST /api/file` and reloads all artboard iframes after 600ms (hot reload)
- **Resync** button re-reads the file from disk via `POST /api/file/read` (useful after external edits or agent changes)
- Modified dot (accent-colored circle) appears when editor content differs from the on-disk baseline
- Tab key inserts 2 spaces instead of moving focus

**Video mode** (`.mov`, `.mp4`, `.webm`, `.ogg`, `.m4v`, `.avi`):
- Plays video inline via `<video controls>` element
- Default size: 500×350
- Drag by the header, resize via dimensions popover, duplicate, or delete on hover

**Audio mode** (`.mp3`, `.wav`, `.aac`, `.m4a`, `.flac`):
- Compact `<audio controls>` player
- Default size: 400×100
- Drag by the header, duplicate, or delete on hover

**When agents should add file nodes:**
- Place a component's source file next to its artboard for side-by-side editing
- Add CSS/token files so users can edit styles and see live hot-reload
- Include images for visual reference alongside live artboards

File nodes persist in the canvas JSON under the `fileNodes` array. Each node stores `source` (absolute path), `fileType` (`"image" | "video" | "audio" | "text"`), dimensions, and for text files, `content` and `originalContent`.

**PermissionError handling:** If the server cannot read a file due to macOS sandboxing, it returns a 403 with a hint to grant Full Disk Access to the terminal app in System Settings > Privacy & Security. The file node displays this error message inline.

### Clip Tool

The clip button in the titlebar enables screen-region capture:
1. Click **Clip** (or the scissors icon)
2. Drag a rectangle over any region of the canvas
3. The clipped image is copied to clipboard and downloaded as PNG
4. A caption strip is appended with branch name, port, route, viewport, and zoom level
5. Press `Esc` to cancel clip mode

### Server Banner

When the canvas detects the Python server isn't running (e.g., opened via `file://`), it shows a warning banner with the command to start the server. Persistence is disabled without the server.

---

## Frame Budget

Each artboard and standalone frame is a live iframe — a full browser context with its own DOM, JS runtime, and memory. Performance degrades as frame count grows.

**Guidelines per canvas:**

| App weight | Comfortable | Pushing it | Too many |
|---|---|---|---|
| Heavy SPA (Next.js, large React) | 3–6 | 8–10 | 12+ |
| Light pages (static, simple apps) | 8–12 | 15 | 20+ |

**When generating canvas configs**, prefer splitting across multiple canvases over packing everything into one:

- **One flow per canvas** — e.g., "Login Flow" (3 screens at desktop) and "Dashboard Breakpoints" (3 viewports) as separate canvases, not 6 frames on one canvas
- **One branch comparison per canvas** — comparing 2 branches × 3 viewports = 6 frames is fine; 3 branches × 3 viewports = 9 frames is where you should suggest splitting
- **Suggest the canvas switcher** — when a user's request would produce more frames than the comfortable range, recommend splitting into multiple canvases and using the switcher to navigate between them

**Example recommendation:**

> That's 4 routes × 3 breakpoints = 12 frames, which may get sluggish. I'll split this into two canvases:
> - **"Auth Flow"** — Login, Register, Forgot Password at Desktop/Tablet/Mobile (9 frames)
> - **"Dashboard"** — Dashboard at Desktop/Tablet/Mobile (3 frames)
>
> You can switch between them using the dropdown in the titlebar.

The canvas switcher unloads one canvas and loads the next, so total frame count across all canvases doesn't matter — only the count on the active canvas.

---

## Reading Canvas Feedback

When the user says something like **"check my canvas for feedback"**, **"look at my notes on live canvas"**, **"check live canvas"**, or **"I left feedback on the canvas"** — they're telling you to read annotations (sticky notes and markers) from the canvas JSON and act on them.

This is a structured feedback loop. Notes and markers have text content and spatial coordinates. Artboards have routes, viewports, branches, and bounding boxes. By correlating positions, you can determine which artboard each annotation refers to — and therefore which page, viewport, and branch the feedback targets.

### The workflow

#### 1. Find the active canvas

Check for the canvas directory and find the most recently modified canvas JSON:

```bash
ls -lt {dir}/canvases/*.json | head -1
```

Or if you know the canvas name, fetch directly:

```bash
curl -s http://localhost:8888/api/canvases/{canvas-name}
```

#### 2. Read the canvas JSON

The response contains everything:

```json
{
  "branches": [
    {
      "branch": "main",
      "port": 3000,
      "screens": [
        { "name": "Desktop", "route": "/dashboard", "width": 1440, "height": 900 },
        { "name": "Mobile", "route": "/dashboard", "width": 390, "height": 844 }
      ]
    }
  ],
  "positions": {
    "artboard-0-0": { "x": 0, "y": 60 },
    "artboard-0-1": { "x": 1490, "y": 60 },
    "note-note-1706000000000-0": { "x": 1520, "y": 300 },
    "marker-marker-1706000000001-0": { "x": 200, "y": 500 }
  },
  "notes": [
    { "id": "note-1706000000000-0", "x": 1520, "y": 300, "text": "padding is way too tight here", "width": 220, "height": 160 }
  ],
  "markers": [
    { "id": "marker-1706000000001-0", "x": 200, "y": 500, "text": "1" }
  ]
}
```

#### 3. Correlate annotations to artboards

For each note and marker, determine which artboard it's closest to using bounding box proximity. The logic:

1. **Reconstruct artboard bounds** — each artboard's position comes from `positions["artboard-{branchIdx}-{screenIdx}"]` (falling back to the layout-computed defaults). The bounding box is `(x, y)` to `(x + width, y + height)`.

2. **Get annotation position** — a note's position is `positions["note-{id}"]` (falling back to `note.x, note.y`). Same pattern for markers with `"marker-{id}"`.

3. **Find nearest artboard** — for each annotation, compute distance to each artboard's bounding box. An annotation inside or overlapping an artboard's bounds has distance 0. Otherwise, use the shortest distance from the annotation's position to the artboard's rectangle edge.

4. **Build the feedback list** — each entry maps an annotation to its nearest artboard:

| Annotation | Text | Nearest Artboard | Branch | Route | Viewport |
|---|---|---|---|---|---|
| Note | "padding is way too tight here" | Mobile | main | /dashboard | 390x844 |
| Marker 1 | (no text beyond label) | Desktop | main | /dashboard | 1440x900 |

#### 4. Act on the feedback

For each annotation:

- **Notes with text** — the text is the feedback. Read it, understand the intent, locate the relevant code (using the route and viewport context), and make the fix.
- **Markers without descriptive text** — these are positional callouts. The marker's position relative to the artboard suggests roughly *where* on the page the issue is. Combine with any nearby notes for full context. If the intent is ambiguous, ask the user.
- **Multiple annotations on one artboard** — address them together if they relate to the same component or area. Keep the fixes scoped to what the annotations describe.

After making changes, tell the user to check the canvas — the artboard iframes will reflect the updates via hot reload.

### Example agent response

When the agent reads the canvas and finds annotations:

> I found 3 annotations on your canvas:
>
> 1. **Note near Mobile /dashboard (main):** "padding is way too tight here" — I'll look at the dashboard layout at mobile width and adjust spacing.
> 2. **Note near Desktop /settings (feature-x):** "this header overlaps the nav" — I'll check the header z-index and positioning on the settings page.
> 3. **Marker 1 near Tablet /dashboard (main):** No description — this is pointing at the sidebar area. Want me to look at something specific here?
>
> Fixing items 1 and 2 now. Let me know about marker 1.

### Notes on position data

- Positions in the `positions` map take precedence over the `x`/`y` stored directly on the note/marker object. The `positions` map is updated during drag operations. Always check `positions["note-{id}"]` first, fall back to `note.x, note.y`.
- Artboard positions follow the key format `artboard-{branchIdx}-{screenIdx}` where indices are zero-based, matching the order in the `branches` array.
- If no position entry exists for an artboard, use the default layout: artboards are arranged left-to-right within a branch row, with `SCREEN_GAP` (50px) between them, and branch rows are stacked vertically with `BRANCH_GAP` (120px) between them. The first artboard in the first branch starts at approximately `(0, 60)` after the branch label height.

---

## Creating Branches

When the user clicks **Prompt** in the canvas titlebar and copies the generated prompt, or asks directly for a branch comparison:

1. Read `references/variant-workflow.md` for the full step-by-step procedure
2. Key steps: create worktree → install deps → start dev server on new port → POST branch to canvas API → reload
3. After creating: tell the user to reload the canvas to see the new branch row

**Adding a branch via the API** (preferred over editing HTML):

```bash
# POST the updated canvas config to the server
curl -X POST http://localhost:8888/api/canvases/{canvas-name} \
  -H 'Content-Type: application/json' \
  -d '{ ... updated canvas JSON with new branch ... }'
```

The canvas will pick up changes on next page load or when the user switches canvases.

See `references/variant-workflow.md` for complete branch lifecycle including cleanup.

---

## Adding Design Tokens to the Canvas

Design token nodes are agent-driven — they're not created via the UI dropdown but by the agent analyzing the project's token files and writing data to the canvas JSON.

### When the user asks to add design tokens:

1. **Find token source** — look for CSS custom properties files, Tailwind config, theme JSON, SCSS variables, or similar. Ask the user to point you to the file if unclear.

2. **Parse tokens** — extract variable names and values, grouping into categories: `colors`, `spacing`, `typography`, `radius`, `shadows`, etc.

3. **Build the node data** — read an existing canvas JSON or the rendering code in `live-canvas.html` to confirm the current schema for design token nodes. The schema below is illustrative — field names and structure may have evolved:
   ```json
   {
     "id": "ds-<timestamp>",
     "x": 2000,
     "y": 100,
     "width": 380,
     "tokens": {
       "colors": { "--primary": "#2563eb", "--secondary": "#64748b" },
       "spacing": { "--spacing-sm": "8px", "--spacing-lg": "24px" },
       "typography": { "--font-size-sm": "14px", "--font-size-lg": "18px" },
       "radius": { "--radius-sm": "4px", "--radius-md": "8px" }
     },
     "modifications": {},
     "source": "src/styles/tokens.css"
   }
   ```

4. **Write to canvas JSON** — load the current canvas data, add the node to the `designNodes` array, POST back via `/api/canvases/{id}`:
   ```bash
   # Read current canvas
   curl http://localhost:8888/api/canvases/{canvas-name} > /tmp/canvas.json

   # Add design node to the JSON (use jq or edit in code)
   # Then POST back
   curl -X POST http://localhost:8888/api/canvases/{canvas-name} \
     -H 'Content-Type: application/json' \
     -d @/tmp/canvas.json
   ```

5. **Reload** — tell the user to reload the canvas to see the design token node

6. **Walk through** — explain how to use the node:
   - Tweak color values using the color picker swatches or by typing values (including `var(--other)` references) in the text input
   - Drag range sliders for spacing, typography, and radius values, or type directly in the text inputs
   - Modified tokens highlight in blue
   - Two paths for applying changes:
     - **Save** button — writes directly to the CSS source file via `POST /api/tokens`, triggering dev server hot reload, then reloads all artboard iframes after a short delay
     - **Prompt** button — copies a formatted prompt to clipboard for pasting to the agent
   - **Undo** button appears after saving, reverting to the pre-save state (single-level, session-only)
   - **Reset** button — re-reads all token values from the source file on disk, replacing the widget's baselines and clearing any pending modifications. Useful when external changes were made to the token file (by the agent, another tool, or git operations)

### Dual-path workflow

The design token node supports two complementary paths for applying changes:

| Path | Button | Best for |
|---|---|---|
| **Direct save** | Save | Rapid iteration — tweak a slider, see the change instantly across all viewports via hot reload + iframe refresh |
| **Copy prompt** | Prompt | Complex refactors — when you want the agent to apply changes alongside other code modifications |
| **Reset** | Reset | Sync widget to disk — re-reads current values from the CSS source file, clearing local edits and undo history |

**How direct save works:**
1. User tweaks token values using sliders, color pickers, or text inputs
2. Click **Save** — frontend POSTs to `/api/tokens` with the source file path and changed values
3. Server applies regex replacements to the CSS source file and writes it back
4. Dev server (Vite, Next.js, etc.) detects the file change and triggers hot reload
5. After a 600ms delay, the canvas reloads all artboard iframes so the new token values are reflected

**Security notes:** The `/api/tokens` endpoint runs on `localhost` with the same trust model as the dev server — no authentication needed. The `source` path must be absolute and the file must have a recognized extension (`.css`, `.scss`, `.less`, `.json`, `.js`, `.ts`, `.yaml`, `.yml`). The server validates existence and extension before writing.

**Undo:** After saving, an **Undo** button appears that reverts both the source file baselines and the modification state to their pre-save values. Undo is single-level (only the most recent save) and session-only (not persisted in the canvas JSON).

### Design token node categories

The canvas renders different controls based on category name:

| Category | Control | Visual |
|---|---|---|
| `colors` | Color picker swatch | Colored square with hex value |
| `spacing` | Text input | Proportional bar visualization |
| `typography` | Text input | "Aa" preview at the token's font size |
| `radius` | Text input | Square with the border-radius applied |

Categories are flexible — use whatever names match the project's token structure. Only the four names above get special visual treatments; other categories render as plain text inputs.

---

## Tailoring the Canvas

### Change the canvas server port

```bash
PORT=9999 python3 live-canvas/serve.py
```

### Change default screens in HTML

Search `live-canvas.html` for the default screens array (historically named `defaultScreens`) — these are the fallback viewports used when no `?canvas=` parameter is provided. Edit the array to match your preferred defaults:

```javascript
const defaultScreens = [
  { name: 'Desktop', route: '/', width: 1440, height: 900 },
  { name: 'Tablet',  route: '/', width: 768,  height: 1024 },
  { name: 'Mobile',  route: '/', width: 390,  height: 844 },
];
```

### Add custom preset viewports

Common device sizes to use in canvas configs:

| Device | Width | Height |
|---|---|---|
| iPhone SE | 375 | 667 |
| iPhone 15 Pro | 393 | 852 |
| iPad Mini | 768 | 1024 |
| iPad Pro 12.9" | 1024 | 1366 |
| MacBook Air 13" | 1440 | 900 |
| Desktop 1080p | 1920 | 1080 |
| Ultrawide | 2560 | 1080 |

### Edit canvas JSON directly

Canvas files are plain JSON in `{dir}/canvases/`. You can edit them directly — the server reads them on each request:

```bash
# List canvases
ls live-canvas/canvases/

# Edit a canvas
cat live-canvas/canvases/my-canvas.json
```

### Change the titlebar subtitle

Search `live-canvas.html` for the subtitle element in the titlebar (historically `#titlebar-subtitle`). You can edit it in the HTML, or let the canvas JSON `name` field override it when loaded via `?canvas=`.

---

## Starting Point Templates

Use these JSON structures when creating the initial `canvases/{name}.json` in Step 3. Replace placeholder values with project-specific config gathered in Step 2.

### Breakpoints

```json
{
  "name": "Breakpoints",
  "branches": [
    {
      "branch": "main",
      "port": 3000,
      "screens": [
        { "name": "Desktop", "route": "/", "width": 1440, "height": 900 },
        { "name": "Tablet", "route": "/", "width": 768, "height": 1024 },
        { "name": "Mobile", "route": "/", "width": 390, "height": 844 }
      ]
    }
  ]
}
```

### User Flow

```json
{
  "name": "User Flow",
  "branches": [
    {
      "branch": "main",
      "port": 3000,
      "screens": [
        { "name": "Login", "route": "/login", "width": 1440, "height": 900 },
        { "name": "Dashboard", "route": "/dashboard", "width": 1440, "height": 900 },
        { "name": "Settings", "route": "/settings", "width": 1440, "height": 900 }
      ]
    }
  ]
}
```

### Branch Comparison

```json
{
  "name": "Branch Comparison",
  "branches": [
    {
      "branch": "main",
      "port": 3000,
      "screens": [
        { "name": "Desktop", "route": "/", "width": 1440, "height": 900 },
        { "name": "Tablet", "route": "/", "width": 768, "height": 1024 },
        { "name": "Mobile", "route": "/", "width": 390, "height": 844 }
      ]
    },
    {
      "branch": "feature-x",
      "port": 3001,
      "screens": [
        { "name": "Desktop", "route": "/", "width": 1440, "height": 900 },
        { "name": "Tablet", "route": "/", "width": 768, "height": 1024 },
        { "name": "Mobile", "route": "/", "width": 390, "height": 844 }
      ]
    }
  ]
}
```

### Custom

For custom setups, build the JSON structure from the user's description. Each branch is a row on the canvas, and each screen within a branch is a column. Use the same schema:

```json
{
  "name": "<descriptive-name>",
  "branches": [
    {
      "branch": "<branch-name>",
      "port": "<port-number>",
      "screens": [
        { "name": "<label>", "route": "<path>", "width": "<w>", "height": "<h>" }
      ]
    }
  ]
}
```

**Note:** The canvas also accepts the legacy `"variants"` key for backward compatibility with older canvas JSON files, but always use `"branches"` for new canvases.

---

## Setup Flow

Follow these steps interactively. Each step has a human-in-the-loop checkpoint.

### Step 0 — Preflight

Detect the project environment before asking any questions:

1. **Read `package.json`** — extract `name` and `scripts.dev` (or `scripts.start`)
2. **Check for `git`** — run `git rev-parse --show-toplevel` to confirm it's a repo
3. **Find running dev servers** — `lsof -i :3000 -sTCP:LISTEN` (also check :5173, :8080 for Vite/other)
4. **Check for existing `live-canvas/` directory** — if found, skip to "Open Existing" flow below
5. **Report findings** to the user:
   > Found **my-app** (Next.js) with dev server on port 3000.
   > No existing live-canvas directory detected.

**Open Existing flow:** If `live-canvas/` already exists with `serve.py` and `canvases/`, ask the user if they want to launch the existing canvas or create a new one. To launch:
```bash
python3 live-canvas/serve.py &
open http://localhost:8888/live-canvas.html?canvas=<most-recent-json>
```

### Step 1 — Choose starting point

Use `AskUserQuestion` to ask what the canvas is for:

| Option | Description |
|---|---|
| **Breakpoints** (default) | Single page at Desktop / Tablet / Mobile viewports |
| **User flow** | Multiple routes at a single viewport (e.g., login → dashboard → settings) |
| **Branch comparison** | Same page across git branches/worktrees |
| **Custom** | User describes their own setup |

### Step 2 — Gather config

Based on the choice, ask targeted follow-up questions:

- **Breakpoints:** Which route? (default: `/`)
- **User flow:** Which routes? Which viewport? (default: Desktop 1440x900)
- **Branch comparison:** Which branches? (list from `git branch --list`)
- **For all:** What port is the dev server on? (use auto-detected port or ask)
- **For all:** Canvas directory name? (default: `live-canvas/`)

### Step 3 — Scaffold

Create the directory and files:

```
{dir}/
├── live-canvas.html    ← copied from skill templates/
├── canvas.css          ← copied from skill templates/
├── serve.py            ← copied from skill templates/
└── canvases/
    └── {canvas-name}.json   ← built from Step 2 answers
```

**File operations:**
1. Create `{dir}/` directory (default `live-canvas/`)
2. Copy `${CLAUDE_PLUGIN_ROOT}/skills/live-canvas/templates/live-canvas.html` → `{dir}/live-canvas.html`
3. Copy `${CLAUDE_PLUGIN_ROOT}/skills/live-canvas/templates/canvas.css` → `{dir}/canvas.css`
4. Copy `${CLAUDE_PLUGIN_ROOT}/skills/live-canvas/templates/serve.py` → `{dir}/serve.py`
5. Create `{dir}/canvases/` directory
6. Create `{dir}/canvases/{canvas-name}.json` using the appropriate Starting Point Template (see Section 6)
7. Add `live-canvas/` to `.gitignore` if not already present

**Tell the user after scaffolding:**
> I've added `live-canvas/` to `.gitignore` since canvases are personal dev tools. If you'd like to share the canvas setup with your team, you can remove that line.

### Step 4 — Launch

Start the server and open the browser:

```bash
python3 {dir}/serve.py &
open http://localhost:8888/live-canvas.html?canvas={canvas-name}
```

Confirm to the user that the canvas is running and ready.

### Updating to Latest Template

When the skill templates are updated (new features, bug fixes, UI improvements), existing canvases can pull the latest. Canvas data in `canvases/` is always preserved — only `serve.py`, `live-canvas.html`, and `canvas.css` are candidates for update.

**When the user asks to update** (e.g., "update my canvas to the latest template", "pull latest live-canvas changes"):

#### Step 1 — Detect local modifications

For each file (`serve.py`, `live-canvas.html`, `canvas.css`), diff the user's copy against the current template:

```bash
diff {dir}/serve.py ${CLAUDE_PLUGIN_ROOT}/skills/live-canvas/templates/serve.py
diff {dir}/live-canvas.html ${CLAUDE_PLUGIN_ROOT}/skills/live-canvas/templates/live-canvas.html
diff {dir}/canvas.css ${CLAUDE_PLUGIN_ROOT}/skills/live-canvas/templates/canvas.css
```

Three possible outcomes per file:

| Diff result | Meaning | Action |
|---|---|---|
| No differences | User hasn't customized this file | Safe to overwrite — `cp` the new template |
| Differences found | User has local modifications | Proceed to conflict resolution (Step 2) |

If both files have no local modifications, skip to Step 3.

#### Step 2 — Conflict resolution

When the user's copy has local modifications:

1. **Read both files** — the user's modified copy and the new template
2. **Identify the user's customizations** — compare against the template to find what the user changed. Common customizations:
   - `defaultScreens` array (different viewports)
   - Custom CSS additions (in `canvas.css`)
   - PORT constant changes
   - Additional JavaScript functions
3. **Present the conflicts** to the user using `AskUserQuestion`:
   - List each customized section and what the new template changes in that area
   - Offer options:
     - **Keep my changes** — preserve the user's version of that section, manually apply template improvements around it
     - **Take the update** — use the new template version, discard the user's customization
     - **Merge both** — apply the template update while preserving the user's customization (agent does this manually by editing the new template to re-add the user's changes)
4. **Apply the resolution** — write the final merged file

**Common non-conflicting updates** (safe to apply without asking):
- New CSS rules added to `canvas.css` (append-only, don't conflict with existing rules)
- New JavaScript functions added (append-only)
- New API endpoints in `serve.py` (append-only)
- Bug fixes to existing functions where the user hasn't modified that function

**Always ask about:**
- Changes to `defaultScreens` or any config constants
- Changes to functions the user has modified
- Structural changes to HTML layout

#### Step 3 — Apply and restart

```bash
# Kill existing server
lsof -i :8888 -sTCP:LISTEN -P 2>/dev/null | awk 'NR>1{print $2}' | xargs kill 2>/dev/null
sleep 0.5

# Start fresh
python3 {dir}/serve.py &
```

Tell the user to reload the canvas tab.

#### What's always preserved
- All canvas JSON files in `canvases/` (artboard layouts, design token nodes, sticky notes, positions)
- The `.gitignore` entry
- User customizations (via conflict resolution above)

#### What's updated
- `serve.py` — server code (API endpoints, static file serving)
- `live-canvas.html` — canvas UI (widgets, controls, JS logic)
- `canvas.css` — all visual styles (layout, theming, component chrome)

---

## Extending Token Widgets

The design token node renders different widget controls per category. Before extending, read the render function for design token nodes in `live-canvas.html` to confirm the current widget pattern and function names. Historically each widget follows the same pattern: **visual preview** + **control input(s)** + a token-update callback.

### Built-in widgets

| Category | Visual preview | Control | Range |
|---|---|---|---|
| `colors` | Color swatch | Color picker + text input | N/A |
| `spacing` | Proportional bar | Range slider (0–128) + text input | `0–128px` |
| `typography` | "Aa" at font size | Range slider (8–72) + text input | `8–72px` |
| `radius` | Single-corner preview | Range slider (0–48) + text input | `0–48px` |

### The widget pattern

Every widget row follows this structure:

```html
<div class="token-row ${modified ? 'modified' : ''}">
  <!-- 1. Visual preview (category-specific) -->
  <div class="token-spacing-bar" style="width:${numVal * 2}px"></div>

  <!-- 2. Token name -->
  <span class="token-name">${name}</span>

  <!-- 3. Controls (slider + input, or just input) -->
  <div class="token-controls">
    <input type="range" min="0" max="128" step="1" value="${numVal}"
      oninput="updateTokenFromSlider('${nodeId}','${name}',this.value,'${unit}','${originalValue}')" />
    <input type="text" value="${current}"
      onchange="updateToken('${nodeId}','${name}',this.value,'${originalValue}')" />
  </div>
</div>
```

Both controls read from the same modifications state. The `oninput`/`onchange` handlers call the token-update functions (historically `updateToken()` and `updateTokenFromSlider()` — verify the current names in `live-canvas.html`), triggering a re-render that keeps both controls in sync.

### Adding new widget types

To add a new widget type (e.g., flexbox direction, component props), find the function that renders design token nodes in `live-canvas.html` and add a new category block following the pattern of the existing category blocks.

**Flexbox example** — a dropdown `<select>` for `flex-direction`:

```javascript
if (dn.tokens.flexbox) {
  let rows = '';
  for (const [name, value] of Object.entries(dn.tokens.flexbox)) {
    const current = (dn.modifications || {})[name] ?? value;
    const modified = (dn.modifications || {})[name] !== undefined;
    const options = ['row', 'column', 'row-reverse', 'column-reverse'];
    const optionsHTML = options.map(opt =>
      `<option value="${opt}" ${current === opt ? 'selected' : ''}>${opt}</option>`
    ).join('');
    rows += `
      <div class="token-row ${modified ? 'modified' : ''}">
        <span class="token-name">${name}</span>
        <div class="token-value">
          <select onchange="updateToken('${dn.id}','${name}',this.value,'${value}')">
            ${optionsHTML}
          </select>
        </div>
      </div>`;
  }
  sectionsHTML += `<div class="design-node-section">
    <div class="design-node-section-title">Flexbox</div>${rows}</div>`;
}
```

Add matching CSS to `canvas.css` for dropdown styling:

```css
.token-value select {
  width: 100%;
  background: #151515;
  border: 1px solid var(--chrome-border);
  border-radius: 4px;
  color: var(--text);
  font-family: var(--mono);
  font-size: 12px;
  padding: 2px 6px;
  outline: none;
  cursor: pointer;
}
.token-value select:focus { border-color: var(--accent); }
```

**Component props example** — range sliders for button sizes, card padding:

Add tokens to the node data with a `components` category:
```json
{
  "tokens": {
    "components": {
      "--btn-padding-x": "16px",
      "--btn-padding-y": "8px",
      "--card-padding": "24px",
      "--card-shadow-blur": "16px"
    }
  }
}
```

These will render with the default text input. To add sliders, find the existing spacing widget block in the design-token render function and add a matching block with appropriate min/max ranges.

---

## Adding Custom Widgets

A **custom widget node** is a draggable, persistent canvas panel with its own content — independent of the design-token system. Use this pattern when you need a new type of canvas element (e.g., a color palette grid, a component checklist, a performance dashboard, an accessibility audit panel). If your goal is to add a new *token category* to an existing design-token node, use the [Extending Token Widgets](#extending-token-widgets) section instead.

Every node type on the canvas follows the same structural contract: a data array, a render function, persistence hooks, minimap/fitAll integration, drag support, and delete handling. This section documents each step with illustrative code snippets.

> **Before implementing:** Read `live-canvas.html` first. Search for each pattern described below — the function names, variable names, and structure may have changed since this was written. Use the existing node types (notes, design token nodes, frames) as your ground truth, not this document. The code snippets here are templates showing the *shape* of each integration point, not copy-paste targets.

### 1. Data model

Search `live-canvas.html` for the top-level arrays (e.g. look for where note, frame, and design-token arrays are declared). Add a new array and ID generator following the same pattern.

```javascript
// Custom widget nodes — adapt naming to match the codebase convention
const widgetNodes = [];
let widgetIdCounter = 0;
function generateWidgetId() { return `wn-${Date.now()}-${widgetIdCounter++}`; }
```

**Minimum node shape:**

```javascript
{
  id: "wn-1706000000000-0",   // unique ID with prefix
  x: 2000,                     // initial canvas X
  y: 400,                      // initial canvas Y
  // ... widget-specific fields
}
```

**Prefix convention** — each node type uses a unique prefix as its drag key. Read the drag mouseup handler to see which prefixes are already in use (historically: `label-`, `artboard-`, `note-`, `frame-`, `ds-`). Choose a prefix that won't collide.

### 2. Render function

Search for the existing render functions (e.g. the one that renders sticky notes or design-token nodes). The typical pattern is:

1. **Cleanup** existing elements by class selector (allows standalone re-render without a full `render()` pass)
2. **Create element**, set `className` and `dataset.dragKey`
3. **Position** via the positions map with fallback to stored `node.x`/`node.y`
4. **Header** with `data-drag-handle` — the global drag system picks this up automatically
5. **Body** with widget-specific content
6. **Append** to canvas

```javascript
function renderWidgetNodes() {
  // 1. Cleanup — targeted removal, not a full canvas wipe
  canvas.querySelectorAll('.widget-node').forEach(el => el.remove());

  widgetNodes.forEach(wn => {
    // 2. Create element
    const el = document.createElement('div');
    el.className = 'widget-node';
    el.dataset.dragKey = `wn-${wn.id}`;

    // 3. Position — runtime drag positions override stored coordinates
    el.style.left = (positions[`wn-${wn.id}`]?.x ?? wn.x) + 'px';
    el.style.top  = (positions[`wn-${wn.id}`]?.y ?? wn.y) + 'px';

    // 4. Header with drag handle + close button
    // 5. Widget-specific body content
    el.innerHTML = `
      <div class="widget-node-header" data-drag-handle>
        <span class="widget-node-title">${wn.title || 'Widget'}</span>
        <button class="design-node-close" onclick="deleteWidgetNode('${wn.id}')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>
      <div class="widget-node-body">
        <!-- widget-specific content here -->
      </div>
    `;

    // 6. Append to canvas
    canvas.appendChild(el);
  });
}
```

**Why cleanup-before-render:** This pattern lets you call the render function standalone (e.g. after a user interaction updates widget state) without triggering a full `render()` cycle. Confirm the existing renderers still use this pattern before following it.

### 3. Persistence

Three persistence touch points need changes. Search for each by looking at how existing node arrays are handled.

**Save function** — find where the canvas payload is built (search for the `fetch` POST to the canvas API). Add the new array to the payload alongside the existing ones:

```javascript
const payload = {
  // ... existing fields ...
  widgetNodes: widgetNodes.map(wn => ({ ...wn })),
};
```

**Load function** — find where canvas data is deserialized from the API response. Add a block that clears and repopulates the array, using an `|| []` guard for backward compatibility with older saved canvases:

```javascript
// Load widget nodes
widgetNodes.length = 0;
(data.widgetNodes || []).forEach(wn => widgetNodes.push(wn));
```

**New canvas function** — find where arrays are reset when creating a fresh canvas. Add a reset for the new array, matching whatever pattern the existing arrays use (historically `.length = 0` to mutate in place):

```javascript
widgetNodes.length = 0;
```

### 4. Minimap and fitAll

The fitAll and minimap functions iterate over every node type to calculate canvas bounds. Search for where the existing node-type loops are in each function, and add a matching block.

**fitAll** — add a `forEach` that expands the bounding box:

```javascript
widgetNodes.forEach(wn => {
  const wx = positions[`wn-${wn.id}`]?.x ?? wn.x;
  const wy = positions[`wn-${wn.id}`]?.y ?? wn.y;
  if (wx < minX) minX = wx;
  if (wy < minY) minY = wy;
  if (wx + (wn.width || 320) > maxX) maxX = wx + (wn.width || 320);
  if (wy + (wn.height || 250) > maxY) maxY = wy + (wn.height || 250);
});
```

**Minimap** — add a visual representation, matching the existing minimap element pattern:

```javascript
widgetNodes.forEach(wn => {
  const wx = positions[`wn-${wn.id}`]?.x ?? wn.x;
  const wy = positions[`wn-${wn.id}`]?.y ?? wn.y;
  const x = (wx - minX) * mmScale;
  const y = (wy - minY) * mmScale;
  const w = (wn.width || 320) * mmScale;
  const h = (wn.height || 250) * mmScale;
  html += `<div class="minimap-widget-node" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;"></div>`;
});
```

Add matching CSS to `canvas.css` for the minimap dot (adapt variable names to match existing minimap CSS):

```css
.minimap-widget-node {
  position: absolute;
  background: rgba(168, 85, 247, 0.25);  /* distinct color from other node types */
  border-radius: 1px;
}
```

### 5. render() integration

Find the main `render()` function — it calls the individual render functions in sequence. Add a call to the new render function in the same block. Verify the call order by reading what's already there.

### 6. Drag integration

The global drag system uses the `data-drag-handle` attribute and `dataset.dragKey` — no extra wiring is needed for basic drag. However, you must persist the drag position on mouseup. Find the drag mouseup handler (search for where other prefixes like `note-` or `ds-` are handled) and add a block for the new prefix:

```javascript
if (dragKey && dragKey.startsWith('wn-')) {
  const wnId = dragKey.replace('wn-', '');
  const wn = widgetNodes.find(n => n.id === wnId);
  if (wn) {
    wn.x = positions[dragKey]?.x ?? wn.x;
    wn.y = positions[dragKey]?.y ?? wn.y;
  }
}
```

### 7. Delete function

Search for the existing delete functions (e.g. the one that deletes a note or design-token node). The typical pattern is: confirm → splice from array → delete positions entry → render + save.

```javascript
function deleteWidgetNode(nodeId) {
  if (!confirm('Remove this widget?')) return;
  const idx = widgetNodes.findIndex(n => n.id === nodeId);
  if (idx !== -1) {
    widgetNodes.splice(idx, 1);
    delete positions[`wn-${nodeId}`];
    render();
    saveCanvas();
  }
}
```

### 8. Add function

Search for how existing nodes are created (e.g. how a note or frame is added). The typical pattern is: convert screen center to canvas coordinates, push a new object to the array, render, and save. Optionally wire to a button in the Add dropdown menu if one exists.

```javascript
function addWidgetNode() {
  const center = screenToCanvas(window.innerWidth / 2, window.innerHeight / 2);
  widgetNodes.push({
    id: generateWidgetId(),
    x: center.x - 160,   // offset by half the widget width to center it
    y: center.y - 125,
    title: 'My Widget',
    // ... widget-specific fields
  });
  render();
  saveCanvas();
}
```

### 9. CSS

Find the CSS for an existing draggable node type in `canvas.css` (e.g. the design-token node styles) and use it as the visual template for consistent chrome (background, border, shadow, border-radius). Adapt variable names and class names to match the actual stylesheet. Add new styles to `canvas.css`. Customize the body styles per widget.

```css
.widget-node {
  position: absolute;
  width: 320px;
  background: var(--chrome-bg);
  border: 1px solid var(--chrome-border);
  border-radius: var(--radius-lg);
  z-index: 40;
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  font-family: var(--font);
}
.widget-node:hover .design-node-close { opacity: 1; }
.widget-node-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--chrome-border);
  cursor: grab;
}
.widget-node-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}
.widget-node-body {
  padding: 12px 16px;
}
```

### Checklist

When implementing a custom widget, read the actual `live-canvas.html` first, then verify every integration point:

- [ ] Top-level array and ID generator declared (find existing arrays as reference)
- [ ] Render function with cleanup → create → position → header → body → append
- [ ] Save function includes the array in the payload (find the save/POST logic)
- [ ] Load function deserializes with fallback guard (find the load/GET logic)
- [ ] New-canvas function resets the array (find the reset logic)
- [ ] fitAll includes a `forEach` block with estimated width/height
- [ ] Minimap includes a `forEach` block with minimap element
- [ ] Main render function calls the new render function
- [ ] Drag mouseup handler persists position for the new prefix
- [ ] Delete function: confirm → splice → delete position → render + save
- [ ] Add function: center coordinates → push → render + save
- [ ] CSS added to `canvas.css` for the node and its minimap representation

---

## API Reference

### `GET /api/canvases`

List all saved canvases.

**Response:** `200 OK`
```json
[
  { "id": "my-canvas", "name": "My Canvas" }
]
```

### `GET /api/canvases/{id}`

Load a canvas by ID.

**Response:** `200 OK` — full canvas JSON
**Response:** `400` — invalid canvas name
**Response:** `404` — canvas not found

### `POST /api/canvases/{id}`

Save a canvas. Body is the full canvas JSON object.

**Response:** `200 OK` — `{"ok": true}`
**Response:** `400` — invalid canvas name or invalid JSON

### `DELETE /api/canvases/{id}`

Delete a canvas by ID.

**Response:** `200 OK` — `{"ok": true}`
**Response:** `400` — invalid canvas name

### `POST /api/tokens/read`

Read current token values from a CSS source file. Used by the widget's **Reset** button to sync baselines with what's on disk.

**Request:**
```json
{
  "source": "/absolute/path/to/tokens.css",
  "names": ["--color-primary", "--spacing-sm"]
}
```

| Field | Type | Description |
|---|---|---|
| `source` | string | **Absolute path** to the token source file |
| `names` | array | List of CSS custom property names to read |

**Response:** `200 OK`
```json
{ "ok": true, "tokens": { "--color-primary": "#2563eb", "--spacing-sm": "8px" }, "file": "/absolute/path/to/tokens.css" }
```

Token names not found in the file are silently omitted from the response.

**Error responses:** Same as `POST /api/tokens` (400, 404, 422, 500).

### `POST /api/tokens`

Write design token changes directly to a CSS source file.

**Request:**
```json
{
  "source": "/absolute/path/to/tokens.css",
  "changes": [
    { "name": "--color-primary", "value": "#ff0000" },
    { "name": "--spacing-sm", "value": "12px" }
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `source` | string | **Absolute path** to the token source file |
| `changes` | array | List of `{name, value}` pairs to update |

**Response:** `200 OK`
```json
{ "ok": true, "updated": 2, "file": "/absolute/path/to/tokens.css" }
```

**Error responses:**

| Status | Condition | Body |
|---|---|---|
| `400` | Missing `source` or `changes`, or invalid JSON | `{"error": "..."}` |
| `404` | Source file does not exist | `{"error": "file not found: ..."}` |
| `422` | Unrecognized file extension | `{"error": "unrecognized file extension '...'", "allowed": [...]}` |
| `500` | File read/write I/O error | `{"error": "read error: ..."}`  or `{"error": "write error: ..."}` |

**Regex pattern:** The server matches CSS custom property declarations using `(--token-name\s*:\s*)[^;]+(;)` and replaces the value portion between the colon and semicolon.

**Security model:** Runs on `localhost` only. Same trust boundary as the dev server — no authentication. Paths must be absolute. File extension is validated against an allowlist: `.css`, `.scss`, `.less`, `.json`, `.js`, `.ts`, `.yaml`, `.yml`.

### `GET /api/file?path=<absolute-path>`

Serve a local file by absolute path with correct Content-Type. Used by image, video, and audio file nodes to display media on the canvas, and can also serve text files.

**Query parameters:**

| Param | Type | Description |
|---|---|---|
| `path` | string | **Absolute path** to the file to serve |

**Response:** Binary data with appropriate `Content-Type` header for images (`.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`, `.ico`, `.bmp`), or `text/plain; charset=utf-8` for text files. Includes `Cache-Control: no-cache` and `Access-Control-Allow-Origin: *`.

For video files (`.mov`, `.mp4`, `.webm`, `.ogg`, `.m4v`, `.avi`) and audio files (`.mp3`, `.wav`, `.aac`, `.m4a`, `.flac`), the server supports `Accept-Ranges: bytes` and returns `206 Partial Content` for Range requests, enabling video seeking and audio scrubbing in the browser.

**Error responses:**

| Status | Condition | Body |
|---|---|---|
| `400` | Missing `path` query parameter | `{"error": "missing 'path' query parameter"}` |
| `404` | File does not exist | `{"error": "file not found: ..."}` |
| `422` | Unrecognized file extension | `{"error": "unrecognized file extension '...'", "allowed": [...]}` |
| `500` | File read I/O error | `{"error": "read error: ..."}` |

### `POST /api/file/read`

Read full text content of a file. Used by file nodes to load/resync file content into the editor.

**Request:**
```json
{
  "source": "/absolute/path/to/file.css"
}
```

| Field | Type | Description |
|---|---|---|
| `source` | string | **Absolute path** to the text file to read |

**Response:** `200 OK`
```json
{ "ok": true, "content": "/* file contents */", "file": "/absolute/path/to/file.css" }
```

**Error responses:** Same as `GET /api/file` (400, 404, 422, 500). Only text file extensions are allowed.

### `POST /api/file`

Write text content to an existing file. Used by the file node Save button.

**Request:**
```json
{
  "source": "/absolute/path/to/file.css",
  "content": "/* updated contents */"
}
```

| Field | Type | Description |
|---|---|---|
| `source` | string | **Absolute path** to the text file to write |
| `content` | string | The full text content to write (empty string allowed) |

**Response:** `200 OK`
```json
{ "ok": true, "file": "/absolute/path/to/file.css" }
```

**Error responses:** Same as `POST /api/file/read`. Will not create new files — the file must already exist on disk.
