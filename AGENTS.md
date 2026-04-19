@/home/fatihmuhamadridho/.codex/RTK.md

## Custom Subagents

### `project_analyst`

Use this subagent when the task is about product or project analysis before implementation.

Call `project_analyst` when you need to:
- analyze a feature or business requirement
- map user flow or system flow from a product perspective
- define scope, assumptions, dependencies, or risks
- write acceptance criteria
- break a feature into backlog items, stories, or tasks
- prepare story sizing in spreadsheet form when the user wants detailed acceptance criteria output similar to an existing sizing sheet

Do not use `project_analyst` for detailed backend API contract design when the main need is request payloads, response schemas, error formats, or endpoint behavior. Use `solutioning_analyst` for that.

Example prompts:
- "Use `project_analyst` to break this feature idea into flow, acceptance criteria, and backlog."
- "Spawn `project_analyst` to analyze the scope and list risks and open questions."
- "Use `project_analyst` to turn this feature into a story sizing sheet like the Example tab."
- "Use `project_analyst` to produce detailed positive flow and negative flow acceptance criteria in sheet form."

Output storage:
- Save `project_analyst` results in spreadsheet form for session-based tracking.
- Default template: `/home/fatihmuhamadridho/.codex/artifacts/templates/project-analysis-template.csv`
- Preferred usage: duplicate the template into a dated working file and update one row per analyzed feature or item.
- When the task is specifically story sizing, prefer writing directly to the target Google Sheet tab using an acceptance-criteria layout with `No`, `Acceptance Criteria`, `Given`, `When`, and `Then`, and make sure the sheet covers detailed positive flow and negative flow rows instead of a compressed summary.

### `solutioning_analyst`

Use this subagent when the task is about backend solution analysis or API design before implementation.

Call `solutioning_analyst` when you need to:
- analyze backend requirements for a feature
- define API flow end-to-end
- design request payloads, headers, params, and validation rules
- define response schema, status codes, and error contract
- analyze downstream integrations, idempotency, retries, side effects, or state changes
- break backend work into technical backlog items

Do not use `solutioning_analyst` for general product discovery, user journey framing, or acceptance criteria that are primarily product-facing unless backend contract design is the main concern. Use `project_analyst` for that.

Example prompts:
- "Use `solutioning_analyst` to define the API contract for this feature, including payload and response format."
- "Spawn `solutioning_analyst` to analyze backend flow, validation, error handling, and integration dependencies."

Output storage:
- Save `solutioning_analyst` results as Markdown technical analysis.
- Default template: `/home/fatihmuhamadridho/.codex/docs/solutioning/templates/solutioning-analysis-template.md`
- Preferred usage: create a dated file per feature under `docs/solutioning/<feature-slug>/`.
