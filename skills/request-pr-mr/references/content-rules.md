# Content Rules

Use this reference when drafting the PR or MR title and description.

## Title

The title must summarize the net change between the source and target branches.

Good titles:
- reflect the real branch outcome
- stay concise
- describe what will land after merge

Bad titles:
- blindly copy the latest commit subject
- mention work that is not in the diff
- overstate the scope of the branch

## Description

The description must be based on the actual file changes between the source and target branches.

Prefer concise content that covers:
- main behavior changes
- structural or config changes when they matter
- important implementation notes visible in the diff

Do not invent:
- testing work that is not visible
- rollout steps that are not shown
- side effects that are not supported by the diff
- future work that is not part of the branch

## Diff-Based Summary Rule

If the diff and the latest commit message disagree, trust the diff.

The request text should describe the merged branch result, not just the most recent commit.
