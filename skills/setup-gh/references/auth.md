# Auth

Use this reference after `gh` is installed.

## Preferred Path

Use the interactive login flow:

```bash
gh auth login
```

Typical choices:
- GitHub.com as the host
- HTTPS as the protocol
- browser or device login flow for authentication

After login, verify with:

```bash
gh auth status
```

## Success Criteria

Auth is complete only when `gh auth status` shows:
- the expected GitHub host
- a logged-in account
- a healthy auth state without an obvious error

## When Token Auth Is Needed

Use token-based auth only when:
- browser or device flow is blocked
- the environment is headless
- the user explicitly wants token auth

In that case, keep the flow explicit and verify with `gh auth status` afterward.

## Re-Auth

If an old login is broken or points to the wrong account:
- check current status first
- re-run `gh auth login` for the correct account or host
- verify the final state after the change
