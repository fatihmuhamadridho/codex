---
name: telegram-bot-sender
description: Use when saving Telegram bot tokens with default chat IDs, listing saved bots, or sending Telegram messages through a stored bot like "bot 1", "bot pertama", or a custom alias.
---

# Telegram Bot Sender

Use this skill when the user wants Codex to manage one or more Telegram bot configs and send chat messages through those bots.

This skill is Windows-first and PowerShell-first for this machine.
Do not ask the user to retype bot details that are already stored unless the stored bot is missing or they explicitly want to update it.

## What This Skill Handles

- save a new Telegram bot config
- update an existing bot config
- resolve a bot by `bot 1`, `bot pertama`, or a custom alias
- list saved bot aliases without exposing full tokens
- send a plain text Telegram message through the chosen bot

## Expected Stored Data

Each stored bot should keep:

- `alias`
- `token`
- `default_chat_id`
- `display_name`
- `alias_variants`
- `created_at`
- `updated_at`

Storage path:

- `C:\Users\fatih\.codex\.sandbox-secrets\telegram-bots.json`

This path is intentionally outside the tracked skill tree so secrets do not get committed with normal repo changes.

## Trigger Phrases

Use this skill when the user asks things like:

- `simpan bot 1 token ... id ...`
- `save bot telegram gua`
- `update bot pertama`
- `list bot telegram yang udah disimpen`
- `kirim chat lewat bot 1`
- `kirim pesan pakai finance-bot`
- `pakai bot telegram yang kemarin`

## Workflow

1. Decide whether the user wants to `save`, `update`, `list`, or `send`.
2. Resolve the bot reference conservatively:
   - support numbered aliases such as `bot 1`
   - support Indonesian ordinal wording such as `bot pertama`
   - support custom aliases such as `finance-bot`
3. If saving or updating:
   - require a bot token
   - require a default `chat_id`
   - store the config through `scripts/save-bot-config.ps1`
4. If listing:
   - use `scripts/list-bot-configs.ps1`
   - never print full tokens
5. If sending:
   - require a stored bot reference and message text
   - use the stored default `chat_id`
   - call `scripts/send-telegram-message.ps1`
6. If the bot does not exist, say exactly which alias could not be resolved and ask for token plus `chat_id`.

## Script Entry Points

Use these bundled scripts instead of reimplementing the logic inline:

- `scripts/save-bot-config.ps1`
- `scripts/list-bot-configs.ps1`
- `scripts/send-telegram-message.ps1`

## Usage Examples

### Save

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\save-bot-config.ps1 `
  -Alias "bot 1" `
  -Token "<TELEGRAM_BOT_TOKEN>" `
  -DefaultChatId "882150808"
```

### Save with custom alias

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\save-bot-config.ps1 `
  -Alias "finance-bot" `
  -Token "<TOKEN>" `
  -DefaultChatId "<CHAT_ID>"
```

### List

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\list-bot-configs.ps1
```

### Send

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\send-telegram-message.ps1 `
  -Bot "bot 1" `
  -Message "Halo dari Codex"
```

## Output Rules

- For `save` or `update`, report:
  - resolved alias
  - default `chat_id`
  - masked token
  - whether the bot was created or updated
- For `list`, show:
  - alias
  - display name
  - default `chat_id`
  - masked token
  - last update time
- For `send`, report:
  - resolved alias
  - target `chat_id`
  - Telegram API success or failure
- Mask tokens in any human-facing output.
- Never echo the full raw token back into the chat response after storage.

## Failure Handling

- If the storage file is missing, let the scripts create it.
- If the storage file is invalid JSON, stop and report the file path instead of silently overwriting it.
- If the user asks to send with a bot that is not stored yet, do not guess which bot to use.
- If Telegram returns an API error, surface the returned description directly and keep the local config unchanged.

## Validation

Before stopping, verify:

- the intended alias resolved to exactly one stored bot
- the human-facing output masks the token
- save and list operations keep the config file readable JSON
- send operations use the stored default `chat_id`
