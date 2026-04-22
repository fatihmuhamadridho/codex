# Output Shape

Use the live target tab as the formatting source of truth.

Do not assume a generic assessment template if the spreadsheet already has an established pattern. Always inspect:

- the target tab
- at least one nearby finished tab used by the same team

## Patricia FE Tracker Shape

When the target sheet matches the Patricia FE tracker pattern, write the output in these active columns:

- `Story Ticket`
- `Ticket`
- `Task`
- `Hard Mandays`
- `Mandays`
- `Actual Mandays`
- `Story`
- `Priority`
- `Start Date`
- `End Date`
- `Internal Testing`
- `PIC`
- `Notes`

Other columns may exist to the right. Leave them untouched unless the user explicitly asks to fill them.

## Group Structure

For each story or flow group:

1. Leave one blank white spacer row after a story block when the reference tab shows visible breathing room between groups.
2. Add a green separator row after that spacer when the reference tab uses one.
3. Write one FE task per row under the next story block.
4. Merge story-level cells only when the reference tab does so.

For Patricia-like tabs, this usually means:

- merge `Story Ticket` vertically across the story block when the whole block belongs to one story ticket
- keep `Ticket` row-level when each FE task has its own ticket
- merge `Story` vertically across the task rows in the same group
- merge `Internal Testing` vertically across the task rows in the same group
- keep `Priority`, `Start Date`, `End Date`, `PIC`, and `Notes` row-level unless the reference tab clearly merges them

## Writing Rules

- Mirror the nearby finished tab's visual grouping before inventing a new layout.
- In Patricia-like tabs, do not let one story block visually touch the next one.
- The expected transition is: last task row -> one blank white row -> one green separator row -> next story block.
- Prefer one story block per actual FE flow, not one oversized dump block for unrelated screens.
- Keep `Actual Mandays` empty unless the user provides actuals.
- If `Story Ticket` or `Ticket` mappings are unknown, leave them blank rather than inserting misleading placeholders.
- If the reference tab uses green status cells such as `Done`, copy that convention only when it fits the user's requested output.

## Example

Patricia-style output should look like this structurally:

| Story Ticket | Ticket | Task | Hard Mandays | Mandays | Actual Mandays | Story | Priority | Start Date | End Date | Internal Testing | PIC | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |
| SPPAT-XXXX |  | [FE] Slicing Login Page - 0.5 | 0.5 | 0.5 |  | Login + OTP | 1 | ... | ... | ... | ... | ... |
|  |  | [FE] Integrasi Submit Login - 0.5 | 0.5 | 0.5 |  |  | 2 | ... | ... |  | ... | ... |
|  |  | [FE] Slicing OTP Verification Page - 0.5 | 0.5 | 0.5 |  |  | 3 | ... | ... |  | ... | ... |

## Validation

Before stopping, confirm:

- the sheet no longer contains placeholder story labels from the template
- task rows sit under the correct story group
- merged cells match the reference pattern
- `Hard Mandays` and `Mandays` are both filled when both columns exist
- the written block reads cleanly in the actual sheet UI, not only in raw cell output
