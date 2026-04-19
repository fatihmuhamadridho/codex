# Red Flags

Use this reference when a Figma-driven implementation feels wrong.

## Figma Intake Failures

- Continuing from a Figma link that was not actually readable
- Guessing the target frame from a broad file link
- Building from the wrong screen because the node was not confirmed

When these happen, stop and ask for a screenshot.

## Repo Compliance Failures

- Implementing a brand new feature by editing an unrelated existing page
- Putting most of the screen logic directly in the route entry file
- Ignoring an existing component library or design-system layer
- Creating new wrappers with vague names instead of using known repo patterns

## Component Failures

- Building the page mostly from `div`, `span`, `button`, `input`, and other raw tags even though the repo already has abstractions
- Creating page-only mega components with no meaningful child boundaries
- Adding new shared components when the reuse is hypothetical rather than real

## Boundary Failures

- One feature importing another feature directly
- `commons-ui` receiving business logic
- shared helpers using one feature's language and rules
- page code acting as the real feature container

## Smell Test

If the implementation would surprise a repo maintainer because it ignores existing components, lands in the wrong feature, or looks unrelated to the target Figma screen, treat that as a failure and re-evaluate before continuing.
