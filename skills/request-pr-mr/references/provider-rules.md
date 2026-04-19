# Provider Rules

Use this reference to choose the correct request creation flow.

## Provider Detection

Detect the provider from the active remote.

Use:
- GitHub flow when the remote is GitHub-hosted
- GitLab flow when the remote is GitLab-hosted

## GitHub

Preferred path:
- use `gh pr create` when `gh` is available

Behavior:
- use the selected source branch
- use the user-confirmed target branch
- pass the diff-based title and description
- attach assignee and only existing labels when supported

If `gh` is not available:
- still prepare the title and description
- report the exact next command or manual fallback needed

## GitLab

Preferred path:
- use `glab mr create` when `glab` is available

Behavior:
- use the selected source branch
- use the user-confirmed target branch
- pass the diff-based title and description
- attach assignee and only existing labels when supported

If `glab` is not available:
- still prepare the title and description
- report the exact next command or manual fallback needed

## Creation Rule

Create the request only after:
- the target branch is confirmed
- the diff is reviewed
- the title and description reflect the diff
- the source branch is already pushed
