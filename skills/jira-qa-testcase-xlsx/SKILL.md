---
name: jira-qa-testcase-xlsx
description: Generate QA test-case workbooks in XLSX format from a Jira story using an internal template. Use when Codex needs to analyze a Jira story URL, infer positive and negative test scenarios, and write a new test-case file into Downloads that matches the provided Excel example.
---

# Jira QA Testcase XLSX

Use this skill when the user wants a Jira story turned into a QA test-case workbook.

This skill is for spreadsheet output, not for general Jira summarization. Read the Jira story with Atlassian Rovo, infer the likely scenarios from the story content, then generate a new XLSX file with the bundled template and script.

## Inputs

Minimum input:

- one Jira story URL

Optional input:

- preferred output filename
- preferred language, if the user wants something other than the default mixed language style

## Workflow

1. Use Atlassian Rovo search and fetch tools to read the Jira story.
2. Analyze only the provided story by default. Do not include linked issues or comments unless the user explicitly asks for them.
3. Extract:
   - Jira key and URL
   - story title
   - roles mentioned in the story
   - platform or channel if it is stated
   - visible user flows, validations, empty states, and failure cases
4. Convert the story into test cases grouped by role.
5. Cover the main user-visible scenarios:
   - default page or initial state
   - positive flow
   - negative or validation flow
   - empty or no-result state when implied
   - permission or role-specific behavior when implied
   - server or network failure only when the story text reasonably implies it
6. Build a JSON payload that matches the script schema in [references/template-layout.md](references/template-layout.md).
7. Run `scripts/generate_testcase_workbook.py` with:
   - `--input-json`
   - optional `--output`
8. Verify the generated file exists in `~/Downloads` and that the workbook contains:
   - `Summary`
   - one sheet per role
   - `Legend`

## Output Rules

- Default output language is mixed, matching the style of the provided workbook.
- Split sheets by role when the story mentions more than one role.
- Use conservative defaults when the story is incomplete:
  - `PLATFORM`: `Web CMS`
  - `TYPE`: `Functional`
  - `COMPLEXITY`: `Medium`
- Use `BEHAVIOUR` as `Positive` or `Negative`.
- Leave execution-only columns blank:
  - `ACTUAL RESULT`
  - `REMARKS`
  - `DATE`
  - `PIC TESTER`
  - `EVIDENCE SIT`
  - `Evidence Internal Test`
  - `Automate/Manual`
- Keep `LINK STORY`, `FEATURE / SUITE`, and `ROLE USER` consistent across all rows in the same role sheet.
- Order rows with positive flow first, then negative, validation, no-result, and failure rows.

## Script Usage

Use the bundled script:

```bash
python3 scripts/generate_testcase_workbook.py \
  --input-json /tmp/story-testcases.json \
  --output ~/Downloads/SPPAT-1724_test-cases.xlsx
```

The script copies `assets/template.xlsx`, rewrites the role sheets, refreshes `Summary`, keeps `Legend`, and saves a new workbook in Downloads.

## Resources

- `assets/template.xlsx`: the formatting source of truth for the workbook
- `references/template-layout.md`: JSON input schema and column mapping
- `scripts/generate_testcase_workbook.py`: deterministic XLSX generator with no external Python dependencies
