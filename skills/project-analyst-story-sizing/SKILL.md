---
name: project-analyst-story-sizing
description: Generate acceptance-criteria story sizing sheets from product requirements using the project_analyst subagent and write the result into a Google Sheet tab.
---

# Project Analyst Story Sizing

Use this skill when the user wants a feature or requirement turned into a spreadsheet-style acceptance-criteria sheet with detailed flow coverage.

This skill is for spreadsheet-style sizing output, not for general feature analysis. For normal product analysis without sizing-sheet output, use `project_analyst` directly without this skill.

## Trigger phrases

Use this skill when the request includes ideas like:

- "buat story sizing"
- "isi sheet seperti Example"
- "ubah requirement jadi sizing sheet"
- "bikin estimation sheet"
- "tulis ke Google Sheet"

## Inputs

Minimum useful input:

- feature request, requirement, or user story text

Optional input:

- Google Sheets URL
- target tab name
- whether to overwrite an existing tab or write into a new one
- team-specific sizing heuristics if they exist

## Workflow

1. Read the requirement and identify the primary actor, user goal, expected outcome, and visible interaction steps.
2. Break the requirement into detailed positive flow and negative flow slices before writing any rows.
3. Spawn `project_analyst` to produce the analysis in story sizing mode.
4. Convert the analysis into the `Example` layout described in [references/example-layout.md](references/example-layout.md).
5. Write the result directly to the target Google Sheet tab.
6. Re-read the written range and verify the structure and numbering.

## Output rules

- Mirror the acceptance-criteria layout described in the reference file.
- Keep the opening feature statement near the top of the sheet.
- Use numbered acceptance-criteria rows.
- Write positive flow and negative flow as separate rows.
- Keep the flow detailed: break a broad user journey into multiple observable rows when the user sees different states, actions, validations, or results.
- Preserve only these major fields:
  - `No`
  - `Acceptance Criteria`
  - `Given`
  - `When`
  - `Then`
- Do not add technical or estimation columns such as `Surrounding`, `Technical Flow`, `UI Slicing`, `Task`, `Mandays`, `Total`, or `Size`.
- If information is missing, keep the acceptance criteria conservative and make the smallest safe assumption explicit in the AC wording.
- Order rows with positive flow first, then negative flow and validation/error flow after that.
- Cover all visible states reasonably implied by the requirement, including empty state, validation state, error state, blocked action, or failed action when relevant.

## Google Sheet write policy

- Prefer writing directly to the user-provided spreadsheet.
- If the target tab already exists and the user clearly wants that tab updated, clear and rewrite that tab.
- If the target tab does not exist, create a new tab with the requested name.
- Do not overwrite unrelated tabs.

## Validation

After writing the tab:

- confirm the tab name is correct
- confirm numbered acceptance rows are present
- confirm the feature statement is present
- confirm only `Acceptance Criteria`, `Given`, `When`, and `Then` are used as AC fields
- confirm positive flow rows are present
- confirm negative or validation flow rows are present when the feature implies them
- confirm the rows are detailed enough that separate user-visible steps are not collapsed into one broad AC

If the write result does not match the expected layout, fix the sheet before stopping.
