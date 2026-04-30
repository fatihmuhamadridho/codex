# Placement Rules

Use this reference when you need a deterministic answer about where code should live.

## Decision Order

1. Start with the feature that owns the user-facing behavior.
2. Keep code there unless it is clearly reused or should be reused by multiple features.
3. Move code to shared only when it stays meaningful outside the original feature.
4. Keep route-only concerns at the page boundary.

## `src/features/*`

Place code in a feature when it:
- serves one user-facing capability
- contains business rules or feature-specific state
- supports one screen flow, use case, or domain subflow
- would be awkward or misleading if imported by unrelated features

Typical candidates:
- feature containers
- feature hooks
- selectors tied to one feature
- feature-specific API adapters
- feature state and orchestration
- feature forms and validation

Do not extract from a feature just because the file is large. Size alone is not a reason to move code to shared.

## `src/pages/*`

Keep code in `src/pages/*` only when it is route wiring.

Allowed:
- route entrypoint composition
- page-level metadata
- SSR or ISR entry functions
- parameter parsing tied to the route
- selecting which feature view gets rendered

Avoid in pages:
- feature business logic
- reusable domain hooks
- component trees that really belong to a feature
- direct data transformation that a feature owns

When SSR or ISR is used, the page owns the route contract and request boundary. The feature should own feature-specific mapping, orchestration, and behavior once the route hands data off.

## `src/commons/*`

Move code to `src/commons/*` only when it is:
- non-UI
- reused by multiple features, or clearly intended to be shared soon across them
- domain-neutral enough to stand on its own

Typical candidates:
- generic utility functions
- shared HTTP client wrappers
- common formatting helpers
- reusable storage or environment adapters
- shared validators that are not feature-owned

Reject moves to `commons` when the code still speaks in one feature's language or encodes one feature's rules.

## `src/commons-ui/*`

Move code to `src/commons-ui/*` only when it is reusable UI with no business logic.

Typical candidates:
- buttons, inputs, modals, tables, tabs
- reusable layout shells
- form field shells without feature rules
- visual states and design-system components

Do not place code here if it:
- fetches feature data
- knows one feature's workflow
- embeds feature-specific validation or branching
- coordinates one domain flow

## Feature-to-Feature Dependencies

Do not create direct imports from one feature into another.

If two features need the same thing:
- keep it in one feature if the reuse is accidental and short-lived
- extract it to shared only if the abstraction is generic and stable
- otherwise duplicate a small amount of code rather than binding features together

## SSR and ISR Ownership

Use this split:
- page owns route params, route lifecycle, and framework entrypoints
- feature owns the capability-specific transformation and UI behavior

A good rule is:
- if the logic exists because of Next.js routing, keep it in `pages`
- if the logic exists because of the product capability, keep it in the owning feature
