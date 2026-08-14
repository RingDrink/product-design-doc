---
name: product-design-doc
description: "Jyun 个人维护的通用产品 / 游戏策划案写作上位工作流。MUST USE when Jyun wants to write, rewrite, review, or clarify any product design doc, feature spec, gameplay/system proposal, prototype validation plan, implementation-readiness decision, UX-backed complete spec, or asks to grill/ask questions before writing—including inside Project F1. This personal Core owns document genre, reasoning, structure, visuals, formatting preservation, and writing quality; project Skills and tools may supply facts or publishing adapters but must not replace it."
---

# Product Design Doc

Use this skill to turn a vague feature idea, design discussion, UX source, or existing draft into a readable design document that a product, UX, engineering, or game-dev team can act on. Before a feature reaches specification or implementation, require it to serve a named expected experience and a concrete validation question.

The skill is split into **Core** and **Adapters**:

- **Core** is the portable workflow: context intake, question-grilling, design decisions, document structure, visuals, UX evidence, readability, lint, and handoff.
- **Adapters** are optional environment bindings: where to ask questions, where to publish, how to read Figma, where to store decisions, and how to write back to a project memory system.

Do not assume the user has any specific agent framework, project memory system, or document platform. If an adapter is unavailable, keep working in Markdown and leave a clear handoff package.

## Personal Authority

This repository is Jyun's personal authority for design-document writing. Whenever Jyun asks to write, rewrite, review, or clarify a design doc, load this skill even if a project harness also selects a project design capability.

- This Core owns document genre, reasoning gates, structure, source-format preservation, visual/text division, compression, and writing quality.
- Project capabilities may provide project facts, terminology, coupling evidence, paths, source-control constraints, publishing tools, and platform-specific checks.
- A project template or project design Skill must not replace this Core's document frame or silently override the source document's format contract.
- If a project procedure conflicts with this Core on writing method or presentation, follow this Core and use the project procedure only for its adapter responsibilities. Surface any unavoidable hard-policy conflict instead of silently merging the two.
- Do not register this personal Skill in a team's shared selector or copy its Core into a team Skill merely to make it routable. Personal Agent entry instructions invoke it above the project harness.

## Route

1. If the user wants to "ask first", "grill", "clarify", "pressure test", or the design is still ambiguous, use `references/grill-before-writing.md`.
2. For a new feature, gameplay system, prototype, or material change, load `references/experience-led-validation.md` and pass its Experience Gate before detailing functions or authorizing implementation.
3. If the user wants a draft or complete doc, read current context first, then follow `references/core-workflow.md`.
4. If the doc needs UX/Figma/demo/UI evidence, load `references/visuals-and-ux-evidence.md` before writing.
5. If the task involves publishing, personal KB, project knowledge, Figma tools, or a team-specific workflow (e.g. a Project F1 design doc, which must pull the shared design context), load `references/adapters.md` and select only the relevant adapter. Adapters provide evidence and execution bindings; they do not become the writing authority.
6. Only when the requested artifact is a **system design spec** for an existing or settled rules/state/resource system, load `references/concise-system-spec.md` before writing. Do not apply it to gameplay concept pitches, narrative/quest/level/content plans, UX exploration, validation briefs, or other design-doc genres unless the user explicitly asks to convert them into a system spec.
7. For structure, style, and formatting rules, use `references/structure-conventions.md`.
8. Before delivery, run `python3 scripts/structure_lint.py <draft.md>` when a Markdown draft exists. For an implementation-ready requirement, run `python3 scripts/structure_lint.py --implementation-ready <draft.md>` instead. If the doc is exported/published through an adapter, also run `python3 scripts/structure_lint.py --rendered <exported.md|html|xml>` on the exported/published artifact; add `--require-numbered-headings` only when that adapter promises generated feature-heading numbers.

## Core Workflow

Always do these steps unless the user explicitly asks for a narrow edit:

