# Output Shape

Use the live target tab as the formatting source of truth.

Do not assume a generic assessment template if the spreadsheet already has an established pattern. Always inspect:

- the target tab
- at least one nearby finished tab used by the same team

## Simplified Patricia Template

When the target sheet matches the simplified Patricia template, write the output in these columns only:

- `Task`
- `Mandays`
- `Story`
- `Notes`

Other columns may exist in other tabs. Ignore them unless the user explicitly asks to fill them.

## Row Structure

Write the assessment as a simple downward list:

1. One FE task per row.
2. Put the coarse estimate in `Mandays`.
3. Fill `Story` on every row, even when several consecutive rows belong to the same story.
4. Fill `Notes` only when there is useful additional context.

Do not use merged cells for grouping in this simplified template.
Do not write plain values into unformatted rows and assume the sheet will look correct. Reuse the existing formatted task row style from the target tab.

## Writing Rules

- Mirror the target tab structure before borrowing patterns from nearby tabs.
- Before writing a block, inspect one valid task row from the target tab and treat it as the formatting source of truth.
- If you need to extend the block downward, copy the template row format first or write in a way that preserves the same borders, alignment, wrap, and fonts on each new row.
- If the user gives a finished tab such as `Drop 5.1`, use it only as a content example for task granularity and estimation style.
- From finished tabs, only carry forward the relevant content:
  - FE task wording
  - coarse mandays
  - story name
- Do not copy planning metadata such as ticket ids, priority, dates, internal testing, or PIC into the simplified template.
- Keep notes short and practical, for example:
  - dependency on API contract
  - assumption about role access
  - reason a task is split
  - rule or constraint from the requirement

## Example

Simplified Patricia-style output should look like this structurally:

| Task | Mandays | Story | Notes |
| --- | --- | --- | --- |
| [FE] Slicing Onboarding landing page | 0.5 | Onboarding | Includes empty state and CTA state |
| [FE] Integrasi API submit onboarding form | 1 | Onboarding | Wait for final payload contract |
| [FE] Slicing modal confirm onboarding action | 0.25 | Onboarding |  |
| [FE] Slicing user preference page | 0.5 | Preferences | Role visibility follows BRD section 4 |

## Validation

Before stopping, confirm:

- the sheet no longer contains placeholder story labels from the template
- every task row has a populated `Story` value
- repeated story labels are written explicitly instead of implied by merges
- `Mandays` is populated on each task row
- `Notes` is only used for real context, not filler
- each written row keeps the same border and formatting treatment as the target template
- the written block reads cleanly in the actual sheet UI, not only in raw cell output
