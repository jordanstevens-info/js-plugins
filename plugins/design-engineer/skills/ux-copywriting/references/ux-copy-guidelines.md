# FGT UX Copy Guidelines

Version 1.0 | Last updated: Sep 18, 2025

**Purpose**: Single source of truth for planning, writing, reviewing, and evaluating interface copy across all Front Gate Tickets applications.

**Applies to**:

- Internal operations apps: Backstage, Admit One, Thundercat
- Consumer-facing experiences: Ecomm native app, B2C marketing site
- Client-facing tools: B2B portal and partner workflows
- Shared system communications: notification services, transactional email triggers, support macros

## 1. How to Use These Guidelines

- **Writers/designers**: Reference global standards first, then layer on app-specific guidance before drafting.
- **Engineers**: Use the component patterns and checklists to validate strings before implementation.
- **Product & QA**: Apply the review workflow checklist to approve copy changes across releases.

## 2. Brand Voice & Tone System

Front Gate copy should feel like a trusted backstage lead: confident, calm under pressure, and genuinely helpful. Maintain a human, conversational voice, and tune tone based on audience, urgency, and channel.

### Voice Attributes

| Attribute | Description | Do | Avoid |
|---|---|---|---|
| Trusted | Conveys reliability and operational confidence without sounding rigid. | State facts, cite data sources, acknowledge when we will follow up. | Promise outcomes we cannot control or hedge with "should" and "might" when certainty exists. |
| Efficient | Respects users' time by removing friction and extra words. | Lead with the action, surface only the information needed to decide. | Pad sentences with filler or repeat the UI label in helper text. |
| Approachable | Keeps language friendly and human, even in complex workflows. | Use contractions, familiar verbs, and plain language. | Slip into slang, jokes, or sarcasm — especially in client or error flows. |
| Inclusive | Welcomes every fan, staff member, and client. | Use person-first language, offer context for accessibility needs, honor chosen names and pronouns. | Reference assumptions about ability, gender, or economic status. |

### 2.1 Tone Modulation Matrix

Use this matrix to calibrate tone by scenario. Flag strings that drift outside the recommended tone or emotional range.

| Scenario | Primary Tone | Guardrails | Example — Do | Example — Avoid |
|---|---|---|---|---|
| Happy path flows (all apps) | Efficient, upbeat | Never becomes playful or casual at the expense of clarity. | "Add VIP parking" | "Would you like to add the VIP Parking package today?" |
| Transactional confirmations | Direct, reassuring | Dial up warmth when money or compliance is involved. | "Payment received. Seats 104–106 are locked in." | "Awesome! Your order is good to go!!!" |
| Warnings & recoverable errors | Calm, solution-oriented | Shift to urgent only when there is real risk. | "Card declined. Try another payment or contact your bank." | "Invalid payment details!" |
| Critical incidents (internal) | Commanding, precise | Acknowledge downstream impact and next steps. | "Gate 3 scanners offline. Switch to handheld backup." | "There is an issue with some scanners." |
| Support & education moments | Empathetic, encouraging | Offer context and link to learning resources. | "Need help choosing seats? Compare sightlines in the map." | "Not sure what to do? Read the guide." |
| Empty states & upsells | Inviting, value-led | Keep copy optional and respectful. | "No upgrades yet. Explore premium add-ons." | "You have not purchased any add-ons. Fix that now!" |

## 3. Global Writing Fundamentals

### 3.1 Design + Content Work Together

- Write with the component in mind. If the UI pattern can succeed without helper copy, remove the helper copy.
- Leverage icons and layout before adding words; flag redundant text beside universally known icons.
- Front-load the action. Lead with "Download guest list" rather than "You can download the guest list here."

### 3.2 Keep It Lean

- Choose the shortest phrasing that preserves meaning. Target fewer than 45 characters for CTAs and fewer than 120 characters for helper text where possible.
- Remove duplicate nouns. If the field label is "Delivery method," the helper copy should not repeat "Your delivery method…".
- Limit modal body copy to one actionable thought; move secondary guidance into links or tooltips.

