# Output Shape

Use this as the formatting source of truth for frontend assessment output.

The target shape mirrors the logical pattern of the `Drop 2-fix` sheet:

- a review marker row
- a story header row
- a list of FE tasks under that story
- blank spacer rows when useful for readability

## Active columns

Use these columns in order:

- `Task`
- `Actual Mandays`
- `Mandays`
- `Story`
- `Notes`

Other columns may exist in the user sheet. Leave unrelated columns untouched unless the user asks to normalize the whole tab.

## Group structure

For each module:

1. Add a row with `Task = NEED TO BE REVIEW`
2. Add a header row with the module name in `Story`
3. Add FE task rows below it

Example:

| Task                                 | Actual Mandays | Mandays | Story    | Notes                       |
| ------------------------------------ | -------------- | ------- | -------- | --------------------------- |
| NEED TO BE REVIEW                    |                |         |          |                             |
|                                      |                |         | Location |                             |
| [FE] Slicing Location Page           |                | 1       |          | Perhatikan BR-26 s.d. BR-30 |
| [FE] Integrasi API Get List Location |                | 1       |          |                             |
| [FE] Slicing Modal Create Location   |                | 0.5     |          |                             |
| [FE] Integrasi API Create Location   |                | 1       |          |                             |

## Naming rules

- Prefix frontend tasks with `[FE]`
- Prefer verbs such as `Slicing`, `Integrasi API`, `Setup`, `Handle`, `Implement`, `Add`, `Guard`
- Keep each row to one concrete FE unit of work
- Use Indonesian naming if the surrounding spreadsheet uses Indonesian

## Estimation rules

- Fill `Mandays` with coarse FE estimates
- Leave `Actual Mandays` empty by default
- If the user supplies actuals, write them only in `Actual Mandays`

## Notes rules

Use `Notes` sparingly for:

- BR references
- role or permission constraints
- missing API contract warnings
- dependencies on analyst output or Figma flow

Do not repeat obvious task text in `Notes`.
