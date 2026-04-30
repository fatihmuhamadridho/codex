---
name: frontend-tech-assessment
description: Break down frontend implementation tasks from BRDs, spreadsheets, analyst outputs, Figma, and flow images into grouped FE assessment sheets with coarse manday estimates.
---

# Frontend Tech Assessment

Use this skill when the user wants a frontend tech assessment, frontend task breakdown, or FE implementation worksheet derived from one or more requirement sources.

This skill is for turning product and technical inputs into grouped frontend tasks such as `Location`, `Billing`, `User Management`, or `Device Outbound`, then writing the result into either:

- a spreadsheet-shaped assessment
- a Markdown `.md` assessment document

It is not for implementing the UI or writing code.

The default assessment template for this skill is the simplified Patricia format with only 4 input columns:

- `Task`
- `Mandays`
- `Story`
- `Notes`

## Trigger phrases

Use this skill when the request includes ideas like:

- "buat tech assessment frontend"
- "breakdown task frontend"
- "turunin BRD jadi task FE"
- "isi sheet assessment frontend"
- "analisa hasil project analyst jadi task frontend"
- "analisa solutioning jadi task frontend"
- "breakdown figma atau flow jadi task frontend"

## Inputs

Minimum useful input:

- one requirement source such as BRD, PRD, analyst output, spreadsheet, Figma, or flow image

Optional input:

- Google Sheets URL and target tab
- Excel file path
- Markdown output path
- Figma URL
- image or screenshot paths
- expected modules or drop name
- team-specific estimation heuristics

## Output modes

This skill supports two output modes:

1. `Spreadsheet mode`
   Use this when the user wants the breakdown written into Google Sheets or Excel, or when the user points to a target tab or workbook.
2. `Markdown mode`
   Use this when the user wants the breakdown as `.md`, `markdown`, a doc-style task list, or when no spreadsheet target is provided and a file artifact is preferred.

If the user does not specify the output mode:

- prefer `Spreadsheet mode` when a spreadsheet URL, workbook, tab name, or existing assessment sheet is provided
- otherwise prefer `Markdown mode`

## Source priority

When multiple sources exist, use this order unless the user says otherwise:

1. `project_analyst` outputs or project-analysis spreadsheets for the baseline story list, scope framing, and flow coverage
2. `solutioning_analyst` documents for API integration tasks, validation, error handling, and dependencies
3. BRD, PRD, PDF, or other requirement docs for business rules and module boundaries
4. Figma files, screenshots, or flow images for UI surfaces, modal splits, state coverage, and hidden FE work

Read [references/source-priority.md](references/source-priority.md) when sources conflict or only partially overlap.

## Workflow

1. Inspect the provided sources and identify the frontend-relevant modules or stories.
2. Ignore backend, infra, QA, or mobile-only scope unless the user explicitly asks for cross-functional tasks.
3. Build a grouped module list first, such as `Location`, `Billing`, `Revenue`, `Device Outbound`, or `User Management`.
4. For each module, derive granular FE tasks using [references/task-breakdown-rules.md](references/task-breakdown-rules.md).
5. Split UI work from API integration work whenever both are present.
6. Add `Notes` only when they materially help, such as BR references, API dependency notes, assumptions, reasons for estimation, role constraints, or missing-contract warnings.
7. Fill `Mandays` with coarse frontend estimates.
8. Decide the output mode first:
   - use `Spreadsheet mode` for Google Sheets or Excel targets
   - use `Markdown mode` for `.md` output
9. In `Spreadsheet mode`, inspect the target tab and at least one nearby reference tab so the output mirrors the live sheet layout instead of assuming a generic template.
10. In `Spreadsheet mode`, before filling multiple rows, identify one correctly formatted template row in the target tab and preserve its cell formatting, borders, alignment, and wrap behavior for every written row.
11. In `Spreadsheet mode`, identify the true last used row in the target tab by checking the lowest visible row that still contains content in the active assessment block. Do not assume the last row from a partial read if lower rows may already be filled.
12. In `Spreadsheet mode`, write new tasks only below that true last used row unless the user explicitly asked to overwrite an existing block.
13. In `Spreadsheet mode`, for Google Sheets, copy the format from a valid reference row or block into the destination rows first, then write cell values into that already-formatted range. Do not write value-only rows into fresh blank rows when the sheet relies on borders or wrap styling.
14. In `Spreadsheet mode`, after writing, re-read the rows immediately above and below the inserted block to confirm nothing existing was overwritten and the new block kept the same borders and visual treatment.
15. In `Spreadsheet mode`, when the target is the simplified Patricia template, write only into `Task`, `Mandays`, `Story`, and `Notes` by following [references/output-shape.md](references/output-shape.md).
16. In `Markdown mode`, render the same grouped FE breakdown into a Markdown document with a clear title, short source/context note, and one row per task in either a Markdown table or concise task list.
17. In `Markdown mode`, keep the same logical fields as the spreadsheet output:
   - `Task`
   - `Mandays`
   - `Story`
   - `Notes`
