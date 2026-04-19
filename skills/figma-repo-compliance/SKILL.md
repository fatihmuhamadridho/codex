---
name: figma-repo-compliance
description: Compliance workflow for implementing code from Figma into an existing repository. Use when Codex must translate a Figma design into repo code while respecting existing components, choosing the correct feature or page target, avoiding unnecessary native HTML, and stopping for screenshots when the Figma context is unclear.
---

# Figma Repo Compliance

Use this skill when the user wants code built from Figma and the result must comply with the repository's existing components, structure, and architecture rules.

This skill is a gatekeeper and orchestrator. It does not replace Figma MCP skills or repo architecture skills. It decides how to apply them safely.

## Required Workflow

1. Get a Figma target that can be verified.
2. If the link, node, or frame is unclear, stop and ask for a screenshot or clearer target.
3. Decide whether the design is a new feature or a change to an existing one.
4. Inspect the repository for existing components, patterns, and feature ownership before building.
5. Reuse existing repo components first.
6. Use `$fdd` to decide feature placement and page ownership.
7. Use `$atomic-design` to decide component extraction and UI boundaries.
8. Use `$clean-architecture` if the work touches data flow, hooks, or use-case placement.
9. Use `$tdd` only when the user explicitly asks for testing work.
10. Validate the implementation against both Figma fidelity and repo compliance before finishing.

Read [references/workflow.md](references/workflow.md) for the step-by-step decision flow.

Read [references/checklist.md](references/checklist.md) before finalizing work.

Read [references/red-flags.md](references/red-flags.md) when reviewing an implementation that feels off.

## Core Rules

- Never implement from a vague or misread Figma target.
- If Figma access is incomplete or unreliable, ask for a screenshot instead of guessing.
- Do not overwrite or reshape an existing page unless the design actually targets that page.
- Do not assume a design is an update to an existing feature when it is clearly a new feature.
- Reuse repo components before reaching for native HTML.
- Native HTML is a fallback, not the default.
- Keep new code inside the correct feature or shared boundary based on repo rules.

## Native HTML Policy

Default rule:
- do not use native tags like `div`, `button`, `input`, `img`, or similar as the first implementation choice when the repo already has an equivalent abstraction or composition pattern

Allowed only when all of these are true:
- there is no existing repo abstraction that fits
- introducing the native tag keeps the implementation minimal
- the usage does not bypass an established design-system or component-library rule

If native HTML is used, keep it narrow and intentional rather than building the whole screen out of primitives.

## What This Skill Prevents

Use this skill to avoid failures like:
- building the wrong page from the Figma target
- modifying an unrelated existing feature
- implementing a new screen as one giant page component
- ignoring reusable repo components that already exist
- continuing from an unreadable Figma link instead of asking for a screenshot
- using large amounts of native HTML where repo components should have been reused

## Coordination

Use this skill before or alongside:
- `figma:figma-implement-design` for extracting design context from Figma
- `$fdd` for feature ownership and route boundaries
- `$atomic-design` for component composition decisions
- `$clean-architecture` for dependency and layering decisions

Do not duplicate the full contents of those skills. Use them to make the specific decision they own.

## Review Checklist

Before finishing, verify:
- the Figma target was correctly identified
- the implementation landed in the correct feature or page
- repo components were reused where appropriate
- no unnecessary native HTML dominates the UI
- route-level and feature-level responsibilities are still correct
- the result matches the intended Figma screen rather than a guessed variant

## Trigger Examples

Use this skill for prompts like:
- "Use $figma-repo-compliance to implement this Figma screen in the repo."
- "Bikinin halaman ini dari Figma tapi harus ikut komponen repo yang sudah ada."
- "Review kenapa hasil dari Figma masih banyak pakai div."
- "Pastikan implementasi dari Figma tidak salah feature dan tidak melanggar struktur repo."
