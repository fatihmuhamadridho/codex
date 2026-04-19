# Install

Use this reference when `glab` is not installed yet.

## First Check

Start with:

```bash
glab --version
```

If the command succeeds, `glab` is already installed and you can move to authentication.

If the command fails, install `glab` using the correct path for the current OS.

## Windows

Preferred approach:
- install GitLab CLI with `winget` when available

Example:

```powershell
winget install --id GitLab.glab
glab --version
```

Fallback:
- use the official GitLab CLI installer package for Windows if `winget` is unavailable

## macOS

Preferred approach:
- install with Homebrew

Example:

```bash
brew install glab
glab --version
```

Fallback:
- use the official GitLab CLI package for macOS if Homebrew is not available

## Ubuntu

Preferred approach:
- install from the official package path supported by GitLab CLI documentation for Debian-based systems

Minimal guidance:
- add the GitLab CLI package source if needed
- install `glab` through `apt`
- verify with `glab --version`

If the environment already uses a company-approved package source, follow that instead of inventing a new install path.

## Verification

The install step is not done until:
- `glab --version` succeeds
- the shell can find `glab` without a temporary path hack