1. **Intake current truth**: read the user-provided draft, links, screenshots, UX, code notes, tickets, meeting notes, and prior decisions available in the current environment. Do not ask questions already answered by supplied material.
2. **Classify the stage**:
   - **Exploration / decision alignment**: the feature frame is not stable; ask targeted questions and record decisions.
   - **Early draft**: UX/design is not final; explain the target experience, feature frame, flow, and likely visuals so UX or stakeholders can align.
   - **UX alignment**: use the draft to support UX, prototype, demo, or interaction decisions.
   - **Complete spec**: UX/demo/UI is available; use real design evidence and define functional rules, data, edge cases, resources, and engineering handoff.
3. **Pass the Experience Gate**: name the expected experience, the main choice or tension, the risk/cost, the lasting outcome, the product/theme promise, and the primary uncertainty to validate. If the intended experience is still unclear, continue design discussion; do not detail or implement the feature. Every implementation-bound function must serve at least one expected-experience validation.
4. **Resolve before publishing**: if a product, gameplay, UX, value, priority, or boundary decision is missing, ask the highest-leverage question and keep asking until the requirement can state one conclusion. Do not put `TBD`, `待确认`, “冻结决策”, “开放问题”, or an equivalent unresolved-decision section in a reader-facing requirement. If the decision cannot be obtained, remain in exploration or leave the question in conversation / `handoff.md`; do not present the document as implementation-ready.
5. **Pressure-test before build**: check for boring optimal play, exploitable incentives, dependency cascades, removable complexity, and solutions that merely patch an undecided frame.
6. **Choose the document genre before the stage**: preserve the conventions of gameplay proposals, narrative/quest/level/content plans, UX exploration, prototype briefs, and other genres. Apply the compact model/rules/developer-self-check shape only to a system design spec, not to every design document.
7. **Write for human readers**: business/product/gameplay headings, short paragraphs, bullets, tables, and selective visuals. Internal checks such as the Experience Gate and unresolved-decision tracking stay outside the reader-facing requirement.
8. **Compress before delivery**: state each rule once, keep background subordinate to decisions, move future ideas out of the main rule path, and delete sections that do not change implementation, developer self-check, or stakeholder judgment. Put cross-system effects and behavior boundaries beside the functional rule they constrain; do not add a default “关联系统与边界” chapter or coupling matrix. When rewriting an existing system spec, compress its content inside the existing document frame; do not replace that frame with this skill's default shape. For a system spec that separates one value/object into parallel resources or states, run the separation audit in `references/concise-system-spec.md`; do not describe a future possibility as present-version tension.
9. **Protect the source contract**: treat the source document as authority for both visuals and presentation. Preserve title metadata blocks, heading levels, indentation, deliberate blank lines and separators, list nesting, captions, table layout/widths, inline colors, and other rich-text conventions unless the user explicitly asks to restyle them or the target platform cannot represent them. For a system spec, cover the main flow and audit every major operation module for an adjacent authoritative visual or explicit visual handoff; divide responsibility so visuals show flow/state/layout while prose supplies confirmed boundaries and feedback without narration. Project F1 system diagrams use self-contained SVG as the final source and Feishu SVG whiteboards as the published form.
10. **Validate and hand off**: run source lint and, when publishing/exporting, rendered lint; fix ERRORs, handle WARNs or explain them, and leave a continuation checkpoint if work is incomplete.

## Knowledge Return

- When Jyun says `KB` without a qualifier, it means his personal library. Preserve project names, internal rules, links, and concrete decisions when they are needed to keep the conclusion accurate; de-identification is optional, never a reason to distort the reasoning.
- When Jyun says `FF`, it means the FireForge project knowledge base. Use it for team-facing current project facts, decisions, links, and implementation state.
- `KB` and `FF` are routing terms, not mutually exclusive content-security tiers. A stable personal lesson may cite the concrete project evidence that produced it; do not duplicate material mechanically when one destination is sufficient.
- A project-local knowledge adapter must never reinterpret unqualified `KB` as project knowledge. Normal credential, privacy, and authorization boundaries still apply in both destinations.

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
- `references/concise-system-spec.md` only for compact implementation-facing system design specs; never treat it as the default structure for other design-doc genres.
- `references/structure-conventions.md` for document shape, readable headings, resource lists, and lint expectations.
- `references/visuals-and-ux-evidence.md` for diagrams, screenshots, Figma/demo/UI sources, and media manifest rules.
- `references/adapters.md` for optional runtime, publishing, Figma, project-memory, or handoff bindings.
- `templates/design-doc-brief-template.md` when delegating or asking another agent/person to draft.