18. Re-read the written output and confirm the story labels, task ordering, notes placement, estimates, and final shape are present.

## Output rules

- The output target may be either a spreadsheet tab or a Markdown file.
- If the user asks for `.md`, `markdown`, or a document output, produce a Markdown file instead of a sheet update.
- If no spreadsheet target is provided, produce a Markdown table or list that mirrors the same grouped structure.
- The output must follow the live target sheet shape, not a fallback template from another workbook.
- When the target resembles the simplified Patricia template, use only these columns:
  - `Task`
  - `Mandays`
  - `Story`
  - `Notes`
- Write one FE task per row going downward.
- Repeat the story label on every row that belongs to that story. Do not rely on merged cells for story grouping.
- Preserve the existing row format from the sheet template. New task rows must keep the same borders, alignment, font treatment, and wrap settings as the valid example rows above them.
- Determine the append position from the actual last populated row in the target block, not from the last row in a limited read window.
- When appending rows in Google Sheets, treat formatting as a separate required step:
  - first copy format from a valid example row or block into the target rows
  - then write values into those rows
  - then verify the borders still exist after the write
- If an incorrect write already happened in the current turn, repair the sheet before stopping by moving or rewriting the content into the correct rows and restoring the expected formatting.
- If the user provides a finished tab such as `Drop 5.1` as the example source, only borrow the content pattern from it:
  - `Task`
  - `Mandays`
  - `Story`
  - optional contextual explanation in `Notes`
- In `Markdown mode`, prefer one of these shapes unless the user asked otherwise:
  - a Markdown table with columns `Task`, `Mandays`, `Story`, and `Notes`
  - a grouped section-per-story layout with flat task bullets that still include mandays and notes
- If writing Markdown to disk, save it as a `.md` file in the workspace and use a filename derived from the feature or module name.
- Ignore columns such as ticket ids, priority, dates, PIC, testing status, or other planning metadata unless the user explicitly asks to fill them.
- Use FE-first task names such as:
  - `[FE] Slicing Location Page`
  - `[FE] Integrasi API Get List Location`
  - `[FE] Slicing Modal Create Location`
  - `[FE] Integrasi API Create Location`
- Keep task names action-oriented and frontend-specific.
- Do not collapse one module into a single summary row if the UI clearly contains multiple surfaces or operations.
- Keep `Story` values stable per functional area. Example: if a block belongs to `Onboarding`, each row for that block should still say `Onboarding` in the `Story` column.

## Reading different sources

Use [references/input-types.md](references/input-types.md) to decide how to read:

- Google Sheets or Excel from manual assessments or `project_analyst`
- Markdown technical docs from `solutioning_analyst`
- PDF or text requirement docs
- Figma files
- flow screenshots or journey images

## Validation

Before stopping:

- confirm every task row has a visible story label
- confirm the written block mirrors the target sheet's simple 4-column pattern
- confirm each task is frontend-specific
- confirm UI slicing and API integration are split when both exist
- confirm `Mandays` is populated with coarse estimates
- confirm notes only contain helpful references or dependencies
- in `Spreadsheet mode`, confirm the append started below the actual last existing row
- in `Spreadsheet mode`, confirm no pre-existing filled rows were overwritten
- in `Spreadsheet mode`, confirm every written task row keeps the same format and border treatment as the target template row
- in `Spreadsheet mode`, confirm the final sheet shape follows the downward row pattern in the reference file
- in `Markdown mode`, confirm the file is valid Markdown, the heading/context is present, and every task row still exposes `Task`, `Mandays`, `Story`, and `Notes`

## Boundaries

- Do not invent backend endpoints.
- Do not turn this into acceptance-criteria output.
- Do not produce design-system refactors or implementation code.
- When the requirement is unclear, make the smallest safe FE assumption and record it in `Notes`.
- Do not add empty-note filler text. Leave `Notes` blank when there is nothing useful to explain.
