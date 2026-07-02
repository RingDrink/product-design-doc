# Design Doc Draft Brief

Use this brief when delegating a draft to another agent or teammate.

## Goal

Produce a readable product/game feature design doc in Markdown.

## Current Stage

- Stage: exploration / early draft / UX alignment / complete spec
- Target reader:
- Target output path or platform:

## Inputs

- Existing draft:
- Product / gameplay notes:
- UX/UI/demo sources:
- Code or implementation anchors:
- Tickets / meeting notes:
- Constraints:

## Confirmed Decisions

- ...

## Open Questions

- ...

## Writing Requirements

- Follow `product-design-doc/SKILL.md`.
- Use `references/structure-conventions.md` for headings, resource list, readable style, and lint expectations.
- If UX/UI/demo exists, follow `references/visuals-and-ux-evidence.md`; use real UX evidence and do not keep early UI SVGs as final interface authority.
- Do not expose internal local paths, private tracking ids, or workflow-only labels in the reader-facing doc.
- Missing facts must be asked, marked `TBD`, or listed in follow-up. Do not fabricate.
- Resource lists must use `function heading -> module heading -> checklist`; do not put checklist items directly under a function heading.
- If the doc is exported/published through an adapter, run rendered lint on the exported artifact. Use `--require-numbered-headings` only when that adapter promises generated feature-heading numbers.

## Deliverables

- `draft.md`
- `media/` outputs if any
- `media-manifest.md` if media is used
- `handoff.md` if incomplete
- Lint result from `python3 scripts/structure_lint.py <draft.md>`
- Rendered lint result from `python3 scripts/structure_lint.py --rendered <exported.md|html|xml>` if exported/published
