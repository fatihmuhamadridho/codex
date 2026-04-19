# Test Selection

Use this reference when deciding the first test to write.

## Selection Order

1. Start with the lowest test level that can prove the behavior.
2. Move upward only when the behavior depends on a real boundary.
3. Keep expensive tests few and targeted.

## Heuristics

- Choose a unit test when the behavior is pure logic, branching, mapping, validation, calculation, or state transition.
- Choose an integration test when correctness depends on framework wiring, persistence, serialization, network adapters, queues, or multiple collaborating modules.
- Choose an end-to-end test when the bug only appears through the real user journey or the external contract must be proven intact.

## Escalation Rules

- If a unit test needs too many mocks to feel credible, step up to integration.
- If an integration test is slow but the core decision logic is isolated, keep one boundary test and push the inner cases down to unit tests.
- If an end-to-end test finds a regression, keep that regression test only if it protects a real journey; add smaller tests for the inner rules.

## Placement Rules

- Place tests next to the code when the repo already follows co-location.
- Place tests in dedicated test trees when the repo already centralizes them.
- Follow the nearest existing convention before introducing a new layout.
