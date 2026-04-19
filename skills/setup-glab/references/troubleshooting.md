# Troubleshooting

Use this reference when install or auth does not complete cleanly.

## `glab` Not Found

Symptoms:
- `glab --version` fails
- shell says command not found

Check:
- whether install really completed
- whether the chosen package manager exists on the machine
- whether the shell session needs to be reopened to refresh PATH

## Wrong Install Path

Symptoms:
- install command fails because the package manager is not available

Fix:
- switch to the correct OS-specific install route
- do not mix Homebrew, winget, and apt instructions on the wrong platform

## Auth Fails

Symptoms:
- login exits with an error
- browser or interactive flow does not complete

Check:
- whether network access to the GitLab host is available
- whether the correct host was chosen
- whether the environment needs token auth instead of the default auth flow

## Wrong Host or Account

Symptoms:
- auth succeeds, but not for the expected GitLab host or account

Fix:
- inspect the current auth state
- re-run auth for the intended host
- confirm the final host and account after the retry

## Done Means Verified

Do not report success just because the install command ran or the login prompt opened.

The setup is done only when both of these are true:
- `glab --version` works
- the final auth check confirms the expected host and account
