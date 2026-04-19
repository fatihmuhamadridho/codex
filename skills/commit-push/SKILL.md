---
name: commit-push
description: Guide for committing staged Git changes and pushing the current branch with a constrained Conventional Commit prefix. Use when Codex should prepare a commit message, create a commit, and push the active branch while limiting allowed commit types to feat, fix, hotfix, test, and refactor.
---

# Commit Push

Use this skill when the user wants Codex to commit local changes and push the current branch.

This skill only covers commit and push. It does not stage files automatically and it does not open a PR or MR.

## Workflow

1. Confirm the current directory is inside a Git repository.
2. Inspect the active branch and working tree.
3. Verify there are staged changes.
4. Review only the staged diff to infer the commit intent.
5. Write a commit message in the required subject-and-body format.
6. Create the commit.
7. Push the active branch to its remote.
8. If the branch has no upstream, push with upstream tracking.

Stop and tell the user if there are no staged changes. Do not run `git add`, `git add -u`, or `git add -A` as part of this skill unless the user explicitly asks for staging help in a separate instruction.

## Commit Format

Every commit created with this skill must include:

1. A subject line
2. A description body after one blank line

The subject format is:

```text
type: summary
```

The full commit shape is:

```text
type: summary

description paragraph
```

Rules:
- `type` must be lowercase.
- Allowed types are only `feat`, `fix`, `hotfix`, `test`, `refactor`.
- Use exactly one colon followed by one space.
- Do not add scope, such as `feat(api): ...`.
- Keep `summary` short, specific, and imperative.
- Do not end the summary with a period.
- Always add a description body.
- The description should be a short paragraph, not bullets.
- Keep the description grounded in the staged diff and explain what changed and why it matters.
- Do not repeat the subject verbatim in the description.
- Do not leave the description blank even for small commits.

## Allowed Types

Use these meanings:

- `feat`: adds user-facing or developer-facing functionality
- `fix`: fixes a non-urgent bug or regression
- `hotfix`: fixes a production issue or urgent breakage
- `test`: adds or updates tests without changing product behavior
- `refactor`: restructures code without intended behavior changes

If the requested change does not fit one of these categories, say so and ask the user whether they want the closest allowed type used.

## Examples

Valid examples:

```text
feat: add workspace switcher to header

Adds the header workspace selector and updates the switch flow so users can change active workspaces without leaving the current page.

fix: handle empty response in sync job

Guards the sync parser against empty upstream payloads so the job fails safely instead of raising an unhandled exception.

hotfix: prevent checkout crash on null cart

Adds a null check before checkout initialization to stop the production crash path when cart state is missing.

test: cover token refresh retry flow

Adds regression coverage for the retry path after token refresh so auth failures are caught before release.

refactor: split billing service validation logic

Separates billing validation from request orchestration so the rules are easier to reuse and maintain.
```

Invalid examples:

```text
feat(ui): add workspace switcher
docs: update readme
fix add retry for sync job
Refactor: clean service layer
fix: handle empty response
```

That last example is invalid because it has no description body.

## Push Rules

- Push the active branch only.
- Prefer the existing upstream when it is configured.
- If no upstream exists, use a push command that sets upstream for the current branch.
- Do not force-push unless the user explicitly asks for it.

## Safety Checks

Before committing, verify:
- Git repository is available
- Active branch is not detached
- There are staged changes
- The staged diff is coherent enough to summarize in one commit
- The staged diff is coherent enough to justify one subject and one description body

If the staged changes appear too broad for one commit, warn the user before committing.

## Trigger Examples

Use this skill for prompts like:
- "Use $commit-push to commit and push these staged changes."
- "Bantu commit dan push branch ini dengan type fix."
- "Buat commit message yang valid lalu push."
- "Commit perubahan staged ini pakai type refactor."
