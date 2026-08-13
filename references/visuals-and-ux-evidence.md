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

For a system design spec, visual coverage is checked per reader task, not per document:

- one overview visual for the main flow when it spans multiple states, containers, screens, or systems;
- one local visual for each major operation module when a visual can carry its core relationship more directly than prose;
- an explicit visual requirement and insertion point when the final UI, screenshot, asset, or diagram is not yet available.

Preserve the source document's existing images, image requests, captions, and layout requirements during rewrites. Preserve its surrounding rich-text conventions too, including caption block style, indentation, spacing, and placement. Do not interpret prose compression as permission to discard or restyle them. Divide information so the visual owns flow/state/layout and text owns exceptions/feedback/TBDs; neither should narrate the other.

Before authoring each system diagram, state one reader question it must answer. Make the valid path visually continuous, place a prohibition only on the exact forbidden edge, and inspect the rendered figure without relying on its caption. If the figure can imply the opposite rule, it fails even when it looks polished.

### Project F1 system-spec diagrams

For Project F1 system design specs, use self-contained SVG as the default and final source format for authored flow, state, relationship, and system diagrams. Mermaid may be used only as private planning notation and must not be published as the final figure unless the user explicitly requests Mermaid.

- Preserve each SVG source file beside the Markdown package under `media/`.
- When publishing to Feishu, insert the complete SVG through `<whiteboard type="svg">...</whiteboard>` or its supported local-file expansion; do not rasterize it first unless SVG insertion is unavailable.
- Follow the Feishu SVG parser constraints: include an `<svg>` root and `viewBox`, use `<text>` / `<tspan>` for text, keep the diagram self-contained, prefer orthogonal connectors, and avoid unsupported filters, masks, patterns, clipping, and radial gradients.
- Export or query each inserted whiteboard as a rendered preview and visually inspect it before delivery.

## 3. Complete Spec UX Evidence

Use this pipeline when UX/UI/demo exists:

1. Confirm the doc is a complete spec, not an early draft.
2. Put the UX/UI/demo authority source in the header.
3. Identify the smallest screenshot range that explains each major feature point.
4. Place each screenshot next to the rule it supports.
5. Add a caption that says what the reader should look at.
6. Record source, insertion point, authority, value status, and uncertainty in a media manifest.
7. Remove early low-fidelity UI sketches unless they explain non-UI logic that UX does not cover; mark those as `non-ui-diagram-exception`.

Do not treat a UX/UI/demo link alone as enough for a complete spec. The reader should see the relevant interface while reading the rule. If the current environment cannot export or insert screenshots, create a media handoff/manifest that names the missing screenshots, source links, intended insertion points, and blocker.

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
- A complete spec with a UX/UI/demo source has screenshots or an explicit media handoff/manifest.
- Screenshot values are not silently treated as final rules.
- Complete specs do not retain early UI SVGs as final interface evidence.
- Uncertain mappings are labeled `needs-followup`.
- Project F1 system-diagram sources are SVG, inserted as SVG whiteboards in Feishu, and verified through rendered preview.
