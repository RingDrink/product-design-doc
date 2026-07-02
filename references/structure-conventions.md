# Structure Conventions

These rules optimize for human readability and implementation handoff. They are not tied to a document platform.

## 1. Header

Recommended Markdown header:

```markdown
# Feature / System Design Doc
> **Type:** New feature / iteration / system redesign
> **Status:** Draft / reviewing / accepted / superseded
> **UX / UI Source:** [link](https://example.com) (required for complete specs when available)
> **Dependencies:** [related doc](https://example.com)
> **Version / Scope:** v1 / milestone / release
> **Date:** YYYY-MM-DD

---
```

Guidelines:

- Title is the first `#`.
- Metadata is a compact quote block. Keep internal local paths, block ids, decision ids, and private tracking anchors out of reader-facing docs.
- Complete specs with UX/UI/demo evidence should name the authority source in the header.
- If the platform uses another metadata format, keep the same fields semantically.

## 2. Macro Shape

Default order:

1. **Core Experience / Overview**: what this is, why it exists, target experience, version boundary.
2. **Feature Details**: modules, flows, rules, feedback, data, configuration, edge cases.
3. **Delivery / Handoff**: resources, dependencies, acceptance, open decisions, verification.

Delete empty sections. Do not keep a template heading just because the template had it.

## 3. Feature Point Shape

Internal planning facets:

- Goal / user action / rule / feedback / limitation / configuration / implementation / acceptance.

These are **virtual checks**, not mandatory visible headings. The final doc should use business headings:

- Good: `Entry And Operation`, `Cost Preview`, `Inventory And Restock`, `Failure Handling`, `Version Scope`.
- Avoid: `User Behavior`, `System Response`, `Rules And Feedback`, `Limitations And Exceptions`.

Use structure based on content weight:

| Content shape | Preferred form |
|---|---|
| One clear statement | One short paragraph |
| Named parallel rules | `- **Keyword:** explanation` bullets |
| Ordered flow | Numbered list |
| Multiple attributes / comparisons | Table |
| Feature point with several submodules | `####` / `#####` business subheadings |
| Multi-screen navigation | Diagram or UX screenshot near the text |

## 4. Human-Readable Style

- Start with what the reader should understand, then define system behavior.
- Keep paragraphs short. If a paragraph has several actions, states, or exceptions, split it into bullets or a table.
- Use exact terms for fields, classes, config keys, states, and controls, but keep them in implementation or data sections.
- Avoid execution-agent wording such as `cwd`, `adapter`, `reflux`, `canonical`, `outbox`, or local-only tracking ids.
- Avoid filler phrasing such as "in addition", "in summary", "this feature aims to", "ensure a seamless experience" unless the sentence carries concrete information.
- Use bold sparingly for key terms and decisions. Use inline code for field names, controls, states, enum values, and config keys.

## 5. Visual Placement

- A screenshot, diagram, or reference image should appear near the section it explains.
- Every visual needs a nearby caption that tells the reader what to look at.
- Image alt text should be short; long descriptions belong in the caption or media manifest.
- A visual that does not answer a reader question should be removed.

## 6. Resource List

Use a resource list when the document must hand off work across functions.

```markdown
### Resource List

#### Engineering
##### Purchase Flow
- [ ] Server-side validation for price, inventory space, and stock <text color="red">P0</text>
- [ ] Failure reasons mapped to client copy <text color="orange">P1</text>

#### UX / UI
##### Purchase Panel
- [ ] Default, insufficient funds, full inventory, and success states <text color="red">P0</text>
```

Rules:

- Use one function heading once, then group modules below it.
- One checklist item equals one deliverable.
- Do not use a table for the resource list.
- Within the resource-list section, do not insert blank lines before every module heading. Only insert one blank line before the second and later function headings.
- If a whole interface is one UX deliverable, bundle it as a surface and list key states below it instead of atomizing every tiny widget.

## 7. Complete Spec With UX Evidence

When UX/UI/demo exists:

- Use UX/UI/demo screenshots as interface authority.
- Do not keep early low-fidelity UI sketches as if they were final interface evidence.
- State whether values seen in screenshots are formal configuration, placeholder/demo values, TBD, or not relevant.
- If UX shows a reusable component, write the component's reuse scope, close/stacking rules, limits, and ownership boundary.

## 8. Automated Checks

`scripts/structure_lint.py` covers the mechanical subset:

- Inline role/color markers in headings.
- Header metadata not using quote-block style.
- Visible planning-facet labels.
- Internal anchors / local paths leaking into reader docs.
- `grey/gray` color usage.
- Duplicate resource-list function headings.
- Long paragraphs, missing visual captions, long image alt, bold headings, dense resource items.
- Complete specs retaining low-fidelity SVG/whiteboard-style UI sketches.

Lint is a floor, not a substitute for judgment.
