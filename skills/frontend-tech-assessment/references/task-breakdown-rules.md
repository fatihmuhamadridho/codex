# Task Breakdown Rules

Break each module into frontend tasks that are small enough to estimate and implement independently.

## Core splitting rules

- Split main page or list view from modal, drawer, or detail surfaces.
- Split UI slicing from API integration.
- Split create, update, and delete flows when they use separate forms or interactions.
- Split role or access handling if the module has explicit permission behavior.
- Split state handling when it is materially different:
  - loading
  - empty
  - validation
  - submit failure
  - fetch failure

## Typical FE task patterns

Common task shapes include:

- `[FE] Slicing <Module> Page`
- `[FE] Integrasi API Get List <Module>`
- `[FE] Slicing Modal Create <Module>`
- `[FE] Integrasi API Create <Module>`
- `[FE] Slicing Modal Update <Module>`
- `[FE] Integrasi API Update <Module>`
- `[FE] Slicing Modal Delete <Module>`
- `[FE] Integrasi API Delete <Module>`
- `[FE] Handle Empty State <Module>`
- `[FE] Handle Error State <Module>`
- `[FE] Implement RBAC Access for <Module>`

Do not force every pattern into every module. Only include the tasks implied by the sources.

## CRUD and config rules

- For admin modules, assume list plus CRUD unless the requirement clearly limits the operations.
- For configuration-heavy modules, add separate FE tasks for config forms or settings groups when the fields are materially different, such as revenue split, pricing, session duration, or call limit settings.
- For dashboard summary pages, split widget rendering from transaction or action forms when they are distinct UI surfaces.

## Figma and flow-driven rules

- If a Figma flow shows multiple screens or variants, break them into separate FE tasks.
- If a flow image reveals a multistep journey, split the FE work by step transition and validation surface.
- If the design includes modal confirmation, OTP input, or scanner flow, create dedicated FE tasks instead of burying them inside one generic row.

## Scope exclusions

Do not include:

- backend endpoint creation
- database work
- deployment or infra work
- QA-only execution tasks
- mobile implementation unless explicitly requested

## Estimation guidance

Use coarse estimates only. Favor simple increments such as:

- `0.5` for small isolated FE surfaces
- `1` for standard page slice or single API integration
- `1.5` to `2` for more complex forms, guards, or multi-state views

Keep estimates internally consistent within the same sheet.
