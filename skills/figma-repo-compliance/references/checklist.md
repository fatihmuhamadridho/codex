# Checklist

Use this checklist before considering a Figma-driven implementation complete.

## Figma Context

- The intended frame or node is unambiguous
- If the link was unclear, a screenshot was requested instead of guessing
- The built screen matches the intended design target, not a nearby variant

## Repo Targeting

- The work landed in the correct feature or route
- A new feature was not incorrectly merged into an unrelated existing page
- Existing feature code was extended only when the design truly belonged there

## Component Reuse

- Existing repo components were checked before creating new UI
- Shared UI patterns were reused where available
- New UI abstractions were added only when the repo did not already provide them

## Native HTML

- Native tags were not used as the default implementation strategy
- If native HTML was used, it was limited and intentional
- The screen was not built mostly out of raw primitives when repo abstractions existed

## Structural Quality

- Page-level code is still routing or composition oriented
- Feature logic stays in the owning feature
- Shared code is actually shared and not disguised feature code
- No direct feature-to-feature dependency was introduced

## Visual Quality

- Layout and hierarchy match the Figma target
- Existing design tokens or component variants were used where possible
- The implementation feels like part of the repo, not a separate one-off screen
