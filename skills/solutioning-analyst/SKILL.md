---
name: solutioning-analyst
description: Use for turning a Figma link, screenshot, or UI image into backend-oriented solutioning, API flow, and technical scope.
---

# Solutioning Analyst

Use this skill to turn UI evidence into a technical solutioning draft for one feature at a time.

Prefer this skill for requests such as:

- "buat solutioning"
- "analyze figma jadi backend spec"
- "tentuin fitur dari figma"
- "buat API contract dari screen ini"
- "buat objective overview sampai status code"

Do not use this skill for pure product discovery, UI copy review, or broad multi-feature BRDs where no single feature can be scoped safely.

## Inputs

Accept any of these as the primary source:

- Figma link
- image attachment
- local image file exported from Figma

Optional supporting context:

- feature hints from the user
- actor or role names
- domain vocabulary
- business constraints that are already known
- preferred output language: `id` or `en`

## Workflow

1. Inspect the Figma link or image and infer the likely feature scope.
2. If multiple screens or flows appear, choose one primary feature only.
3. State the chosen feature name early and make the scoping assumption explicit.
4. Derive the actor, business objective, core state changes, backend entities, and persistence needs.
5. Identify synchronous flow, asynchronous side effects, validations, and negative cases.
6. Produce the final document in Markdown with Mermaid diagrams.
7. Save one file per feature at `docs/solutioning/<feature-slug>/<yyyy-mm-dd>-<feature-slug>.md` unless the user asks for another location.

## Language Mode

- Default to the user's preferred language if it is explicit.
- If the user does not specify, use Bahasa Indonesia.
- If the user asks for English, keep the entire document in English, including section prose, bullet text, and table descriptions.
- Keep code blocks, Mermaid syntax, endpoint paths, and status codes unchanged across languages.

## Scope Rules

- Default to `one feature doc` per request.
- If the source is ambiguous, list 2-3 candidate feature names internally, then lock one as the primary scope in the output.
- Prefer the feature that best explains the main call to action, main data form, or main workflow transition shown on the screen.
- If the UI contains list, detail, create, edit, and history views of the same domain, treat them as one feature only when they are clearly one lifecycle.
- If the material still does not support a confident backend design, produce a conservative draft and add a short `Assumptions` section after the 8 required sections.

Use [references/feature-inference-rules.md](references/feature-inference-rules.md) when the feature boundary is unclear.

## Output Contract

Always generate these 8 sections in this order:

1. `Objective Overview`
2. `Ringkasan Alur & Cara Kerja Sistem`
3. `Business Rules`
4. `Table Design`
5. `Sequence Diagram`
6. `State Diagram`
7. `API Contract`
8. `Table Status Code`

Rules for each output:

- Write the document in Markdown.
- Write `Sequence Diagram` and `State Diagram` as fenced `mermaid` blocks.
- Keep the document backend-oriented, not a product brief.
- Reflect the style of the provided examples by covering lifecycle, validation, cascade effects, async work, and contract-level detail when relevant.
- Do not copy wording from example documents.
- For `State Diagram`, prefer a business-state card style:
  - each node should represent a meaningful lifecycle state of the domain entity, not a temporary UI or transport state
  - each node should include the state name plus 1-3 short lines that explain business meaning, data condition, inventory/lock effect, or downstream effect when relevant
  - transitions should be labeled with business events such as submit, approve, reject, save draft, activate, finish, or resubmit
  - avoid generic technical states like `SAVING`, `LOADING`, or `UPLOADING` unless the feature itself is fundamentally an async job lifecycle
  - when the source image suggests a richer workflow map, mirror that richness rather than collapsing it into a minimal enum-only diagram
  - when the desired output is visually closer to a workflow board or status-map, prefer Mermaid `flowchart TB` or `flowchart LR` instead of `stateDiagram-v2` so the layout can stay directional and avoid circular auto-routing
  - use `stateDiagram-v2` only when the lifecycle is simple and the rendered layout will remain readable
  - if Mermaid still routes edges in a circular way, force the layout with `subgraph` rows or columns so states stay in deliberate lanes similar to the reference image
  - prefer one-way reading lanes first; only add return arrows when the business flow truly needs them
  - when the user wants rigid lines, add Mermaid init config for flowchart curves such as `%%{init: {'flowchart': {'curve': 'stepBefore'}}}%%`
  - prefer the main reading direction `LR` first, then use `TB` only inside lanes or subgraphs when the user explicitly wants left-to-right then downward flow
  - if horizontal lanes still create crossing arrows, switch the outer layout to `flowchart TB` and arrange states into 2-3 `LR` rows so the reader scans left-to-right within each row, then top-to-bottom across rows
  - keep the happy path grouped in one directional band and place rejection or failure states on a separate row or side to reduce edge collisions
  - reduce the number of return arrows; if two recovery transitions point back into the same working state, prefer the closest target and avoid decorative loops

