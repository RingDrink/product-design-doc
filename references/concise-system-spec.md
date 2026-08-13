# Concise System Spec

Use this reference only when the requested artifact is a system design spec for an existing or settled rules/state/resource system. Do not use it for gameplay concept pitches, narrative/quest/level/content plans, UX exploration, validation briefs, or other design-doc genres unless the user explicitly asks to convert them into a system spec.

## 1. Reader Contract

Optimize for three questions:

1. What changes in the current version?
2. What are the authoritative rules and boundaries?
3. How do we know the implementation is correct?

Rationale, history, future direction, and task planning are supporting information. They must not interrupt the rule path.

## 2. Default Shape

Use the smallest subset that covers a new system-spec feature. For a rewrite, treat this shape as a content audit, not a presentation template: keep the source document's established section hierarchy and rich formatting unless the user explicitly asks to restyle it.

1. **Decision Summary** — goal, one-sentence system model, current-version scope, and explicit non-goals.
2. **System Model** — authoritative objects/resources, ownership, states, conversions, and the main flow. Prefer a compact table or one diagram when relations are non-trivial.
3. **Rules By Operation** — group rules under business operations such as acquire, store, convert, consume, fail, and migrate. State trigger, precondition, result, and failure feedback.
4. **Boundaries And Exceptions** — lifecycle, persistence, concurrency/atomicity, capacity, failure/retry, migration, and cross-system ownership only where relevant.
5. **Acceptance** — observable scenarios that prove the rules, plus unresolved decisions that block implementation.
6. **Delivery** — dependencies and dispatchable tasks. Keep this separate from the design truth.

Do not expose this list mechanically. Use domain headings such as `Cash Acquisition`, `Extraction`, `Deposit`, and `Account Spending`.

## 3. Visual Coverage Contract

Compression removes repeated prose, not the visual contract of the source design.

- Preserve every source visual, screenshot request, caption convention, and layout requirement unless it is superseded, incorrect, or redundant with a stronger visual.
- Preserve the existing presentation contract as well: title metadata quote, heading levels, indentation, intentional blank lines/separators, list nesting, table geometry, inline emphasis, and semantic text colors. Do not translate an existing Feishu design into a newly invented Markdown/table template simply because the information is being compressed.
- Put one authoritative overview visual immediately after the system model when the feature has a multi-stage main flow.
- Audit every major operation module for a local visual. Use a flowchart, state split, relationship diagram, annotated screenshot, or explicit visual handoff whenever the visual can carry the action sequence, ownership change, state difference, or UI placement more directly than prose.
- A system spec may therefore contain several focused visuals. "State each rule once" means that the visual and text divide responsibility; it does not mean reducing the document to one diagram.
- The visual owns flow, object relationships, state transitions, and visible layout. The adjacent text owns preconditions, exceptions, failure handling, feedback, parameter status, and unresolved decisions.
- Do not restate every node and edge in the caption or prose. Captions tell the reader what to inspect and identify whether values or future branches are authoritative, placeholder, or out of scope.
- When the final UX does not exist, add a dispatchable visual requirement at the intended insertion point instead of silently omitting the illustration.
- Before delivery, include a visual coverage list or media manifest that maps `overview + each major operation module` to its figure, source/owner, insertion point, authority, value status, and format requirement.
- For Project F1 system specs, authored diagrams use self-contained SVG as the final source format and are inserted into Feishu as SVG whiteboards; Mermaid is planning notation only unless explicitly requested.

### Semantic gate for each diagram

Before drawing, write the single reader question the figure must answer. Keep the figure only if it answers that question faster or more reliably than adjacent text.

- Put the authoritative flow on the strongest visual path.
- Attach a prohibition marker to the exact invalid edge, not between broad resource groups where it could appear to block valid conversion.
- Show conversion and payment as separate operations. For example, `cash cannot directly pay a normal merchant` must not obscure `cash can be deposited into account balance`.
- Keep current rules and speculative extensions at different visual weights. If a future branch is not needed to understand the present decision, move it to a separate compatibility note instead of adding it to the operation diagram.
- Do not spend most of the canvas on decorative resource cards when the rule depends on branching, ownership, amount conservation, or state change.
- Review the rendered figure without its caption. If a reasonable reader can infer the opposite rule, redraw it.

## 4. Decision-Density Rules

- State a behavior once. Later sections link to or name that rule; they do not paraphrase it.
- Limit the opening rationale to the minimum needed to understand the decision. If two bullets explain the choice, do not add a separate history section.
- Put current-version scope beside the summary. Put future-version ideas in one short `Future Compatibility` note only when they constrain today's data or architecture.
- Do not delete source visuals, visual placeholders, captions, or formatting requirements merely to shorten the document. Replace a visual only when the replacement carries the same design responsibility more clearly.
- Remove examples that merely repeat a general rule. Keep an example only when it fixes an ambiguous value, boundary, or calculation.
- Keep implementation task names out of rule prose. The same noun may appear in a resource list, but the task row should name a deliverable rather than retell the design.
- Do not publish internal reasoning artifacts such as pressure-test checklists, Experience Gate fields, discarded alternatives, or exhaustive decision records unless the reader must approve an unresolved choice.
- Do not promote a reasonable implementation preference into a product decision. If atomicity, overflow behavior, priority, ownership, UX behavior, or a numeric value is not sourced, write `TBD` instead of choosing the safe-looking answer.
- Preserve source status. `Confirmed`, `inferred`, `placeholder`, and `TBD` are different; never rewrite one as another to make the document look complete.

