# Optional Adapters

Adapters bind the portable workflow to a runtime or team environment. Use only adapters that are available and relevant.

## 1. Interaction Adapter

Core rule: ask one high-leverage question at a time when live interaction is possible.

Examples:

- Chat runtime with question UI: use the question UI.
- Plain chat: ask one concise question in normal text.
- No live user access: write a question list and mark blockers.
- Team form or chat workflow: use it only if installed and authenticated.

Never pretend a question has been answered because the preferred interaction tool is unavailable.

## 2. Project Memory Adapter

Core rule: meaningful decisions should not live only in chat.

If the project has a decision log, wiki, ADR, project memory, ticket system, or knowledge base, write or propose entries there according to local rules.

If no such system exists, include a portable decision block in the doc or `handoff.md`:

```markdown
## Decision Record
- Source:
- Context:
- Decision:
- Alternatives:
- Scope:
- Status:
- Follow-up:
```

Do not force a specific knowledge-base path, file layout, or naming scheme.

### Jyun personal routing

For Jyun's environment, keep personal and project knowledge separate:

- Unqualified `KB` means Jyun's personal library (`study`). Reflux only reusable, de-identified methods, preferences, and cross-project lessons.
- `FF` means the FireForge project knowledge base. Store company/project facts, current decisions, internal links, and implementation state there.
- If both are needed, write two distinct entries with different scopes; never copy company facts into the personal KB.

## 3. Publishing Adapter

Default publishing target is Markdown.

If a document platform is available:

- Prefer platform-native structures for headings, lists, tables, images, and comments.
- Before overwriting a published doc, explain the impact and get confirmation unless the user explicitly asked for overwrite.
- When editing an existing published doc with comments/images/embedded blocks, prefer localized edits and verify after writing.
- After publishing or exporting, fetch/export the produced artifact when possible and run rendered lint: `python3 scripts/structure_lint.py --rendered <exported.md|html|xml>`.
- If the platform adapter is supposed to generate numbered feature headings, run the rendered lint with `--require-numbered-headings`.
- If publishing fails or permissions are missing, deliver the Markdown package and a publish handoff.

Potential platforms include team wikis, document suites, issue trackers, code-hosted docs, or local docs repos. None is required by Core.

## 4. UX / Figma Adapter

Use `visuals-and-ux-evidence.md`.

If the environment has a Figma connector, follow its local skill/tool instructions before querying. If no connector exists, use exported screenshots or links and mark any unverified mapping.

## 5. Lint Adapter

Core lint is `scripts/structure_lint.py` and has no external dependency.

Use two gates:

- **Source gate**: `python3 scripts/structure_lint.py <draft.md>` before handoff.
- **Rendered gate**: `python3 scripts/structure_lint.py --rendered <exported.md|html|xml>` after a publishing/export adapter changes the artifact.

Teams may add stricter local checks, but local checks should not change the meaning of Core. If a local check is about platform rendering, generated numbering, or team style, keep it in the adapter layer and document the exact command.

## 6. Long-Run / Quota Adapter

If the runtime has token, time, quota, or context limits:

- Checkpoint before long extraction, publishing, or delegation.
- Checkpoint after failed verification.
- Checkpoint before stopping.

Use the project's existing handoff if present. Otherwise create `handoff.md` beside the draft.

## 7. F1 Shared Design Context Adapter (Lilith / Project F1)

When the task is a Project F1 design doc, pull the producer-maintained shared references before writing:

- Keep `product-design-doc` Core as the writing authority. Project F1 `design-mode` or other project capabilities may supply facts, red lines, coupling checks, output paths, source-control rules, and handoff constraints, but their templates do not replace the source document frame or this Core.
- Do not register this personal Skill in the Project F1 team selector and do not copy its Core rules into Project F1 shared Skills. Invoke it from Jyun's personal Agent entry, then compose only the required project adapters.

- Source page: 《香槟的共享 Skill》 `https://lilithgames.feishu.cn/wiki/K9xAwDcOUiCxMFkAJmMcXowJnoc`
- References under 附属Skill: **F1 StoryDesign** (design-judgment baseline: story generation, sandboxization, theme boundary) and **F1 Product Gameplay Design Index** (product context index: formed directions, active designs, maturity labels).
- Fetch the page with `lark-cli docs +fetch`, locate the attachment tokens, download the latest with `lark-cli docs +media-download`. If the refresh is unavailable, use the most recent local copy and state that it may be stale; do not block writing on a failed refresh.
- Treat both as read-only upstream. Maturity labels decide constraint strength: formed directions constrain the design; seed / in-progress entries are references only.
- Conclusions produced in a design run are proposals. Never write back to the shared page or its attachments; only the catalog owner (徐昌斌 / 香槟) reviews and publishes.
- On conflict with local project knowledge or the user's current instruction, surface the conflict explicitly instead of silently merging.
