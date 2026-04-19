---
name: fdd
description: Practical guidance for Feature-Driven Development in Next.js-style repositories. Use when Codex needs to place code into the correct feature slice, enforce feature isolation, keep pages routing-only, decide whether code belongs in features, commons, or commons-ui, or determine SSR/ISR ownership.
---

# Feature-Driven Development

Use this skill when the task is about feature slicing, file placement, page ownership, or shared-code boundaries in a Next.js-style repository.

Default structure assumed by this skill:
- `src/features/*`: end-to-end feature slices
- `src/pages/*`: routing entrypoints only
- `src/commons/*`: shared non-UI code
- `src/commons-ui/*`: shared UI primitives and reusable presentation

Read [references/placement-rules.md](references/placement-rules.md) when you need the decision rules for placement or SSR/ISR ownership.

Read [references/examples.md](references/examples.md) when you need concrete examples or anti-pattern comparisons.

## Core Workflow

1. Identify the user-facing capability being changed.
2. Choose the owning feature slice.
3. Keep the change inside that feature unless it is truly reusable across features.
4. Keep `src/pages/*` limited to routing and page wiring.
5. Move only domain-neutral shared logic into `src/commons/*`.
6. Move only reusable UI without business logic into `src/commons-ui/*`.
7. Reject direct feature-to-feature dependencies.
8. Prefer the repo's existing pattern before introducing a new variation.

## Default Rules

- Start local to the owning feature.
- Promote code to shared only after reuse is real, not hypothetical.
- `src/pages/*` may compose and wire features, but should not own feature business logic.
- `src/commons-ui/*` must stay free of business rules and feature-specific state.
- Shared code must be generic enough that it does not secretly belong to one feature.

## Boundaries

Use this skill to answer questions like:
- Should this code stay inside one feature?
- Is this page doing too much?
- Does this hook belong in `features` or `commons`?
- Should this component move to `commons-ui`?
- Is SSR or ISR logic owned by the page or the feature?

If the main problem is component layering, also use `$atomic-design`.

If the main problem is dependency direction or use-case placement, also use `$clean-architecture`.

If the task becomes test-first design or test placement, switch to `$tdd`.

## Review Checklist

Before finishing, verify:
- There is one clear owning feature
- No direct import from one feature into another
- `src/pages/*` remains routing-only
- Shared code is actually reusable and domain-neutral
- `commons-ui` contains presentation, not business logic

## Trigger Examples

Use this skill for prompts like:
- "Use $fdd to decide whether this code belongs in feature or commons."
- "Review boundary halaman ini, terlalu banyak logic di page atau tidak."
- "Bantu refactor biar sesuai Feature-Driven Development."
- "Logic SSR ini harus tinggal di page atau di feature?"
