---
name: teams-remote-profile
description: Use for launching or reusing a Chrome remote-debugging profile to inspect and automate Microsoft Teams PWA workflows.
---

# Teams Remote Profile

Use this skill when a task needs repeatable Chrome remote-debugging against a local Chrome profile clone, especially for Microsoft Teams PWA work.

Default assumptions:

- source profile root is `~/.config/google-chrome`
- source profile directory is `Default`
- runtime should use a cloned temp profile under `/tmp`

## Use This Skill For

- launching Chrome with remote debugging without fighting the live profile lock
- checking CDP endpoints and target lists
- finding Teams PWA or Teams web targets
- clearing Teams search input and typing a fresh query
- opening a person or exact search result from Teams search
- closing Teams search overlays that block chat actions
- typing and sending a Teams message in the active conversation
- verifying that a Teams message actually appears in the thread after send

## Core Workflow

1. Run `scripts/launch_profile.sh` to clone the source profile, clear singleton locks, and start Chrome with remote debugging.
2. Run `scripts/cdp_targets.sh` to confirm `json/version` is live and list current page targets.
3. Use `scripts/teams_session.js state` to inspect the active Teams target before doing anything mutating.
4. If Teams search UI is still open, run `scripts/teams_session.js close-search-overlay`.
5. For direct-message or chat lookup, run:
   - `scripts/teams_session.js open-search`
   - `scripts/teams_session.js clear-search`
   - `scripts/teams_session.js search-query "name"`
   - `scripts/teams_session.js open-result "exact visible text"`
6. Confirm the page title or visible header matches the intended chat before mutating the conversation.
7. Before sending a message, run:
   - `scripts/teams_session.js focus-composer`
   - `scripts/teams_session.js type-message "..."`.
8. Only send after the composer text or HTML reflects the intended message.
9. Run `scripts/teams_session.js send-message "..."` when the user clearly asked to send.
10. Always verify delivery with `scripts/teams_session.js tail` or the built-in send verification output.

## Script Reference

- `scripts/launch_profile.sh`
  Starts a temp cloned Chrome profile with CDP enabled. Prints the chosen temp dir, port, and `json/version` payload.
- `scripts/cdp_targets.sh`
  Lists current CDP targets. Pass `teams` to filter Teams URLs and titles.
- `scripts/teams_session.js`
  Node helper for Teams target actions.

Supported commands:

- `state`
- `tail`
- `open-search`
- `clear-search`
- `search-query "text"`
- `search-state`
- `open-result "text"`
- `open-dm "text"`
- `close-search-overlay`
- `focus-composer`
- `type-message "text"`
- `send-message "text"`

## Teams-Specific Rules

- Prefer Teams targets whose title or URL includes `Microsoft Teams`, `teams.cloud.microsoft`, or `teams.microsoft.com`.
- Do not assume a button click means delivery succeeded. Verify that the conversation tail contains the new message.
- `Please type a message to continue.` means the send action happened without the composer being populated in the live DOM.
- If the composer is empty, re-focus it and use `Input.insertText` or direct composer DOM updates before retrying send.
- Search overlays can hijack focus even when the chat view looks active. Close or reset them explicitly before send attempts.
- Search input must be cleared before typing a fresh query. Prefer select-all plus delete, then `Input.insertText`.
- For search-driven navigation, use exact visible text first. Do not silently guess a fuzzy result when multiple candidates exist.

## Trigger Examples

Use this skill for prompts like:

- "Open Teams PWA from the cloned Chrome profile and send a message."
- "Reuse the remote-debug Chrome profile and inspect the active Teams chat."
- "Cari orang dari search Teams lalu buka DM-nya dan kirim chat."
- "Cari target Teams dari CDP lalu isi composer dan kirim pesan."
