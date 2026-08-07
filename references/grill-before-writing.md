# Grill Before Writing

Use this when the design is not clear enough to write, or when the user asks to clarify, pressure-test, or "grill" the idea first.

## Boundary

- This is a pre-writing phase, not a separate deliverable unless the user asks for one.
- Do not start the final design doc until the stop conditions are met or the user explicitly asks to proceed.
- The goal is to reduce unknowns, not to make the user fill a long template.

## Question Frontier

Keep an internal question tree and ask only the highest-leverage unresolved question.

Cover these dimensions as needed:

- User/player goal and experience promise: what should they feel, understand, or repeatedly judge?
- Experience contract: main action, meaningful choice/tension, risk/cost, lasting outcome, and product/theme promise.
- Validation target: the one primary uncertainty this design or prototype must resolve.
- Main flow: entry, steps, exit, repeat rhythm.
- Interaction detail: what the user sees, chooses, receives, and sees in empty/error states.
- Rules and boundaries: allowed states, blocked states, exceptions, failure handling, transitions.
- System impact: economy, inventory, account, permissions, content, UI, backend, analytics, live ops, or other relevant systems.
- Content and values: what must be decided, what belongs to config, what needs source verification.
- Risk: ambiguous terms, old decisions that may be superseded, cross-system consequences, and stakeholder alignment.

For implementation-bound work, stop and load `experience-led-validation.md` if the expected experience or validation target is still unclear. Do not move on by collecting a longer feature list.

## Ask Format

Ask one main question at a time when the runtime supports interaction.

Each question should include:

- Why this matters now.
- The trade-off.
- A recommended answer and reason.
- 2-4 mutually exclusive choices when useful.
- A note that the user can answer freely.
- The intended destination: doc section, decision log, UX follow-up, code verification, backlog item, or handoff.

Example:

```text
Question: What should happen when the user confirms purchase but the inventory is full?
Why now: This decides whether the feature needs a reservation state, mailbox fallback, or hard failure copy.
Recommended: Hard failure for the first version, because it keeps inventory ownership simple.
Options:
- Hard failure with clear copy (Recommended)
- Auto-send to mailbox
- Reserve purchase until inventory has space
- Split into separate follow-up
Destination: Purchase flow rules + failure states + open implementation questions.
```

## Capture Answers Immediately

After each answer, decide where it belongs:

- Term clarification -> terminology / glossary / overview.
- Trade-off -> decision record.
- Case-local conclusion -> feature details.
- Stable system position -> system overview or dependencies.
- Open branch -> follow-up questions or handoff.

## Stop Conditions

Stop grilling and summarize when one is true:

- Goal, main flow, interaction, experience promise, key boundaries, and open issues are clear enough to write.
- The Experience Gate and primary validation question are clear enough to authorize a prototype or functional specification.
- Remaining questions require code, UX, data, teammate, research, or prototype verification instead of the user's oral decision.
- The user says to proceed.

The summary should include confirmed positions, unresolved questions, recommended verification, target document stage, and next output.
