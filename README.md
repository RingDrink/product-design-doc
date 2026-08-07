# product-design-doc

A portable agent skill for writing product / game feature design documents.

It turns a vague feature idea, design discussion, UX source, or existing draft into a readable design doc that product, UX, engineering, or game-dev teams can act on. Before implementation, an Experience Gate requires every function to serve a named expected-experience validation. The workflow is split into a **Core** (experience framing, isolated prototype validation, adversarial review, question-grilling, stage classification, writing conventions, visuals/UX evidence, lint, handoff) and optional **Adapters** (interaction channel, project memory, publishing platform, Figma, long-run checkpointing), so it works in any agent framework that supports Markdown-based skills.

## Install

Copy this directory into your agent's skills folder (e.g. `~/.claude/skills/`, `~/.codex/skills/`, or your framework's equivalent). The entry point is [SKILL.md](SKILL.md).

This Git repository is the shared authority for Codex, Claude, and OpenClaw installations. Runtime copies or junctions are derived installs; update the repository first, then pull or relink it instead of maintaining divergent skill text per runtime.

## Contents

- [SKILL.md](SKILL.md) — entry point: routing, core workflow, output contract, verification.
- [references/](references/) — detailed guides loaded on demand (experience-led validation, core workflow, grilling, structure conventions, visuals/UX evidence, adapters).
- [templates/](templates/) — delegation brief and media manifest templates.
- [scripts/structure_lint.py](scripts/structure_lint.py) — mechanical structure/readability lint for Markdown drafts; Python 3 stdlib only.

## Lint

```bash
python3 scripts/structure_lint.py draft.md          # ERRORs fail
python3 scripts/structure_lint.py --strict draft.md # WARNs also fail
python3 scripts/structure_lint.py --rendered exported.html
```

Lint is a floor, not a substitute for judgment — occasional false positives (e.g. `D-Pad-1`-shaped strings matching the internal-id pattern, `[[wikilinks]]`) can be overridden deliberately.

## Notes

- Resource-list examples use `<text color="...">` markup as an optional priority-color convention. If the target platform does not support it, replace it with plain text or bold priority labels.
