# Example Story Sizing Layout

This reference captures the target acceptance-criteria structure used for story sizing sheets.

Use it as the formatting source of truth when creating or rewriting story sizing tabs.

This layout is AC-only, but the content must still be flow-complete.

## High-level shape

- Row 1 is blank.
- Row 2 contains the feature statement in natural language.
- Row 3 is blank.
- Row 4 contains the main section headers.
- Row 5 contains the subheaders for acceptance criteria columns.
- Rows 6 onward contain numbered acceptance criteria slices.
- Positive flow rows should appear first.
- Negative flow, validation flow, and failure flow rows should appear after the happy path.

## Header structure

Primary headers:

- `No`
- `Acceptance Criteria:`

Subheaders used beneath the acceptance-criteria area:

- `Given`
- `When`
- `Then`

## Content expectations by row

Each numbered row should usually contain:

- `No`: sequential numbering starting from `1`
- `Acceptance Criteria`: actor or state context
- `Given`: optional precondition if needed
- `When`: user/system action
- `Then`: observable system result

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
- Do not add technical or estimation columns.
- Do not collapse the sheet into a one-row summary CSV structure.
- Prefer exact labels above unless the user asks to rename them.
