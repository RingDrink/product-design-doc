---
name: product-design-doc
description: "通用产品 / 游戏功能设计与文档工作流。MUST USE when the user wants to write, rewrite, review, or clarify a product design doc, feature spec, gameplay/system proposal, prototype validation plan, implementation-readiness decision, UX-backed complete spec, or asks to grill/ask questions before writing. Enforces an experience gate before functions enter implementation. Framework-agnostic: default output is portable Markdown; publishing tools, project memory, Figma, and team document platforms are optional adapters."
---

# Product Design Doc

Use this skill to turn a vague feature idea, design discussion, UX source, or existing draft into a readable design document that a product, UX, engineering, or game-dev team can act on. Before a feature reaches specification or implementation, require it to serve a named expected experience and a concrete validation question.

The skill is split into **Core** and **Adapters**:

- **Core** is the portable workflow: context intake, question-grilling, design decisions, document structure, visuals, UX evidence, readability, lint, and handoff.
- **Adapters** are optional environment bindings: where to ask questions, where to publish, how to read Figma, where to store decisions, and how to write back to a project memory system.

Do not assume the user has any specific agent framework, project memory system, or document platform. If an adapter is unavailable, keep working in Markdown and leave a clear handoff package.

## Route

1. If the user wants to "ask first", "grill", "clarify", "pressure test", or the design is still ambiguous, use `references/grill-before-writing.md`.
2. For a new feature, gameplay system, prototype, or material change, load `references/experience-led-validation.md` and pass its Experience Gate before detailing functions or authorizing implementation.
3. If the user wants a draft or complete doc, read current context first, then follow `references/core-workflow.md`.
4. If the doc needs UX/Figma/demo/UI evidence, load `references/visuals-and-ux-evidence.md` before writing.
5. If the task involves publishing, project memory, Figma tools, or a team-specific workflow (e.g. a Project F1 design doc, which must pull the shared design context), load `references/adapters.md` and select only the relevant adapter.
6. For structure, style, and formatting rules, use `references/structure-conventions.md`.
7. Before delivery, run `python3 scripts/structure_lint.py <draft.md>` when a Markdown draft exists. If the doc is exported/published through an adapter, also run `python3 scripts/structure_lint.py --rendered <exported.md|html|xml>` on the exported/published artifact; add `--require-numbered-headings` only when that adapter promises generated feature-heading numbers.

## Core Workflow

Always do these steps unless the user explicitly asks for a narrow edit:

1. **Intake current truth**: read the user-provided draft, links, screenshots, UX, code notes, tickets, meeting notes, and prior decisions available in the current environment. Do not ask questions already answered by supplied material.
2. **Classify the stage**:
   - **Exploration / decision alignment**: the feature frame is not stable; ask targeted questions and record decisions.
   - **Early draft**: UX/design is not final; explain the target experience, feature frame, flow, and likely visuals so UX or stakeholders can align.
   - **UX alignment**: use the draft to support UX, prototype, demo, or interaction decisions.
   - **Complete spec**: UX/demo/UI is available; use real design evidence and define functional rules, data, edge cases, resources, and engineering handoff.
3. **Pass the Experience Gate**: name the expected experience, the main choice or tension, the risk/cost, the lasting outcome, the product/theme promise, and the primary uncertainty to validate. If the intended experience is still unclear, continue design discussion; do not detail or implement the feature. Every implementation-bound function must serve at least one expected-experience validation.
4. **Ask before inventing**: if a required decision is missing, ask the highest-leverage question. If asking is impossible or the user asked to proceed, mark the field as `TBD` / `待确认` and add it to the follow-up list.
5. **Pressure-test before build**: check for boring optimal play, exploitable incentives, dependency cascades, removable complexity, and solutions that merely patch an undecided frame.
6. **Write for human readers**: business/product/gameplay headings, short paragraphs, bullets, tables, and visuals. Internal execution labels are planning aids, not visible section names.
7. **Use visuals by default**: early drafts use diagrams, references, sketches, screenshots, or competitor examples; complete specs use UX/UI/demo screenshots first.
8. **Validate and hand off**: run source lint and, when publishing/exporting, rendered lint; fix ERRORs, handle WARNs or explain them, and leave a continuation checkpoint if work is incomplete.

## Output Contract

Default output is a Markdown package:

- `draft.md`: the design document.
- `media/`: screenshots, diagrams, generated images, or reference images when produced locally.
- `media-manifest.md`: source, insertion point, caption, authority, and uncertainty for each visual when media is used.
- `handoff.md`: only when work cannot be completed in the current session or quota/context may expire.

If the environment has a publishing adapter, the same content may be published to the target doc platform, but the Markdown package remains the portable source.

## Required References

Load only what the task needs:

- `references/core-workflow.md` for end-to-end writing and review.
- `references/grill-before-writing.md` for clarification before writing.
- `references/experience-led-validation.md` for the mandatory Experience Gate, isolated prototype branches, and adversarial pre-build review.
- `references/structure-conventions.md` for document shape, readable headings, resource lists, and lint expectations.
- `references/visuals-and-ux-evidence.md` for diagrams, screenshots, Figma/demo/UI sources, and media manifest rules.
- `references/adapters.md` for optional runtime, publishing, Figma, project-memory, or handoff bindings.
- `templates/design-doc-brief-template.md` when delegating or asking another agent/person to draft.

## Verification

- The document stage is explicit: exploration, early draft, UX alignment, or complete spec.
- The expected experience and primary validation question are explicit before implementation-bound functions are specified.
- Every implementation-bound function maps to at least one expected-experience validation; unmapped functions are removed or deferred.
- A prototype has one primary validation question and no more than three acceptance questions. Supporting scaffolding is not mistaken for validated design.
- The adversarial pre-build review is complete, with unresolved blockers or accepted residual risks visible.
- Missing decisions are either asked, marked `TBD`, or listed in follow-up; no fabricated team decisions, code names, exact numbers, or UX facts.
- Visible headings use business/product terms, not fixed internal facets like "规则与反馈" or "系统响应".
- Complete specs with UX/UI/demo sources use real UX evidence instead of leftover low-fidelity UI SVGs.
- Visuals have source, insertion point, short alt text, and a nearby caption explaining what the reader should see.
- Source lint has no ERRORs: `python3 scripts/structure_lint.py <draft.md>`. WARNs are fixed or called out.
- If a publishing/export adapter is used, rendered lint has no ERRORs: `python3 scripts/structure_lint.py --rendered <exported.md|html|xml>`. Use `--require-numbered-headings` only for adapters that are expected to generate numbered feature headings.
- If work is incomplete or may be interrupted, `handoff.md` or the final response states current state, next steps, unresolved decisions, and where the draft/media live.