## 5. Rule Normalization

Normalize prose into one of these forms:

### Operation Table

| Operation | Preconditions | System result | Failure / feedback |
|---|---|---|---|
| Deposit all cash | Cash exists in storage | Remove cash items and add the same amount to account balance | No cash behavior and failure/rollback semantics follow the source decision; otherwise TBD |

### State / Ownership Table

| Situation | Owned by / stored in | On success | On failure |
|---|---|---|---|
| Extracted cash | Player inventory | Moves to storage | Non-secured cash remains on the body |

### Data Contract

| Field / concept | Meaning | Current-version rule | Future constraint |
|---|---|---|---|
| Cash amount | Stack count equals value | Integer, unit value 1 | Preserve only metadata constraints confirmed by the source; otherwise TBD |

Use prose only when a table would fragment one clear statement.

## 6. Boundary Audit

Ask these questions, but include only relevant answers in the final document:

- **Atomicity:** Can a conversion, purchase, or reward partially apply?
- **Capacity:** What happens at stack, inventory, storage, or account limits?
- **Ownership:** Which system is authoritative for each resource or state?
- **Lifecycle:** What happens on success, failure, death, disconnect, retry, or rollback?
- **Composition:** When instances with different metadata merge or split, what is preserved?
- **Migration:** Are old items, saves, tables, quests, rewards, or references still present?
- **Presentation:** What feedback is required to understand success, failure, and the resulting value?

Mark missing implementation-blocking answers as `TBD`. Do not invent them.

Do not assign task priorities or owners unless the source or user supplied them. Leave the cells `TBD`.

## 7. Parallel Resource / State Separation Audit

Use this audit when one underlying value or object is represented as two currencies, balances, containers, ownership states, legality states, secured/unsecured states, or similar parallel forms. The spec must explain the distinction as a present system rule, not only as theme or a future hook.

### Start from the design problem

State which current problem the separation solves. Typical valid answers include different exposure to loss, different storage/ownership, exclusive transaction eligibility, different liquidity, or a conversion decision with a real cost. "We may add a use later" is future compatibility, not a current player-facing reason.

### Publish the operation matrix

For each form, state its current rules for:

| Dimension | Required distinction |
|---|---|
| Acquire / hold | Where it originates and where it is authoritative |
| Risk / persistence | What can remove, expose, secure, or preserve it |
| Direct consumers | Which operations accept it directly; distinguish direct payment from convert-then-pay |
| Conversion | Direction, ratio, timing, location, fee, limit, and rollback behavior |
| Feedback | How the user knows which form changed and why an operation failed |

If two forms are identical on all relevant dimensions, challenge the split or mark it as implementation scaffolding that should not yet create user-facing management work.

### Attack the optimum

- If conversion is free, immediate, unlimited, lossless, and produces the universally safer or more useful form, rational behavior collapses to "convert immediately." Treat any required click, slot pressure, or repeated cleanup as maintenance friction, not strategy.
- A meaningful choice needs a reason to keep either form: an exclusive opportunity, exposure/risk trade-off, price or fee difference, time/location constraint, capacity limit, or another current rule the player can act on.
- Do not add a fee, delay, or exclusive sink merely to justify the split. First confirm the target experience; otherwise prefer one resource/state and less complexity.

### Use comparisons correctly

When researching precedents, identify the structural model and its supporting conditions instead of copying surface nouns. For example, `two non-convertible currencies with exclusive sinks` solves a different problem from `one currency in exposed and secured states with easy deposit`. State which conditions transfer to this system and which do not.

### Separate current truth from future compatibility

If the current version intentionally ships only a framework for later mechanics, say so explicitly:

- define the present utility and unavoidable management cost;
- name the future constraints that today’s data/model must preserve;
- keep undecided future mechanics `TBD` and outside the authoritative current flow;
- do not claim that the future trade-off already exists.

## 8. Compression Pass

Before delivery:

1. Highlight every present-version decision and acceptance condition.
2. Delete any paragraph that contains neither.
3. Merge duplicate rules into one authoritative table or subsection.
4. Collapse future direction to constraints on today's design; move everything else out of the main document.
5. Check the first screen: a reader should see the goal, system model, and version boundary without scrolling through history.
6. Check the final screen: delivery tasks must be traceable to rules, but must not become a second copy of the spec.
7. Check visual coverage: the main flow and every major operation module either has an adjacent authoritative visual or an explicit visual handoff requirement.
8. Check visual-text division: no paragraph merely narrates the nodes and arrows already visible in the adjacent figure.
9. Compare source and target presentation: heading levels, quote blocks, blank-line rhythm, list nesting, table geometry, text colors, and captions remain intact unless an approved restyle is recorded.

The target is not a short document at any cost. The target is high decision density with no missing boundary that could cause divergent implementations.
