# Experience-Led Validation

Use this gate before turning an idea into a feature list, detailed specification, prototype, or implementation task.

## 1. Experience Gate

Write one compact contract for the experience being validated:

| Field | Required answer |
|---|---|
| Expected experience | What should the user/player feel, understand, or repeatedly judge? |
| Actor and context | Who experiences it, and in what situation? |
| Main action | What do they actually do? |
| Choice or tension | What meaningful trade-off occupies their attention? |
| Risk or cost | What do they fear losing, wasting, or getting wrong? |
| Lasting outcome | What remains changed after success or failure? |
| Product/theme promise | Why is this experience worth having in this product or game? |
| Primary uncertainty | What is still unknown and must be verified? |

Enforce these rules:

- If the expected experience is not clear, continue discussion, research, or experience framing. Do not proceed to functional detail or implementation.
- Every implementation-bound function must serve at least one named expected-experience validation.
- For each function, state the experience it supports and the uncertainty it helps verify. If neither can be named, remove or defer it.
- Supporting scaffolding may exist only to make the validation runnable. Do not treat that scaffolding as a validated feature.
- Define the product/world promise first, then the target experience, then the core loop or user flow, and only then the functions, data, and edge cases.

State and persistence boundaries still matter when the feature needs them, but they are design content, not a universal substitute for clarifying the experience.

## 2. Validation Brief

Give each prototype or design experiment one primary question and at most three acceptance questions in total.

```markdown
## Validation Brief

- Expected experience:
- Primary question:
- Hypothesis:
- Minimum change required:
- Supporting scaffolding:
- Explicitly out of scope:
- Acceptance questions:
  1. ...
- Evidence to collect:
- Acceptance authority:
```

Use observable evidence where possible: behavior, choices, completion pattern, failure pattern, confusion, time/rhythm, or direct playtest feedback. Automated checks can establish that the prototype works technically; they cannot accept a subjective experience on the user's behalf.

## 3. Isolated Prototype Branches

Treat the integrated main prototype as the current accepted baseline. Validate uncertain modules in isolated experiment branches.

- Keep one experiment focused on one primary question.
- Use a real Git branch/worktree when the repository and task benefit from code isolation; otherwise preserve the same conceptual isolation in separate prototypes or documents.
- Do not alter the main prototype merely to make an unvalidated experiment easier.
- After the acceptance authority confirms the experience, merge the smallest reusable implementation and the normalized design conclusion.
- Do not blindly merge experiment-only scaffolding, debug controls, fake data, or unrelated refinements.
- A technically working branch is a merge candidate, not an accepted experience.

## 4. Adversarial Pre-Build Review

Before implementation, attack the proposed design:

1. **Boring optimum:** Does rational play collapse into repetition, waiting, grinding safe content, or avoiding the interesting decision?
2. **Perverse incentive:** Can the user gain by sacrificing what the design says should matter, exploiting resets, or manufacturing failure?
3. **Dependency cascade:** Does this apparently small function require a larger economy, AI, persistence, content, UI, or operations system to become coherent?
4. **Removal test:** If the function is removed, does the expected experience still validate? If yes, why is it in the current experiment?
5. **Frame check:** Is the function solving the target experience, or patching a symptom produced by an undecided higher-level structure?
6. **Promise check:** Could the same function be placed in a different product without changing meaning? If so, identify what makes its use here specific to the product/theme.

Record blockers, required revisions, and residual risks. Do not turn this into a mandatory post-playtest classification system; final acceptance and design judgment remain with the user/product owner.

## 5. Ready Conditions

A design may proceed to detailed specification or implementation only when:

- The Experience Gate is complete.
- The primary validation question is answerable by the proposed prototype or feature.
- Each implementation-bound function has an experience-validation mapping.
- The adversarial review found no unresolved structural blocker.
- The user/product owner has authorized the next step when subjective design judgment is required.
