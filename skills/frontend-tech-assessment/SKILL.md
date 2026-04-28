---
name: frontend-tech-assessment
description: Break down frontend implementation tasks from BRDs, spreadsheets, analyst outputs, Figma, and flow images into grouped FE assessment sheets with coarse manday estimates.
---

# Frontend Tech Assessment

Use this skill when the user wants a frontend tech assessment, frontend task breakdown, or FE implementation worksheet derived from one or more requirement sources.

This skill is for turning product and technical inputs into grouped frontend tasks such as `Location`, `Billing`, `User Management`, or `Device Outbound`, then writing the result into a spreadsheet-shaped assessment. It is not for implementing the UI or writing code.

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
- Figma URL
- image or screenshot paths
- expected modules or drop name
- team-specific estimation heuristics

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
8. Before writing, inspect the target tab and at least one nearby reference tab so the output mirrors the live sheet layout instead of assuming a generic template.
9. Before filling multiple rows, identify one correctly formatted template row in the target tab and preserve its cell formatting, borders, alignment, and wrap behavior for every written row.
10. When the target is the simplified Patricia template, write only into `Task`, `Mandays`, `Story`, and `Notes` by following [references/output-shape.md](references/output-shape.md).
11. Re-read the written range and confirm the story labels, task ordering, notes placement, estimates, and row formatting are present.

## Output rules

- The default output target is a Google Sheet tab.
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
- If the user provides a finished tab such as `Drop 5.1` as the example source, only borrow the content pattern from it:
  - `Task`
  - `Mandays`
  - `Story`
  - optional contextual explanation in `Notes`
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
- confirm every written task row keeps the same format and border treatment as the target template row
- confirm the final sheet shape follows the downward row pattern in the reference file

## Boundaries

- Do not invent backend endpoints.
- Do not turn this into acceptance-criteria output.
- Do not produce design-system refactors or implementation code.
- When the requirement is unclear, make the smallest safe FE assumption and record it in `Notes`.
- Do not add empty-note filler text. Leave `Notes` blank when there is nothing useful to explain.
