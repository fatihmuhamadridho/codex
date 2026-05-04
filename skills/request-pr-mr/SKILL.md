---
name: request-pr-mr
description: Use for preparing a pull request or merge request from branch changes with a diff-based title and summary.
---

# Request PR or MR

Use this skill when the task is to open a GitHub pull request or GitLab merge request from branch changes.

This skill covers:
- choosing the source branch
- always asking for the target branch
- verifying the source branch has been pushed
- deriving title and description from the actual diff
- choosing the correct provider flow
- attaching assignee and only existing labels when supported
- creating the request when the prerequisites are satisfied

This skill does not replace `$commit-push`. Use `$commit-push` first if the branch has not been committed or pushed yet.

Read [references/preparation.md](references/preparation.md) for branch and diff preparation.

Read [references/content-rules.md](references/content-rules.md) for title and description rules.

Read [references/provider-rules.md](references/provider-rules.md) for GitHub and GitLab provider behavior.

Read [references/metadata-rules.md](references/metadata-rules.md) for assignee and label handling.

## Core Workflow

1. Detect the current branch and use it as the default source branch.
2. Ask the user which target branch should receive the PR or MR.
3. Verify the source branch exists and has been pushed.
4. Detect the hosting provider from the remote.
5. Compare the source branch against the chosen target branch using the actual diff.
6. Draft the request title and description from the diff summary.
7. Stop if the diff is empty.
8. Create the request with the correct provider CLI when available.
9. Attach assignee and only existing labels when supported.
10. Report the created request or the precise fallback if provider tooling is unavailable.

## Default Rules

- Always ask for the target branch.
- Do not create a request until the diff has been reviewed.
- Do not create a request if the source branch has not been pushed.
- Do not create a request if there is nothing to merge.
- Use the diff, not only the latest commit message, as the source of truth.
- Attach only labels that already exist.
- Do not create new labels as part of the request flow.

## Boundaries

Use this skill for questions like:
- "buat PR dari branch ini"
- "request MR ke development"
- "bikinin pull request dengan title dan description yang sesuai diff"
- "open merge request dari branch ini ke target branch tertentu"

Do not use this skill for:
- local commit and push work without opening a PR or MR
- deploy tagging or version bumping
- installing provider CLIs

## Review Checklist

Before finishing, verify:
- the target branch was explicitly confirmed
- the source branch was already pushed
- the title matches the net change in the diff
- the description reflects real file changes
- provider selection matched the active remote
- assignee and labels follow platform support and repo rules

## Trigger Examples

Use this skill for prompts like:
- "Use $request-pr-mr to open a PR from this branch."
- "Bikinin MR ke branch development."
- "Buat pull request yang title dan description-nya sesuai diff."
- "Request merge dari branch ini ke target branch yang gua tentuin."