### 3.3 Sound Like Our Audiences

- Use plain language and contractions. Prefer "We'll email your tickets" over "Tickets will be emailed."
- Respect domain knowledge. Internal tools can reference inventory IDs or settlements; consumer flows should never expose internal jargon.
- Keep reading levels accessible: Grade 6–7 for consumer experiences, Grade 8–10 for internal and B2B content.

### 3.4 Inspire Action

- Every interaction should make the next step obvious. If there is more than one possible action, rank them by priority.
- Lead sentences and tooltips with verbs ("Review holds", "Update payout details").
- Break multi-step processes into progressive disclosure. Do not present more than three instructions in a single paragraph.

### 3.5 Transparency Builds Trust

- Tell users what is happening behind the scenes only when it affects them. Otherwise, stay focused on the action they can take.
- Declare data sources and update cadences for analytics modules.
- State when follow-up is required, including how long it will take ("We'll confirm seat maps within 1 business day.").

## 4. Grammar, Mechanics, and Formatting

- **Sentence case** for all headings, buttons, and navigation.
- **Contractions**: Use them ("Don't", "You'll") unless legal compliance requires formal tone.
- **Active voice**: Subject + verb + object keeps instructions clear.
- **Ampersands**: Avoid unless space constrained in navigation. Use "and".
- **Numbers**: Spell out zero through nine in narrative copy; use numerals for time, dates, money, and measurements.
- **Currency**: Precede with the appropriate symbol and include space before three-letter codes (e.g., "CA $45", "USD 35").
- **Time**: Use local time zones with abbreviations on first mention ("Gates open at 5:30 p.m. CT").
- **Lists**: Use parallel structure. Start each bullet with the same part of speech and keep lengths similar.

## 5. Accessibility and Inclusive Language

- Describe actions rather than abilities ("Guests using wheelchairs can access Gate 2").
- Provide alt text that communicates function ("Download CSV"). Leave decorative imagery blank (`alt=""`).
- Avoid gendered language. Refer to "guests," "fans," "team members," or "clients."
- When voice or automated calls are mentioned, offer a text-based alternative.
- Ensure error and success states include both text and visual indicators.
- Do not rely on color alone to convey meaning. Pair status colors with text such as "Confirmed" or "Needs review."
- Respect chosen names; never surface legal names unless legally required.
- Offer translation-ready strings. Keep sentences modular to minimize localization risk.

## 6. Component and Pattern Guidelines

### Buttons and Calls to Action

- Use imperative verbs and limit to three words when possible ("Upgrade seats").
- Primary actions should map to the main success path. Secondary actions use plain verbs ("Cancel", "Back").
- Avoid duplicating information already present in the heading or body copy.

### Navigation and Tabs

- Label navigation with clear nouns ("Inventory", "Reporting"), not marketing taglines.
- Keep labels to a single concept. If more than one concept is required, create separate destinations.
- Use consistent terminology across apps. If "Orders" is in Backstage, use "Orders" everywhere.

### Forms and Data Entry

- Pair every input with a concise helper hint only if the field needs explanation.
- Surface required/optional states in text. Do not rely on asterisks alone.
- Error messages appear inline, first stating what went wrong, then how to fix it.

### Error States and Alerts

- Lead with impact, then action ("Balance overdue. Pay to prevent payouts from pausing.").
- Never use blame or alarmist punctuation. Stay calm and solutions-oriented.
- Offer links to help docs or contacts when resolution requires another system.

### Success, Empty, and Celebration States

- Confirm the outcome and surface the next logical step ("VIP wristbands printed. View pickup checklist.").
- Keep celebratory language minimal and relevant ("You're in! Get event reminders by email.").
- For empty states, clarify why the state is empty and provide a primary action to populate it.

### Tooltips and Inline Help

- Use tooltips for definitions, not primary instructions.
- Keep to 80 characters or fewer. Reference the object the tooltip explains.
- Avoid repeating the same content in helper text and tooltips.

### Tables and Data Visualizations

