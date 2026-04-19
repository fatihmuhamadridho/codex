# Test Seams

Use this reference when production code is hard to control in tests.

## Typical Seams

- Time: inject a clock or time provider.
- Randomness: inject a deterministic source.
- Network: wrap clients behind an adapter or gateway interface.
- Filesystem: isolate file operations behind a port or helper.
- Framework globals: move logic behind thin wrappers so the domain code sees plain inputs.
- Process environment: read env vars once, then pass concrete values inward.

## Seam Rules

- Introduce the smallest seam that gives the test control it needs.
- Prefer seams at module boundaries over seams inside core logic.
- Do not create abstractions only for hypothetical reuse.
- Keep adapters thin and test the business rule separately from the transport.

## Fakes, Stubs, and Mocks

- Prefer simple fakes for stateful collaborators.
- Use stubs when only return values matter.
- Use mocks only when interaction order or call shape is itself part of the contract.
- Avoid asserting every internal call when the observable result is enough.
