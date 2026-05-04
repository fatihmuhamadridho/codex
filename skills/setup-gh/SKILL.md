---
name: setup-gh
description: Use for installing, authenticating, and verifying GitHub CLI on Windows, macOS, or Ubuntu.
---

# Setup GH

Use this skill when the user wants help setting up GitHub CLI (`gh`) on a machine.

This skill covers:
- checking whether `gh` is already installed
- installing `gh` on Windows, macOS, or Ubuntu
- authenticating GitHub CLI
- verifying that `gh` is ready to use

This skill does not cover advanced `gh` configuration, PR workflow, aliases, or editor defaults.

Read [references/install.md](references/install.md) for install steps by OS.

Read [references/auth.md](references/auth.md) for GitHub authentication and verification.

Read [references/troubleshooting.md](references/troubleshooting.md) when install or auth does not work cleanly.

## Core Workflow

1. Detect whether `gh` is already available.
2. If `gh` is missing, choose the correct install path for the current OS.
3. Verify the installation with `gh --version`.
4. Run GitHub CLI authentication.
5. Verify login with `gh auth status`.
6. Report whether the environment is ready for normal `gh` usage.

## Default Rules

- Do not assume `gh` is installed.
- Use OS-specific install instructions instead of mixing package managers.
- Verify after install before moving on to auth.
- Verify after auth before declaring success.
- Prefer interactive `gh auth login` unless there is a concrete reason to use another auth path.

## Boundaries

Use this skill for questions like:
- "bantu setup gh"
- "install GitHub CLI di laptop ini"
- "login gh"
- "cek kenapa gh auth belum beres"

Do not use this skill for:
- creating PRs or issues
- writing commit messages
- setting up GitLab CLI
- advanced GitHub CLI customization

## Review Checklist

Before finishing, verify:
- `gh` can be executed
- the install path matched the user's OS
- auth completed successfully
- `gh auth status` confirms the expected GitHub host and account

## Trigger Examples

Use this skill for prompts like:
- "Use $setup-gh to install and login GitHub CLI."
- "Bantu gua setup gh di laptop ini."
- "Cek apakah gh sudah ke-install dan siap dipakai."
- "Login-in gh buat akun GitHub gua."