- Label columns with nouns ("Tickets sold", "Scan rate").
- Use singular nouns when referring to individual rows ("Section", not "Sections").
- Explain metrics on first use and provide download options for detailed analysis.

### Notifications, Banners, and Toasts

- Indicate urgency visually and verbally ("Banner — needs action", "Toast — confirmation").
- Front-load the key detail within 70 characters.
- Include dismiss labels ("Dismiss") rather than "X".

## 7. Terminology and Naming Standards

### 7.1 People and Roles

- **Guests/Fans**: People purchasing or holding tickets.
- **Clients**: Promoters, venues, or partners contracting Front Gate Tickets.
- **Team members**: Internal staff using Backstage, Admit One, or Thundercat.
- **Volunteers/Temp staff**: Use "event staff" unless a specific role is defined.

### 7.2 Common Actions

- Use "Add", "Edit", "Remove" consistently for CRUD actions.
- Prefer "Refund" over "Return" for ticket reimbursements.
- Use "Transfer" for sending tickets to another person; reserve "Resell" for marketplace listings.
- Label login-related actions as "Sign in"/"Sign out" across all applications.

### 7.3 Financial Terms

- Use "Payout" for funds sent to clients; avoid "Settlement" unless referencing legal agreements.
- "Fees" refer to charges paid by guests; "Service charges" only when legally required.
- Always specify currency and cadence ("Weekly payouts in USD").

## 8. Governance, Workflow, and Tooling

1. **Brief**: Capture audience, action, constraints, legal or policy requirements, and success metrics for the copy change.
2. **Draft**: Write directly in the design file, component, or CMS with proper version control. Document alternatives considered.
3. **Pair Review**: Partner with design or product to stress-test clarity, tone, inclusivity, and data accuracy.
4. **Legal & Compliance**: Route to Legal when copy affects pricing, terms, or policy statements. Capture approvals in the ticket history.
5. **Implementation QA**: Validate the live string matches the approved copy, including punctuation, spacing, and fallback states.
6. **Monitor**: Track key metrics (conversion, drop-off, support contacts). Iterate as needed, updating this document when guidance shifts.

### 8.1 Quality Gates

- **Coverage**: Confirm a draft or implementation exists for every string impacted by the ticket.
- **Voice alignment**: Compare tone against the matrix in Section 2; flag mismatches.
- **Inclusivity**: Run automated checks for banned terminology and manual review for context.
- **Readability**: Surface the reading grade and highlight sentences exceeding 25 words.
- **Action clarity**: Ensure every screen has one primary action or a clearly staged sequence.
- **Traceability**: Link feedback to ticket IDs, components, or string resource keys.

### 8.2 Metrics and Tooling

- **Preferred readability metric**: Flesch-Kincaid. Aim for Grade 6.5 in consumer flows, Grade 8.5 for B2B/internal.
- **String management**: Use the localization repository as the source of truth. Document context notes for translators.
- **Instrumentation**: Tag UI copy experiments with analytics event IDs to monitor impact.
- **Feedback loop**: Capture user support phrases to refine terminology lists quarterly.

## 9. Application-Specific Guidance

### Backstage (Internal Operations)

**Audience & mindset**: Event, inventory, and settlement specialists who need to act fast under pressure.

**Voice priorities**:
- Lead with precision. State quantities, deadlines, and ownership.
- Assume high context. Domain terms like "manifest" or "settlement" are acceptable.
- Balance candor with courtesy; skip fluff while acknowledging impact.

**Key scenarios and copy cues**:
- **Dashboards**: Use headline + metric + action. "Holds: 26 tickets. Release by 5 p.m."
- **Incident management**: Begin with status, then assignment. "Scanner 04 offline. Assign tech."
- **Approvals**: Provide summary + decision + effect. "Approve transfer? Seats release immediately."

**Do / Avoid**:
- Do: State dependencies and timing ("Report exports in 3–5 minutes").
- Avoid: Leaving timing vague ("Export soon").
- Do: Highlight irreversible actions ("Deleting this manifest removes all holds.").
- Avoid: Burying risk in a tooltip or secondary paragraph.
- Do: Use table labels that match reporting taxonomy.
- Avoid: Inventing new shorthand per module.

