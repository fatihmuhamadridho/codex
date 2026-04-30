---
name: repo-conventions
description: Repo-wide coding conventions and completion checks for work that must follow local repository patterns without relying on one architecture skill alone. Use when Codex should apply existing repo conventions, avoid broad anti-patterns, and verify that a change is actually done before stopping.
---

# Repo Conventions

Use this skill when the task needs repo-wide rules, coding conventions, or completion checks that are not owned by a more specific skill.

This skill is the general rulebook. It does not replace `$feature-driven-development`, `$atomic-design`, `$clean-architecture`, or `$commit-push`. It complements them.

Read [references/repo-rules.md](references/repo-rules.md) for the repo-wide implementation rules.

Read [references/done-checklist.md](references/done-checklist.md) before considering work complete.

Read [references/anti-patterns.md](references/anti-patterns.md) when a change feels inconsistent with the repo.

## Core Workflow

1. Identify whether the task needs repo-wide guidance rather than a narrower architecture skill.
2. Inspect the nearest existing pattern before introducing anything new.
3. Keep the implementation as small and local as the task allows.
4. Apply the repo's naming, structure, and composition habits consistently.
5. Use the more specific local skill if the main question becomes about feature slicing, component layering, dependency direction, or Git workflow.
6. Run the completion checklist before treating the task as done.

## Default Rules

- Follow existing patterns before creating a new variation.
- Prefer the repo's current conventions over personal preference.
- Keep changes scoped to the task instead of opportunistically reshaping unrelated areas.
- Reuse existing abstractions when they fit.
- If an abstraction does not fit, extend carefully before creating a competing pattern.
- Leave the surrounding code more coherent, not more fragmented.

## Boundaries

Use this skill for questions like:
- Is this change aligned with the repo's existing pattern?
- Is this implementation actually complete?
- Did this task introduce a repo-wide smell?
- Is the change too broad for the requested scope?

Do not use this skill as a substitute for:
- `$feature-driven-development` when the main issue is feature ownership or page boundaries
- `$atomic-design` when the main issue is UI composition boundaries
- `$clean-architecture` when the main issue is dependency direction or layer placement
- `$commit-push` when the main issue is Git workflow

This skill does not define testing workflow. If testing becomes the core concern, switch to `$test-driven-development`.

## Review Checklist

Before finishing, verify:
- the implementation follows an existing repo pattern where one exists
- the change scope still matches the user's request
- new abstractions were added only when justified
- there are no obvious repo-wide smells left behind
- the task is actually complete, not just partially wired

## Trigger Examples

Use this skill for prompts like:
- "Use $repo-conventions to review whether this change fits the repo."
- "Pastikan hasil kerja ini sudah sesuai convention repo."
- "Cek apakah implementasi ini sudah benar-benar selesai."
- "Jangan bikin variasi baru kalau repo sudah punya pola yang dipakai."
