# Input Types

Use this file to decide how to read different requirement sources before producing FE tasks.

## Google Sheets and Excel

Use these as structured sources when they already contain:

- grouped stories or modules
- acceptance criteria
- flow steps
- notes from manual assessment
- output from `project_analyst`

Reading strategy:

- identify module names first
- extract rows that imply UI surfaces, actions, validation, or role-based behavior
- convert acceptance-criteria wording into FE implementation tasks
- do not keep the source in acceptance-criteria format

## Project Analyst outputs

Expect:

- feature names
- flow summaries
- acceptance criteria summaries
- backlog item summaries
- dependencies or risks

Use them mainly to:

- decide the module breakdown
- capture positive and negative flow coverage
- find missing UI states or branching paths

## Solutioning Analyst docs

Expect:

- API or integration flow
- request and response shape
- validation rules
- error scenarios
- dependency mapping

Use them mainly to:

- create API integration tasks
- add FE validation work
- add error-state or retry-state handling
- mark dependencies when contracts are still incomplete

## BRD, PRD, or PDF docs

Expect:

- module names
- business rules
- CRUD scope
- role access
- configuration fields

Use them mainly to:

- confirm module boundaries
- derive implied FE forms and settings areas
- capture notes such as BR identifiers

## Figma and image flows

Expect:

- screens
- component states
- modal variants
- user-flow transitions
- role-specific visibility

Use them mainly to:

- detect missing FE surfaces not visible in text docs
- split one module into more realistic UI work units
- identify confirmations, wizards, OTP steps, scanners, drawers, tabs, or empty states

If the visual source is ambiguous, keep the FE task conservative and mention the uncertainty in `Notes`.
