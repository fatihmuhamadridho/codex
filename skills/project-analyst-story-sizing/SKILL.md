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
4. Convert the analysis into the exact `Example` sheet shape described in [references/example-layout.md](references/example-layout.md).
5. If the target tab is created by duplicating `Example`, clear the old example content before writing new rows.
6. Write only into the active acceptance-criteria area and leave the non-AC template sections empty.
7. Re-read the written range and verify the structure, numbering, and empty template sections.

## Output rules

- Mirror the acceptance-criteria layout described in the reference file.
- Preserve the overall sheet shape, merges, borders, and visual structure of the `Example` tab.
- Keep the opening feature statement near the top of the sheet.
- Use numbered acceptance-criteria rows.
- Write positive flow and negative flow as separate rows.
- Keep the flow detailed: break a broad user journey into multiple observable rows when the user sees different states, actions, validations, or results.
- The only active content columns in the acceptance-criteria table are:
  - `No`
  - `Given`
  - `When`
  - `Then`
- `Acceptance Criteria:` is a group header above `Given`, `When`, and `Then`. It is not a separate row field and must not be used as its own content column.
- Do not add duplicate AC columns such as a second `When` or `Then`.
- Do not populate non-AC template sections such as `New Technology`, `Surrounding`, `Technical Flow`, `UI Slicing`, `Task`, `Mandays`, `Total`, or `Size`.
- If those sections exist in the duplicated template, preserve the structure but leave their contents empty.
- If information is missing, keep the acceptance criteria conservative and make the smallest safe assumption explicit in the AC wording.
- Order rows with positive flow first, then negative flow and validation/error flow after that.
- Cover all visible states reasonably implied by the requirement, including empty state, validation state, error state, blocked action, or failed action when relevant.

## Google Sheet write policy

- Prefer writing directly to the user-provided spreadsheet.
- If the target tab already exists and the user clearly wants that tab updated, clear and rewrite that tab.
- If the target tab does not exist, create a new tab with the requested name.
- If the tab is created from `Example`, keep the overall layout identical to `Example` while clearing example-specific text and leaving non-AC sections blank.
- Do not overwrite unrelated tabs.

## Validation

After writing the tab:

- confirm the tab name is correct
- confirm numbered acceptance rows are present
- confirm the feature statement is present
- confirm the active AC columns are only `No`, `Given`, `When`, and `Then`
- confirm `Acceptance Criteria:` appears only as the group header above `Given`, `When`, and `Then`
- confirm there is no duplicate `When` or `Then` header
- confirm positive flow rows are present
- confirm negative or validation flow rows are present when the feature implies them
- confirm non-AC sections such as `UI Slicing` and `Task` are empty
- confirm the last AC row still belongs to the same bordered table as the rows above it
- confirm the rows are detailed enough that separate user-visible steps are not collapsed into one broad AC

If the write result does not match the expected layout, fix the sheet before stopping.
