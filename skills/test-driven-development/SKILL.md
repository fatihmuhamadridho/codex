---
name: test-driven-development
description: Use for pragmatic Test-Driven Development, including test-first changes, minimal failing tests, and safe iteration.
---

# Test-Driven Development

Use this skill when the main problem is test-first design, test placement, or deciding how to drive a change through red-green-refactor.

Read [references/test-selection.md](references/test-selection.md) when you need to choose the first test level or decide whether a case should stay unit, integration, or end-to-end.

Read [references/test-seams.md](references/test-seams.md) when you need to create seams around IO, time, randomness, frameworks, or external services.

Read [references/anti-patterns.md](references/anti-patterns.md) when a test plan feels brittle, over-mocked, or retrofitted after the implementation already exists.

## Core Workflow

1. State the behavior to prove before touching production code.
2. Pick the smallest test that can fail for that behavior.
3. Write the failing test first.
4. Implement the minimum production change needed to pass.
5. Re-run the relevant tests until the change is green.
6. Refactor only while the tests stay green.
7. Repeat in small slices until the requested behavior is complete.

## Default Rules

- Start from observable behavior, not private implementation details.
- Prefer the lowest test level that proves the behavior with confidence.
- Write one failing test for one behavioral slice at a time.
- Keep test setup small enough that the assertion remains obvious.
- Replace hard dependencies with seams only when the test needs control over them.
- Use integration tests to verify boundaries, not to cover every branch.
- Refactor production code and tests together after green, not before red.
- Treat legacy code as incremental TDD: characterize current behavior first, then tighten around the change.

## Pragmatic Exceptions

- For exploratory spikes, allow throwaway code without full TDD, then restart with tests before keeping the result.
- For legacy areas with no safe seam, start with characterization tests before changing behavior.
- For infrastructure-heavy flows, begin with one integration test at the real boundary, then drive inner logic downward with smaller tests.
- If a bug is only reproducible end-to-end, capture that failure first, then add narrower tests as the code becomes more isolatable.

## Boundaries

Use this skill for questions like:
- What is the first failing test I should write here?
- Should this behavior be covered by a unit test or an integration test?
- Where should this test live?
- How do I create a seam around this dependency?
- How do I apply TDD in a messy or legacy area?

If the main problem becomes feature ownership or page boundaries, also use `$feature-driven-development`.

If the main problem becomes dependency direction or layer placement, also use `$clean-architecture`.

If the task is mainly about repo-wide implementation consistency rather than testing workflow, also use `$repo-conventions`.

## Review Checklist

Before finishing, verify:
- there is a clear behavior statement behind each new test
- the first new test failed before the implementation changed
- the chosen test level is the smallest one that gives enough confidence
- tests assert user-visible or contract-visible outcomes
- mocks and fakes support the behavior under test instead of mirroring implementation structure
- refactors happened only after green
- legacy or boundary-heavy work still has a documented reason for any TDD shortcut

## Trigger Examples

Use this skill for prompts like:
- "Use $test-driven-development to drive this bug fix from a failing test."
- "Help me choose the first test to write before implementing this feature."
- "Apply pragmatic TDD in this legacy module."
- "Bantu kerjakan ini pakai TDD."
- "Test dulu, baru implement logic ini."
