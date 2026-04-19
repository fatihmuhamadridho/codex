# Install

Use this reference when `gh` is not installed yet.

## First Check

Start with:

```bash
gh --version
```

If the command succeeds, `gh` is already installed and you can move to authentication.

If the command fails, install `gh` using the correct path for the current OS.

## Windows

Preferred approach:
- install GitHub CLI with `winget` when available

Example:

```powershell
winget install --id GitHub.cli
gh --version
```

Fallback:
- use the official GitHub CLI installer package for Windows if `winget` is unavailable

## macOS

Preferred approach:
- install with Homebrew

Example:

```bash
brew install gh
gh --version
```

Fallback:
- use the official GitHub CLI package for macOS if Homebrew is not available

## Ubuntu

Preferred approach:
- install from the official package path supported by GitHub CLI documentation for Debian-based systems

Minimal guidance:
- add the GitHub CLI package source if needed
- install `gh` through `apt`
- verify with `gh --version`

If the environment already uses a company-approved package source, follow that instead of inventing a new install path.

## Verification

The install step is not done until:
- `gh --version` succeeds
- the shell can find `gh` without a temporary path hack