Use [references/output-template.md](references/output-template.md) as the shape of the final document.

## API and Data Modeling Rules

- `Table Design` must describe real domain tables or aggregates, not placeholder generic tables.
- For each table, include purpose and key fields with type, constraint, and notes.
- `API Contract` must cover the main endpoints needed by the feature, not every imaginable endpoint.
- Each endpoint should include method, path, auth expectation, request shape, validation, success response, negative cases, and at least one concrete example response for each important negative case.
- Write negative cases in a compact format:
  - `404` Showtime not found
    - `Example response:`
    - JSON response example
- Always include list and detail endpoints when the screen clearly represents a CRUD master-data flow with a detail or modal view.
- Use these default endpoint patterns unless the user or screen evidence says otherwise:
  - list: `GET /<feature>/v1/list`
  - detail: `GET /<feature>/v1/detail/{id}`
  - create: `POST /<feature>/v1/submit`
  - update: `PUT /<feature>/v1/update/{id}`
  - delete: `DELETE /<feature>/v1/delete/{id}`
- `Table Status Code` must stay consistent with the API contract.
- When the UI implies status transitions, include a state model even if the exact enum names are inferred conservatively.
- Favor durable lifecycle states over ephemeral interaction states. If a file upload or save action only supports a larger domain lifecycle, model the persisted business outcome instead of the front-end request phase.
- If the feature has a dense approval or release flow, optimize the state section for readability of the path first, even if that means using a Mermaid flowchart with state-like cards rather than a literal state-machine syntax.
- When choosing between semantic completeness and readability, prefer the clearer diagram. Omit low-value alternate arrows if they make the path harder to follow.

Use [references/api-contract-shape.md](references/api-contract-shape.md) for the minimum API contract depth and response structure.

## Recommended Execution Pattern

When the request is substantial, use `solutioning_analyst` to produce the backend analysis and then normalize the final write-up into the required 8-section format.

When using `solutioning_analyst`, keep the delegated goal specific:

- identify the feature and actor
- derive business rules and persistence model
- define state transitions and async side effects
- produce API contract and error/status table

Then consolidate the result into one final Markdown document.

## Validation Checklist

Before stopping, verify that:

- the chosen feature name is explicit
- exactly the 8 required sections exist and are ordered correctly
- both diagrams are valid Mermaid blocks
- the state diagram uses business lifecycle states, not page or request phases, unless the feature genuinely is a processing pipeline
- the chosen Mermaid syntax keeps the layout readable and does not create unnecessary circular routing when a directed workflow card layout is more appropriate
- the state diagram separates major outcomes like success and rejection enough that arrow direction remains easy to follow
- `Table Design` includes the core entities implied by the UI
- `API Contract` includes at least one positive path and relevant negative paths
- `Table Status Code` aligns with the API contract
- any uncertainty is captured briefly in `Assumptions` after the mandatory sections