### Admit One (Box Office)

**Audience & mindset**: Box Office staff scanning tickets and resolving entry issues in noisy environments.

**Voice priorities**:
- Keep sentences short and scannable. Aim for 30 characters or less on primary actions.
- Use imperative tone for directions ("Scan again").
- Provide immediate resolution paths (override, escalate, or educate the guest).

**Key scenarios and copy cues**:
- **Entry confirmation**: "Welcome! Gate 2. Enjoy the show."
- **Scan failure**: "Ticket already used at 7:12 p.m. Send to supervisor."
- **Hardware issues**: "Reader offline. Switch to backup device."

**Do / Avoid**:
- Do: Mention escalation options within the same screen.
- Avoid: Sending staff to another tool without guidance.
- Do: Use color + text ("Denied — Already scanned").
- Avoid: Color-only indicators for pass or fail.
- Do: Keep translation-ready by avoiding idioms.
- Avoid: Phrases like "Give it another whirl."

### Thundercat (On-Site Operations)

**Audience & mindset**: Field and Client Operation teams.

**Voice priorities**:
- Adopt a diagnostic voice: describe state, impact, root cause, next step.
- Reference data sources and timestamps for traceability.
- Link to runbooks or logs for deeper dives.

**Key scenarios and copy cues**:
- **Status alerts**: "API latency high (1.8s). Payment retries queued."
- **Integrations**: "Freshdesk sync paused. Resume after API key update."
- **Capacity planning**: "VIP check-in trending +18% vs. forecast. Add staff to Gate 1."

**Do / Avoid**:
- Do: Surface severity levels (Info, Warning, Critical).
- Avoid: Leaving severity implicit.
- Do: Use verb + noun labels for actions ("Restart job").
- Avoid: Technical jargon without user-facing meaning.
- Do: Note when issues auto-resolve.
- Avoid: Implying manual work when automation is in place.

### Ecomm App (Consumer)

**Audience & mindset**: Fans purchasing tickets, add-ons, and merchandise primarily on mobile.

**Voice priorities**:
- Build excitement while staying clear. Focus on benefits and logistics.
- Reduce anxiety around payments, delivery, and support.
- Respect accessibility needs: provide seat info, pricing, and policy clarity.

**Key scenarios and copy cues**:
- **Product discovery**: "Choose your 3-day GA pass. See map for sightlines."
- **Add-ons**: "Add parking to skip day-of lines."
- **Checkout**: "Payment received. We emailed your mobile tickets."
- **Post-purchase**: "Need help? Chat with us or text 512-555-1111."

**Do / Avoid**:
- Do: Highlight value in first clause ("Skip the gate line with Fast Pass").
- Avoid: Feature-only statements ("Fast Pass available").
- Do: Clarify delivery methods ("Tickets arrive by email within 2 minutes").
- Avoid: Vague timelines ("You'll get tickets soon").
- Do: Offer reassurance for refunds/exchanges.
- Avoid: Threatening tone around policies.

### B2C Marketing Site

**Audience & mindset**: Prospective and returning fans browsing events and offers on desktop and mobile.

**Voice priorities**:
- Lead with headline clarity: Event, location, date.
- Balance excitement with accuracy — never exaggerate availability.
- Make promotions transparent: state price, deadline, exclusions.

**Key scenarios and copy cues**:
- **Hero section**: "Front Gate Tickets — Your pass to unforgettable festivals."
- **Promo modules**: "Save $20 on weekend bundles through Oct 31."
- **FAQ entries**: "How do I transfer tickets? Sign in, select your order, choose Transfer."

**Do / Avoid**:
- Do: Use action-oriented CTAs ("Explore passes").
- Avoid: Hype without action ("Can't miss this!").
- Do: Place legal info adjacent to the relevant offer.
- Avoid: Burying disclaimers in footers.
- Do: Optimize for SEO with natural phrases ("festival parking passes").
- Avoid: Keyword stuffing or unnatural sentence fragments.

### B2B Client Portal

