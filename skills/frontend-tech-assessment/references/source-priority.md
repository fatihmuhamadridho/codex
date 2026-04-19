# Source Priority

Use this file when multiple sources describe the same module with different levels of detail.

## Default precedence

1. `project_analyst` output
2. `solutioning_analyst` output
3. BRD, PRD, PDF, or other requirement docs
4. Figma or image-based flow sources

## How to reconcile

- Treat `project_analyst` as the default source for story names, grouped modules, and broad flow coverage.
- Treat `solutioning_analyst` as the source for API-aware FE work such as integration points, field validation, response handling, retry/error states, and dependency notes.
- Use BRD or PRD to confirm business rules, CRUD scope, limits, role access, and configuration fields.
- Use Figma or image flows to reveal hidden UI surfaces such as modal variants, empty states, tabs, step transitions, or role-based visibility that are not explicit in text docs.

## Conflict rules

- If analyst output expands a module without contradicting the BRD, keep the expanded FE work.
- If BRD and analyst output disagree on scope, stay conservative and note the conflict.
- If Figma shows extra UI not supported by any requirement source, include it only when it looks like required flow support rather than decorative exploration.
- If the API contract is missing, still include the FE task and note the dependency instead of inventing exact request details.

## Missing-source behavior

- If only BRD exists, derive the FE breakdown from business rules and CRUD or flow implications.
- If only Figma or images exist, infer modules from screens and user flows, then mark uncertain items in `Notes`.
- If only analyst docs exist, trust them as the baseline and use any attached spreadsheets or references to refine granularity.
