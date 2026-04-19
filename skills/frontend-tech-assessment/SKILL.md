---
name: frontend-tech-assessment
description: Break down frontend implementation tasks from BRDs, spreadsheets, analyst outputs, Figma, and flow images into grouped FE assessment sheets with coarse manday estimates.
---

# Frontend Tech Assessment

Use this skill when the user wants a frontend tech assessment, frontend task breakdown, or FE implementation worksheet derived from one or more requirement sources.

This skill is for turning product and technical inputs into grouped frontend tasks such as `Location`, `Billing`, `User Management`, or `Device Outbound`, then writing the result into a spreadsheet-shaped assessment. It is not for implementing the UI or writing code.

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
6. Add task notes only when they materially help, such as BR references, API dependency notes, role constraints, or missing-contract warnings.
7. Fill `Mandays` with coarse frontend estimates. Leave `Actual Mandays` empty unless the user provides actuals.
8. Write the result into the requested Google Sheet tab by following [references/output-shape.md](references/output-shape.md).
9. Re-read the written range and confirm the grouping, story labels, task ordering, and estimates are present.

## Output rules

- The default output target is a Google Sheet tab.
- If no spreadsheet target is provided, produce a Markdown table or list that mirrors the same grouped structure.
- The primary output columns are:
  - `Task`
  - `Actual Mandays`
  - `Mandays`
  - `Story`
  - `Notes`
- Use grouped sections with a review marker row before each module.
- Use FE-first task names such as:
  - `[FE] Slicing Location Page`
  - `[FE] Integrasi API Get List Location`
  - `[FE] Slicing Modal Create Location`
  - `[FE] Integrasi API Create Location`
- Keep task names action-oriented and frontend-specific.
- Do not collapse one module into a single summary row if the UI clearly contains multiple surfaces or operations.

## Reading different sources

Use [references/input-types.md](references/input-types.md) to decide how to read:

- Google Sheets or Excel from manual assessments or `project_analyst`
- Markdown technical docs from `solutioning_analyst`
- PDF or text requirement docs
- Figma files
- flow screenshots or journey images

## Validation

Before stopping:

- confirm every module has a visible story or group label
- confirm each task is frontend-specific
- confirm UI slicing and API integration are split when both exist
- confirm `Mandays` is populated with coarse estimates
- confirm `Actual Mandays` is blank unless actuals were provided
- confirm notes only contain helpful references or dependencies
- confirm the final sheet shape follows the grouped pattern in the reference file

## Boundaries

- Do not invent backend endpoints.
- Do not turn this into acceptance-criteria output.
- Do not produce design-system refactors or implementation code.
- When the requirement is unclear, make the smallest safe FE assumption and record it in `Notes`.