**Audience & mindset**: Promoters, venue managers, and client partners overseeing sales, settlements, and marketing.

**Voice priorities**:
- Adopt a consultative tone. Highlight insights and recommended actions.
- Be explicit about financials — include timeframes, amounts, and reconciliation cues.
- Support collaboration: indicate shared responsibility and next steps.

**Key scenarios and copy cues**:
- **Reporting**: "Sales pace +12% vs. forecast. Review add-on inventory."
- **Financials**: "Payout scheduled Oct 3 for $124,500. View breakdown."
- **Marketing**: "Audience overlap 34% with 2024 event. Launch retargeting?"

**Do / Avoid**:
- Do: Use precise business vocabulary ("remit", "net revenue").
- Avoid: Consumer-friendly slang in professional contexts.
- Do: Offer contextual links to deeper data and export options.
- Avoid: Trapping users in summary views without actions.
- Do: State assumptions behind recommendations.
- Avoid: Presenting recommendations as facts without evidence.

## 10. Review Checklists and Rubrics

### 10.1 Global Copy QA Checklist

- [ ] Voice & tone match the scenario matrix.
- [ ] Plain language: no unexplained acronyms or internal jargon.
- [ ] Action clarity: each screen highlights the primary action.
- [ ] Accessibility: text alternatives, color contrast, focus order validated.
- [ ] Localization: strings are neutral and context notes exist where needed.
- [ ] Legal/compliance statements validated with stakeholders.
- [ ] Analytics events or logging updated for new or revised flows.

### 10.2 Scoring Rubric

| Category | Score 3 — Excellent | Score 2 — Needs polish | Score 1 — Rework |
|---|---|---|---|
| Clarity | Action obvious, sentences concise, no ambiguity. | Some redundancy or long sentences remain. | Meaning unclear or conflicting actions. |
| Tone fit | Matches voice matrix and respects audience needs. | Mostly aligned but occasional tonal drift. | Tone inappropriate or confusing. |
| Inclusivity & accessibility | Language inclusive, supports assistive tech. | Minor accessibility gaps (e.g., missing alt guidance). | Excludes users or violates accessibility basics. |
| Accuracy & trust | Data references, legal statements confirmed and labeled. | Some context missing but directionally correct. | Outdated, incorrect, or overpromising content. |

### 10.3 App-Specific Spot Checks

- **Backstage**: Confirm totals, timestamps, and SLA language align with ops policies.
- **Admit One**: Validate button labels fit hardware screens and offer escalation path.
- **Thundercat**: Ensure severity tags and runbook links exist for every alert.
- **Ecomm**: Check checkout copy against legal and payment processor requirements.
- **B2C site**: Verify promotional copy includes deadlines and complies with brand style.
- **B2B portal**: Provide export and reconciliation instructions for financial data.

## Appendix A: Common Microcopy Library

- **Primary actions**: "Continue", "Review order", "Print passes", "View details".
- **Secondary actions**: "Back", "Cancel", "Save draft", "Skip for now".
- **Empty state starters**: "No [item] yet", "Nothing scheduled", "All clear".
- **Loading**: "Working on it…", "Fetching latest data…".
- **Error CTAs**: "Try again", "Update payment method", "Contact support".

## Appendix B: Error Message Template

1. **Heading** (optional): State the effect. Example: "Payment failed".
2. **Body sentence 1**: What happened + impact. "Card ending •1234 was declined."
3. **Body sentence 2**: How to fix. "Try another card or contact your bank."
4. **Optional link**: "Get help with payments."
5. **CTA** (if needed): "Update payment method".

## Appendix C: Glossary

For definitions of key terms such as Addon, Gate hold, Manifest, Payout, Settlement, Transfer, and Upgrade, refer to `fgt-glossary.md` in this references directory. The glossary contains 200+ FGT-specific terms organized alphabetically and by category (FGT Applications, Features, Concepts, Acronyms, Vendors, and LNE Companies).

Maintain this document quarterly. Capture updates to terminology, policies, or product surfaces and socialize changes with all content practitioners.
