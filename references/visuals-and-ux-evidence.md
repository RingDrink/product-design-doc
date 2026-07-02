# Visuals And UX Evidence

Design docs should use visuals when visuals reduce ambiguity. The visual strategy depends on the document stage.

## 1. Stage Strategy

| Stage | Visual strategy |
|---|---|
| Exploration | Rough diagrams, reference screenshots, decision sketches |
| Early draft | Flow diagrams, UI sketches, competitor references, lightweight mockups |
| UX alignment | Screen-flow diagrams, prototype/demo screenshots, annotated questions for UX |
| Complete spec | Real UX/UI/demo screenshots first; diagrams only for non-UI logic not covered by UX |

## 2. Visual Selection

| Need | Use |
|---|---|
| Main loop / scope / system relationship | Flowchart, mindmap, system map |
| Multi-screen navigation | Screen-flow / navigation map |
| Single object lifecycle | State machine |
| Multi-role timing | Swimlane / timeline |
| Spatial relation / range / hit area | Top-down sketch |
| UI behavior after UX is available | UX/UI/demo screenshot |
| Parameters / enum / comparison | Table |
| Exact algorithm / branching threshold | Pseudocode or table, not decorative diagram |

Rule of thumb: if prose contains three or more arrows (`A -> B -> C`) or multiple screens in one sentence, make a diagram or place a UX screenshot near the section.

## 3. Complete Spec UX Evidence

Use this pipeline when UX/UI/demo exists:

1. Confirm the doc is a complete spec, not an early draft.
2. Put the UX/UI/demo authority source in the header.
3. Identify the smallest screenshot range that explains each major feature point.
4. Place each screenshot next to the rule it supports.
5. Add a caption that says what the reader should look at.
6. Record source, insertion point, authority, value status, and uncertainty in a media manifest.
7. Remove early low-fidelity UI sketches unless they explain non-UI logic that UX does not cover; mark those as `non-ui-diagram-exception`.

## 4. Figma Or Design Tool Adapter

If Figma or another design-tool adapter is available:

- Read only the relevant page/frame/node area; do not dump an entire file into context.
- Prefer stable screen/frame/component exports over cropping a huge canvas.
- Record node/frame id, name, bounds, screenshot path, and confidence.
- If login or permission fails, say so and use supplied screenshots, exported images, demo screenshots, or a text-only fallback.

If the design file is spatially organized rather than split by files/pages, build a local index:

```markdown
| Area / Frame | Feature | Source node | Key screens | Paired doc/demo | Notes |
|---|---|---|---|---|---|
```

## 5. Media Manifest

Use `templates/media-manifest-template.md` or this field set:

| Field | Meaning |
|---|---|
| `feature` | Feature point / overview section |
| `source_type` | figma-frame / ui-spec / demo / screenshot / reference / generated |
| `source_link` | URL or source path |
| `node_or_region` | Node id, frame id, or crop region |
| `image_path` | Local output path when applicable |
| `insert_after` | Heading or anchor sentence |
| `caption` | What the reader should look at |
| `alt_text` | Short alt text |
| `authority_scope` | ux-authoritative / doc-rules-authoritative / reference-only |
| `value_status` | formal-config / demo-placeholder / tbd / none |
| `component_scope` | Reusable component name and scope, if any |
| `diagram_exception` | `none` or `non-ui-diagram-exception: reason` |
| `confidence` | high / medium / low |
| `notes` | Follow-up, risk, permission issue |

## 6. Quality Gate

- Screenshot is non-empty, readable, and cropped to the relevant area.
- Visual is near the text it explains.
- Caption explains the reading path or state difference.
- Screenshot values are not silently treated as final rules.
- Complete specs do not retain early UI SVGs as final interface evidence.
- Uncertain mappings are labeled `needs-followup`.
