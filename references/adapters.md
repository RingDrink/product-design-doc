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

## 3. Publishing Adapter

Default publishing target is Markdown.

If a document platform is available:

- Prefer platform-native structures for headings, lists, tables, images, and comments.
- Before overwriting a published doc, explain the impact and get confirmation unless the user explicitly asked for overwrite.
- When editing an existing published doc with comments/images/embedded blocks, prefer localized edits and verify after writing.
- If publishing fails or permissions are missing, deliver the Markdown package and a publish handoff.

Potential platforms include team wikis, document suites, issue trackers, code-hosted docs, or local docs repos. None is required by Core.

## 4. UX / Figma Adapter

Use `visuals-and-ux-evidence.md`.

If the environment has a Figma connector, follow its local skill/tool instructions before querying. If no connector exists, use exported screenshots or links and mark any unverified mapping.

## 5. Lint Adapter

Core lint is `scripts/structure_lint.py` and has no external dependency.

Teams may add stricter local checks, but local checks should not change the meaning of Core. If a local check is about platform rendering or team style, keep it in the adapter layer.

## 6. Long-Run / Quota Adapter

If the runtime has token, time, quota, or context limits:

- Checkpoint before long extraction, publishing, or delegation.
- Checkpoint after failed verification.
- Checkpoint before stopping.

Use the project's existing handoff if present. Otherwise create `handoff.md` beside the draft.
