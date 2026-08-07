# Core Workflow

This is the platform-independent design-doc workflow. It assumes only Markdown and the current conversation are available.

## 1. Intake Current Truth

Read the available material before asking:

- Existing design docs, drafts, tickets, notes, meeting conclusions, screenshots, video, UX/UI/demo links, Figma links, code keywords, and stakeholder comments.
- Project conventions in the current repo or workspace, if they are present.
- Prior accepted decisions, if the project has a decision log or equivalent.

Rules:

- Do not ask a question that the provided material already answers.
- Do not treat stale memory or an old draft as current truth when newer input exists.
- If two sources conflict, surface the conflict and ask whether the new source supersedes the old one.
- If a source is inaccessible, state that and continue from available evidence with explicit uncertainty.

## 2. Decide The Document Stage

Use the stage to choose the right level of detail and visual strategy.

| Stage | Goal | Good output |
|---|---|---|
| Exploration / decision alignment | Find the design frame and key trade-offs | Question summary, decision record, open questions |
| Early draft | Align product/gameplay direction before UX or implementation | Target experience, feature frame, main flows, boundaries, early diagrams/references |
| UX alignment | Help UX/prototype/demo converge | Interaction assumptions, flow diagrams, areas needing UX decision |
| Complete spec | Support actual implementation | UX-backed rules, data, edge cases, resources, acceptance, engineering handoff |

If the user does not name the stage, infer it from evidence:

- No stable UX/UI/demo and many open choices -> early draft or exploration.
- Figma/demo/UI source exists and the user wants developer-facing details -> complete spec.
- The user asks "先问清楚" / "grill" / "pressure test" -> exploration.

## 3. Pass The Experience Gate

For a new feature, gameplay system, prototype, or material change, load `experience-led-validation.md` before functional decomposition.

- Define the expected experience and primary uncertainty first.
- Map every implementation-bound function to at least one expected-experience validation.
- If the experience is unclear, remain in exploration. Do not disguise a feature inventory as a settled design.
- Run the adversarial pre-build review before implementation handoff.

Do not make a universal state-boundary worksheet a substitute for experience clarity. Specify persistence, reset, ownership, and failure boundaries only when the feature actually requires them.

## 4. Clarify Before Writing

Use `grill-before-writing.md` when:

- Main flow, user goal, key state, scope boundary, or system impact is unclear.
- Several valid design directions exist and choosing one affects structure.
- The user gave a meeting conclusion without enough traceable fields.

Ask one high-leverage question at a time when possible. If the environment cannot support live interaction, produce a compact question list and mark blockers.

## 5. Write The Doc

Use this macro shape by default:

1. **Overview / Core Experience**: what this feature is, why it exists, the target experience, and the version boundary.
2. **Feature Details**: the functional modules, player/user actions, system rules, feedback, data, edge cases, and configuration.
3. **Delivery / Handoff**: resources, owners/functions, dependencies, acceptance, open decisions, and verification.

This is a shape, not a rigid template. Delete empty sections. Add domain-specific sections only when they help the reader.

## 6. Handle Decisions

For every non-trivial design decision, preserve enough traceability that a teammate can later understand it:

- Source: who/what established it.
- Context: what problem it solves.
- Decision: the normalized conclusion.
- Alternatives: meaningful options considered, if known.
- Scope: feature/system/version affected.
- Status: proposed / accepted / superseded / TBD.
- Follow-up: what would reopen or verify it.

If fields are missing, ask. If asking is not feasible, leave `TBD` and list it in follow-up.

## 7. Resumability

Before stopping, handing off, or when quota/context risk is visible, leave a checkpoint:

```markdown
# Design Doc Handoff

## Current State
- Stage:
- Draft path / published URL:
- Last completed section:

## Confirmed Decisions
- ...

## Open Questions
- ...

## Media / UX Evidence
- ...

## Next Steps
1. ...
```

If the project has an existing handoff, task log, or memory adapter, write there. Otherwise, create a `handoff.md` next to the draft or include the same checkpoint in the final response.

## 8. Review Before Delivery

- Reader can understand the feature in the first screen without internal workflow context.
- Expected experience, primary validation question, and feature-to-experience mapping are explicit before implementation handoff.
- The prototype or feature has one primary validation question, no more than three acceptance questions, and a named acceptance authority.
- The adversarial review has no hidden structural blocker.
- Each feature point has enough action, rule, feedback, edge case, and implementation handoff detail for the document stage.
- Complete specs do not use early low-fidelity UI sketches as final interface authority.
- Visuals are placed near the rules they explain.
- Source lint passes with no ERRORs: `python3 scripts/structure_lint.py <draft.md>`.
- If a publishing/export adapter is used, rendered lint also passes with no ERRORs: `python3 scripts/structure_lint.py --rendered <exported.md|html|xml>`.
- If that adapter is expected to generate numbered feature headings, add `--require-numbered-headings` to the rendered lint command.
