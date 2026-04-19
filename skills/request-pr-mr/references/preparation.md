# Preparation

Use this reference before drafting or creating a request.

## Source Branch

Default the source branch to the current checked out branch unless the user explicitly names a different one.

Before continuing, verify:
- the source branch exists
- the source branch is not detached
- the source branch has already been pushed to the remote

If the source branch has not been pushed, stop and tell the user to push it first.

## Target Branch

Always ask the user which target branch should receive the PR or MR.

Do not guess the target branch from habit, repo defaults, or naming conventions.

Before continuing, verify the chosen target branch exists locally or on the remote.

## Diff as Source of Truth

Compare the source branch against the chosen target branch using the real branch diff.

Use the diff to determine:
- the net purpose of the branch
- the main files and subsystems changed
- whether the branch is actually ready for a request

If the diff is empty, do not create a request.

## Minimal Stop Conditions

Stop and report clearly when:
- the target branch was not provided
- the source branch has not been pushed
- the target branch does not exist
- the source-vs-target diff is empty
