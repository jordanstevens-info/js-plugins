# Variant Workflow

Complete guide for adding, managing, and cleaning up branch variants in a Live Canvas.

A **variant** is a row on the canvas showing the app running from a different git branch. Each variant has its own worktree, dev server on a unique port, and set of artboard screens.

---

## Adding a Variant

### 1. Detect package manager

Before creating the worktree, detect which package manager the project uses:

```bash
# Check for lockfiles (in priority order)
if [ -f pnpm-lock.yaml ]; then
  PKG_MGR="pnpm"
elif [ -f yarn.lock ]; then
  PKG_MGR="yarn"
elif [ -f package-lock.json ]; then
  PKG_MGR="npm"
else
  PKG_MGR="npm"  # fallback
fi
```

### 2. Select a port

Pick the next available port starting from one above the highest existing variant port:

```bash
# Find next available port (start from 3001, skip occupied)
NEXT_PORT=3001
while lsof -i :$NEXT_PORT -sTCP:LISTEN >/dev/null 2>&1; do
  NEXT_PORT=$((NEXT_PORT + 1))
done
echo "Using port: $NEXT_PORT"
```

### 3. Create the git worktree

```bash
# From the main project root
PROJECT_NAME=$(basename $(pwd))
BRANCH_NAME="feature/my-variant"
WORKTREE_DIR="../${PROJECT_NAME}-${BRANCH_NAME##*/}"

# Create worktree from existing branch
git worktree add "$WORKTREE_DIR" "$BRANCH_NAME"

# OR create worktree with new branch
git worktree add -b "$BRANCH_NAME" "$WORKTREE_DIR"
```

### 4. Install dependencies

```bash
cd "$WORKTREE_DIR"

# Use the detected package manager
case $PKG_MGR in
  pnpm)  pnpm install ;;
  yarn)  yarn install ;;
  npm)   npm install ;;
esac
```

### 5. Start the dev server on the assigned port

```bash
# Next.js
PORT=$NEXT_PORT pnpm dev &

# Vite
pnpm dev --port $NEXT_PORT &

# Create React App
PORT=$NEXT_PORT pnpm start &
```

Verify the server is running:
```bash
# Wait for port to become available
for i in {1..30}; do
  curl -s http://localhost:$NEXT_PORT >/dev/null 2>&1 && break
  sleep 1
done
```

### 6. Add the variant to the canvas

**Preferred method — via the server API:**

Read the current canvas, add the new variant, and POST it back:

```bash
CANVAS_NAME="my-canvas"
CANVAS_PORT=8888  # the live-canvas server port

# Fetch current canvas config
CURRENT=$(curl -s http://localhost:$CANVAS_PORT/api/canvases/$CANVAS_NAME)

# Add new variant (use jq or build JSON manually)
# The new variant should copy the screens array from the first variant,
# changing only branch and port
UPDATED=$(echo "$CURRENT" | jq --arg branch "$BRANCH_NAME" --argjson port $NEXT_PORT \
  '.variants += [{"branch": $branch, "port": $port, "screens": .variants[0].screens}]')

# Save updated canvas
curl -X POST "http://localhost:$CANVAS_PORT/api/canvases/$CANVAS_NAME" \
  -H 'Content-Type: application/json' \
  -d "$UPDATED"
```

**Alternative — without jq**, build the POST body programmatically or use the `addVariant()` function in the canvas UI.

### 7. Reload the canvas

Tell the user to reload the canvas browser tab, or the agent can navigate:
```bash
open "http://localhost:$CANVAS_PORT/live-canvas.html?canvas=$CANVAS_NAME"
```

---

## Updating an Existing Variant

To modify a variant's screens (add/remove artboards, change routes):

```bash
# Fetch → modify → POST back
curl -s http://localhost:8888/api/canvases/my-canvas \
  | jq '.variants[1].screens += [{"name":"New Page","route":"/new","width":1440,"height":900}]' \
  | curl -X POST http://localhost:8888/api/canvases/my-canvas \
    -H 'Content-Type: application/json' -d @-
```

Or edit the JSON file directly at `live-canvas/canvases/my-canvas.json` — changes are picked up on next canvas load.

---

## Removing a Variant

### 1. Stop the dev server

```bash
# Kill the process on the variant's port
kill $(lsof -ti:3001)
```

### 2. Remove from canvas config

```bash
# Remove variant at index 1 (0-indexed)
curl -s http://localhost:8888/api/canvases/my-canvas \
  | jq 'del(.variants[1])' \
  | curl -X POST http://localhost:8888/api/canvases/my-canvas \
    -H 'Content-Type: application/json' -d @-
```

### 3. Remove the worktree

```bash
# From the main project root
git worktree remove ../project-name-variant-branch

# If it's dirty and you're sure:
git worktree remove --force ../project-name-variant-branch

# Clean up worktree tracking
git worktree prune
```

---

## Managing Multiple Variants

When running several variants simultaneously:

### Port allocation convention

| Variant | Port |
|---|---|
| main (primary dev server) | 3000 |
| Variant 1 | 3001 |
| Variant 2 | 3002 |
| Variant 3 | 3003 |

### List active worktrees and servers

```bash
# All worktrees
git worktree list

# All dev servers (listening on 3000+ range)
lsof -i :3000-3010 -sTCP:LISTEN

# All node dev servers
ps aux | grep -E "(next|vite|react-scripts)" | grep -v grep
```

### Teardown all variants

When done with the canvas session:

```bash
# Stop all variant dev servers (keep port 3000 main server)
for port in $(seq 3001 3010); do
  pid=$(lsof -ti:$port 2>/dev/null)
  [ -n "$pid" ] && kill $pid
done

# Remove all worktrees (except main)
git worktree list --porcelain | grep "^worktree " | grep -v "$(pwd)" | while read -r _ path; do
  git worktree remove "$path" 2>/dev/null
done
git worktree prune

# Stop the canvas server
kill $(lsof -ti:8888 2>/dev/null)
```

---

## Tips

- **Worktrees share the git repo** — commits, branches, and stashes are all visible across worktrees. Only the working directory is separate.
- **Don't checkout the same branch in two worktrees** — git prevents this. Each worktree must be on a unique branch.
- **Dependency caches** — `node_modules/` is separate per worktree, but pnpm's global store is shared, so installs are fast.
- **Hot reload works** — changes in a worktree trigger hot reload on that worktree's dev server only. The canvas iframe will update automatically.
- **Port conflicts** — if a port is already in use, the dev server will fail to start. Always check with `lsof` before assigning.