## Verification

- The document stage is explicit: exploration, early draft, UX alignment, or complete spec.
- The expected experience and primary validation question are explicit before implementation-bound functions are specified.
- Every implementation-bound function maps to at least one expected-experience validation; unmapped functions are removed or deferred.
- A prototype has one primary validation question and no more than three acceptance questions. Supporting scaffolding is not mistaken for validated design.
- The adversarial pre-build review is complete. An implementation-ready requirement has no unresolved structural blocker; accepted residual risks appear only where they change a current rule or delivery judgment.
- An implementation-ready requirement contains only resolved conclusions. Missing decisions were asked and answered; unresolved questions remain outside the reader-facing requirement in conversation or `handoff.md`. No fabricated team decisions, code names, exact numbers, or UX facts.
- Visible headings use business/product terms, not fixed internal facets like "规则与反馈" or "系统响应".
- When and only when the artifact is a system spec, it exposes the current-version system model, rules, state/ownership boundaries, failure handling, and developer self-check before rationale, roadmap, or task breakdown.
- In a system spec, each rule has one authoritative location; overview, scope, detail, and resource list do not restate the same behavior in prose.
- In a system spec, background, alternatives, future direction, and internal validation notes are omitted or collapsed unless they change a present decision.
- In a system spec with parallel resources or states, their current-version distinction is explicit across risk, ownership/storage, direct consumers, and conversion. A free, immediate, unlimited, lossless conversion into the universally safer or more useful form is identified as a maintenance optimum rather than advertised as a meaningful choice.
- In a system spec, unsourced values, priorities, owners, atomicity guarantees, overflow behavior, and UX choices are resolved before publication, delegated explicitly as implementation discretion, or omitted when irrelevant; they are never padded with `TBD` in the requirement. Plausible implementation advice is not silently promoted to a confirmed design rule.
- Every implementation-ready requirement has a visible `验收口径` (or source-format equivalent) consisting of concise Markdown checkboxes for the programmer to self-check after implementation. Each item states a condition/action and one observable result, covering the main path and only the key boundaries.
- Cross-system effects and behavior boundaries appear beside the functional rule they constrain. A standalone “关联系统与边界” section is exceptional, not part of the default document frame.
- In a system spec rewrite, source visuals and layout requirements are preserved or explicitly superseded; the main flow and every major operation module has visual coverage or a named visual handoff requirement, and adjacent prose does not repeat the figure.
- In an existing system-spec rewrite, the source's visible format contract is preserved: metadata quote, heading hierarchy, indentation/list nesting, intentional spacing/separators, captions, table structure/widths, and inline emphasis/colors. A new template is not substituted merely to improve concision.
- Every system diagram answers a named reader question and makes the authoritative path unambiguous. A blocked edge is drawn only between the two objects it actually forbids; it must not visually sever a valid conversion path.
- Complete specs with UX/UI/demo sources use real UX evidence instead of leftover low-fidelity UI SVGs.
- Visuals have source, insertion point, short alt text, and a nearby caption explaining what the reader should see.
- Source lint has no ERRORs: use `python3 scripts/structure_lint.py --implementation-ready <draft.md>` for implementation-ready requirements and the base command for other genres. WARNs are fixed or called out.
- If a publishing/export adapter is used, rendered lint has no ERRORs: `python3 scripts/structure_lint.py --rendered <exported.md|html|xml>`. Use `--require-numbered-headings` only for adapters that are expected to generate numbered feature headings.
- If work is incomplete or may be interrupted, `handoff.md` or the final response states current state, next steps, unresolved decisions, and where the draft/media live.
