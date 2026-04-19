# Auth

Use this reference after `glab` is installed.

## Confirm the Host First

Before login, confirm which host the user wants to use:
- `gitlab.com`
- a self-hosted GitLab instance

Do not assume the host.

## Preferred Path

Use the normal login flow against the confirmed host.

Typical flow:
- choose the confirmed host
- use the recommended interactive authentication path for that environment
- verify the resulting login state after auth completes

## Success Criteria

Auth is complete only when the final auth check shows:
- the expected GitLab host
- a logged-in account
- a healthy auth state without an obvious error

## When Token Auth Is Needed

Use token-based auth only when:
- browser or interactive auth is blocked
- the environment is headless
- the user explicitly wants token auth
- the GitLab host policy requires it

If token auth is used, keep the host explicit and verify the final auth state afterward.

## Re-Auth

If an old login is broken or points to the wrong host or account:
- inspect the current auth state first
- re-run auth for the correct host
- verify the final state after the change
