# Ticket Structure Reference

## Section-by-Section Guide

### User Story

Standard format. Keep it about the user's goal, not the implementation.

```
As a [role],
I want [outcome]
so that [benefit].
```

---

### Design Reference

Link to all available design artifacts. These are the visual spec — the ticket
points to them rather than duplicating their content.

**Possible artifacts (include whatever exists):**

| Artifact | What to link | Framing |
|---|---|---|
| Design branch | GitLab/GitHub tree URL + change log links | "Working prototype — match the design intent, reimplement to production standards" |
| Figma file | Figma URL (with node-id if specific frames) | "Source design — refer to for layout, spacing, and component structure" |
| Confluence spec | Confluence page URL | "Requirements doc — refer to for business context and constraints" |
| Other | Slack threads, screenshots, Loom recordings | Brief description of what context it provides |

**Principles:**
- Link, don't embed — the artifacts are living documents, the ticket shouldn't
  duplicate or screenshot them
- One-line framing per artifact so the reader knows what to expect when they
  click through
- If multiple artifacts exist, list them all — the team will decide which ones
  matter for their work

---

### Feature Specification

Describe *what* the feature is — structure, data, and behavior. This section
answers the questions that come up during grooming.

**Common subsections (use only what applies):**

| Subsection | Purpose | Example |
|---|---|---|
| Placement | Where does this render in the UI? | "Below each Scan Insights chart" |
| Data Source | Where does the data come from? | "Derives from existing API response, no new calls" |
| Columns / Fields | What data is shown? | Table with column name, description, alignment |
| Sorting / Filtering | How is data organized? | "Client-side, default sort by X descending" |
| Color System | What colors map to what? | "In=green, Out=red" (no Tailwind classes) |
| States | Loading, empty, error states | "Show skeleton rows while loading" |

**Principles:**
- Describe outcomes, not implementations
- Include enough detail that the team can groom the ticket without needing to
  run the design artifacts first
- If the prototype includes something that should NOT be built, call it out in
  Out of Scope instead

**Design system specifics belong here.** Token values, DS components, and
foundation patterns are design decisions — they're what the design *is*, not
how to implement it. Preserve them in the spec:

| Keep (design spec) | Remove (implementation detail) |
|---|---|
| "Use the `success` color token" | "Add `text-green-600`" |
| "Use the DS `Accordion` component" | "Use CSS grid with 0fr/1fr trick" |
| "Spacing: `space-4` token" | "Add `p-4` Tailwind class" |
| "Typography: `heading-sm` token" | "Add `text-sm font-semibold`" |

If the design uses a specific token or DS component, name it. If it uses a
raw color or ad-hoc styling, describe the intent ("green, readable in both
light and dark modes") and let the team map it to the right token.

---

### Acceptance Criteria

Observable outcomes. Each criterion should be something anyone can verify by
looking at the feature.

**Writing AC:**
- Start with the observable behavior, not the implementation
- Include accessibility requirements inline (aria attributes, keyboard navigation)
- Group related criteria under labeled sections (3-5 sections is ideal)
- Each section should have 3-6 bullet points

**Good AC language:**
- "Collapsed by default"
- "Header reads `Table (N)` where N is the total row count"
- "Toggle via click, Enter, or Space"
- "Does not overflow the viewport"

**Bad AC language (too prescriptive):**
- "Use CSS grid with gridTemplateRows: 0fr/1fr"
- "Implement with TanStack Table serverSide={false}"
- "Add text-green-600 dark:text-green-400 classes"
- "Build a useScanAggregateData hook"

**Bad AC language (not observable):**
- "Should look good"
- "Works correctly"
- "Remains unchanged"

---

### Out of Scope

Explicitly list what the prototype includes or what's adjacent to this work but
should NOT be part of this ticket. Prevents scope creep and sets expectations
during grooming.

**Format:** Bullet list with parenthetical context for each item.

```
- react-icons type cleanup (separate tech debt ticket)
- Avg/Hr column (present in prototype, deferred)
- Breakout table ins/outs (separate story)
```

---

### Known Constraints

Gotchas that would surface during grooming or implementation. NOT instructions
for how to handle them — just awareness.

**Include:**
- Pre-existing bugs or tech debt that affect this work
- Resources that already exist on the design branch (i18n keys, test fixtures)
- External dependencies or blockers

**Do not include:**
- How to solve the constraint
- Implementation patterns from the prototype
- Architecture recommendations
- Testing strategies
- Breakdown suggestions

**Example:**
```
- The react-icons package has 75+ pre-existing TS declaration errors.
  The prototype works around this — be aware when choosing an icon approach.
```

Note: "be aware when choosing" not "use inline SVG".
