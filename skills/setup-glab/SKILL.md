---
name: setup-glab
description: Use for installing, authenticating, and verifying GitLab CLI on Windows, macOS, or Ubuntu.
---

# Setup GLab

Use this skill when the user wants help setting up GitLab CLI (`glab`) on a machine.

This skill covers:
- checking whether `glab` is already installed
- installing `glab` on Windows, macOS, or Ubuntu
- confirming the target GitLab host before login
- authenticating GitLab CLI
- verifying that `glab` is ready to use

This skill does not cover merge request workflow, advanced `glab` configuration, aliases, or project-level customization.

Read [references/install.md](references/install.md) for install steps by OS.

Read [references/auth.md](references/auth.md) for GitLab authentication and verification.

Read [references/troubleshooting.md](references/troubleshooting.md) when install or auth does not work cleanly.

## Core Workflow

1. Detect whether `glab` is already available.
2. If `glab` is missing, choose the correct install path for the current OS.
3. Verify the installation with `glab --version`.
4. Ask which GitLab host will be used.
5. Run GitLab CLI authentication against that host.
6. Verify login state after authentication.
7. Report whether the environment is ready for normal `glab` usage.

## Default Rules

- Do not assume `glab` is installed.
- Use OS-specific install instructions instead of mixing package managers.
- Confirm the GitLab host before login.
- Verify after install before moving on to auth.
- Verify after auth before declaring success.
- Prefer the normal interactive auth flow unless there is a concrete reason to use token-based auth.

## Boundaries

Use this skill for questions like:
- "bantu setup glab"
- "install GitLab CLI di laptop ini"
- "login glab"
- "cek kenapa glab auth belum beres"

Do not use this skill for:
- creating merge requests
- writing commit messages
- setting up GitHub CLI
- advanced GitLab CLI customization

## Review Checklist

Before finishing, verify:
- `glab` can be executed
- the install path matched the user's OS
- the intended GitLab host was confirmed
- auth completed successfully
- the final auth state matches the expected host and account

## Trigger Examples

Use this skill for prompts like:
- "Use $setup-glab to install and login GitLab CLI."
- "Bantu gua setup glab di laptop ini."
- "Cek apakah glab sudah ke-install dan siap dipakai."
- "Login-in glab buat akun GitLab gua."
