# TDD Anti-Patterns

Use this reference when tests feel brittle or when the workflow stopped being test-first.

## Common Problems

- Writing the implementation first, then backfilling tests and calling it TDD.
- Asserting private helpers or internal method calls instead of behavior.
- Over-mocking every dependency until the test only mirrors the implementation.
- Writing large scenario tests that hide which rule actually failed.
- Refactoring in the red phase and losing the signal from the failing test.
- Keeping flaky tests as if they still provide safety.

## Corrections

- Go back to one small failing test for one behavior slice.
- Collapse mock-heavy tests into simpler fakes or a higher-level integration test.
- Rewrite assertions around outputs, state, emitted events, or public contracts.
- Split one broad scenario into several narrow tests with explicit intent.
- Stabilize or delete flaky tests before trusting them.

## Legacy Warning Signs

- The code cannot be tested without booting half the system.
- A small behavior change forces massive fixture setup.
- The test only passes if it knows the exact implementation shape.

When these signs appear, add a characterization test around current behavior, create one seam, and then continue in smaller TDD steps.
