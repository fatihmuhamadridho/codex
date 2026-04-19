# Metadata Rules

Use this reference for assignee and label handling.

## Assignee

When the platform supports assignees, assign the request to the currently authenticated user by default.

If the provider or CLI does not support setting the assignee directly in the chosen flow, keep the request creation path correct first and report the next manual step if needed.

## Labels

Only attach labels that already exist.

Do not create new labels as part of the request flow.

When label support is available, prefer:
- a type label that matches the branch change when such a label already exists
- any other repo-specific labels only if they already exist and can be matched confidently

If none of the relevant labels exist, create the request without labels.

## Priority Rule

Correct request creation and accurate content are more important than optional metadata.

If metadata support is partial, do not block the request on missing labels or unsupported assignee flags.
