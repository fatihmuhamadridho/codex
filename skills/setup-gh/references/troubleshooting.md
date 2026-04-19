# Troubleshooting

Use this reference when install or auth does not complete cleanly.

## `gh` Not Found

Symptoms:
- `gh --version` fails
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
- `gh auth login` exits with an error
- browser or device code flow does not complete

Check:
- whether network access to GitHub is available
- whether the correct host was chosen
- whether the environment needs token auth instead of browser auth

## Wrong Account or Host

Symptoms:
- `gh auth status` succeeds, but not for the expected GitHub account or host

Fix:
- inspect current auth state
- re-run login for the intended account or host
- confirm the final account in `gh auth status`

## Done Means Verified

Do not report success just because the install command ran or the login prompt opened.

The setup is done only when both of these work:
- `gh --version`
- `gh auth status`
