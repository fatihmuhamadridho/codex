# Example Story Sizing Layout

This reference captures the target acceptance-criteria structure used for story sizing sheets.

Use it as the formatting source of truth when creating or rewriting story sizing tabs.

This layout must visually match the `Example` sheet, but only the acceptance-criteria table is actively populated. The rest of the template remains empty.

## High-level shape

- Row 1 is blank.
- Row 2 contains the feature statement in natural language.
- Row 3 is blank.
- Row 4 contains the main section headers.
- Row 5 contains the subheaders for acceptance criteria columns.
- Rows 6 onward contain numbered acceptance criteria slices.
- Positive flow rows should appear first.
- Negative flow, validation flow, and failure flow rows should appear after the happy path.
- The non-AC sections to the right and below the AC table keep the same shape as `Example`, but their contents must stay empty.

## Header structure

Primary headers:

- `No`
- `Acceptance Criteria:`

Subheaders used beneath the acceptance-criteria area:

- `Given`
- `When`
- `Then`

Active columns:

- `No`
- `Given`
- `When`
- `Then`

`Acceptance Criteria:` is a merged group header above `Given`, `When`, and `Then`. It is not a separate content column.

## Content expectations by row

Each numbered row should usually contain:

- `No`: sequential numbering starting from `1`
- `Given`: optional precondition if needed
- `When`: user/system action
- `Then`: observable system result

Do not create or populate:

- an `Acceptance Criteria` content column
- a second `When` column
- a second `Then` column
- any additional AC subheaders beyond `Given`, `When`, and `Then`

## Flow depth rules

- Do not compress an end-to-end flow into one row if the user sees multiple steps or states.
- Add separate rows for:
  - successful progression through the happy path
  - validation failures
  - blocked actions
  - failed submission or failed processing when reasonably implied
- Use the AC wording itself to distinguish the flow type. Do not add a separate label column.

## Fidelity policy

- Follow the ordering closely.
- Keep blank spacer rows when they help preserve readability.
- Match the overall sheet structure of `Example`, including merges, borders, and visual grouping.
- Do not fill technical or estimation sections such as `New Technology`, `Surrounding`, `Technical Flow`, `UI Slicing`, `Task`, `Mandays`, `Total`, or `Size`.
- Do not collapse the sheet into a one-row summary CSV structure.
- Prefer exact labels above unless the user asks to rename them.
- Ensure the last acceptance-criteria row keeps the same borders as the rest of the AC table and does not visually break from the table.
