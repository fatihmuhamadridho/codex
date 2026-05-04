---
name: codex-session-activity-summary
description: Use for summarizing a user's work from Codex session logs for today, yesterday, or a specific date.
---

# Codex Session Activity Summary

Use this skill when the user wants a worklog-style summary from Codex sessions instead of from git history.

## What this skill does

This skill reads `~/.codex/sessions/YYYY/MM/DD/*.jsonl`, extracts task and tool activity, deduplicates overlapping work across multiple sessions on the same date, and returns activity lists in one of three views:

- `per_workspace` for a fuller grouped worklog
- `timeline` for a chronological activity list
- `summary` for the older compact summary

It can also enrich repo labels by scanning configured search roots for `.git` directories, but session `cwd` remains the primary source of truth for where the work happened.

Default output:

- English by default
- switch to Indonesian when the user request is clearly in Bahasa Indonesia
- `per_workspace` view by default
- adaptive number of bullets
- all sessions for the requested date

If the user explicitly asks for a fixed count such as `10 list`, honor that count when the evidence supports it. Do not invent filler if the sessions do not support the requested count.

## Workflow

1. Resolve the target date from the user request.
2. Run the bundled parser script for that date.
3. Inspect the parser output.
4. Inspect detected workspaces and repo labels from the parser output.
5. Optionally enrich repo labels with scoped `.git` discovery when configured.
6. Return the activity list in the view that best matches the request:
   - `per_workspace` when the user wants a fuller list grouped by repo or workspace
   - `timeline` when the user wants the order of work across the day
   - `summary` only when a concise recap is explicitly better

Use the script:

```bash
python3 ~/.codex/skills/codex-session-activity-summary/scripts/summarize_sessions.py --date YYYY-MM-DD --view per_workspace --lang auto --user-text "what did I work on today?"
```

Chronological timeline:

```bash
python3 ~/.codex/skills/codex-session-activity-summary/scripts/summarize_sessions.py --date YYYY-MM-DD --view timeline --lang auto --user-text "what did I work on today in order?"
```

Legacy compact summary:

```bash
python3 ~/.codex/skills/codex-session-activity-summary/scripts/summarize_sessions.py --date YYYY-MM-DD --view summary --lang auto --user-text "give me a short summary of today"
```

If the user requested a fixed number of items:

```bash
python3 ~/.codex/skills/codex-session-activity-summary/scripts/summarize_sessions.py --date YYYY-MM-DD --view per_workspace --max-items 10 --lang auto --user-text "list 10 aktivitas gua hari ini"
```

Use `--format markdown` only if you want a draft list directly from the script. Prefer `json` when you want to inspect evidence before answering.
Use `--lang en` or `--lang id` to force a language. Use `--lang auto` with `--user-text` when you want language selection to follow the user request.
Use scoped repo discovery only when it materially improves repo labels:

```bash
python3 ~/.codex/skills/codex-session-activity-summary/scripts/summarize_sessions.py --date YYYY-MM-DD --lang auto --user-text "what did I work on today?" --discover-git-repos --repo-search-root ~/.openclaw/workspace
```

## Date resolution

Resolve dates conservatively:

- `hari ini` -> current local date from the environment context
- `kemaren` or `kemarin` -> current local date minus one day
- explicit `YYYY-MM-DD` -> use directly

If the user gives a vague phrase you cannot safely resolve from context, ask one short question.

## How to interpret the results

Prefer activity bullets that sound like worklog items, not raw transcript fragments.

Use workspace context from the parser:

- `workspaces` is the raw list of working directories seen that day.
- `workspace_summaries` is the grouped view to prefer for `per_workspace`.
- `timeline` is the ordered event list to prefer for chronological answers.
- `cwd` on each activity is supporting evidence when you need to verify which repo an activity belongs to.
- `repo_roots` is the optional list of discovered repositories from scoped `.git` scanning.
- `repo_root` on each workspace summary is the matched repository root when discovery is enabled.

Good examples in English:

- `Analyzed the reCAPTCHA issue on the token generator page.`
- `Reviewed the front-end flow for load, reset, and token copy.`
- `Investigated browser errors by reading implementation files and searching relevant keywords.`

Good examples in Indonesian:

- `Menganalisis issue reCAPTCHA pada halaman token generator.`
- `Memeriksa implementasi front-end untuk alur load, reset, dan copy token.`
- `Menginvestigasi penyebab error di browser melalui pembacaan file dan pencarian kata kunci terkait.`

Bad examples:

- `rg -n recaptcha index.html`
- `sed -n 221,520p index.html`
- `opened screenshot`

## Output rules

- Use `per_workspace` by default when the user says they want a complete activity list.
- Use `timeline` when the user explicitly wants the order of work across the day.
- Use a flat list inside each workspace section.
- Prefer English verbs such as `Analyzed`, `Created`, `Reviewed`, `Investigated`, `Summarized`, `Adjusted` when the output language is English.
- Prefer Indonesian verbs such as `Menganalisis`, `Membuat`, `Memeriksa`, `Menginvestigasi`, `Merangkum`, `Menyesuaikan`, `Men-debug` when the output language is Indonesian.
- If evidence is weak, use conservative wording.
- If no sessions exist for that date, say that no Codex sessions were found for the requested date.
- Do not mix in git history, shell history, or assumptions outside `~/.codex/sessions` unless the user explicitly asks for it.
- In `per_workspace`, group activities by repo or workspace instead of mixing them into one list.
- In `timeline`, preserve order and include workspace context on each line or when the workspace changes.
- Prefer repo labels such as `alpha-dashboard` or `btcmarketscanner` when they can be derived safely from the workspace path.
- If the repo label is ambiguous, fall back to a short workspace path.
- Prefer session `cwd` for activity ownership. Use `.git` discovery only to improve repo labeling, not to infer activity that does not exist in the session logs.
- Avoid `find . -type d -name ".git"` from an arbitrary current directory as the default strategy. Prefer scoped roots such as a dedicated workspace directory.

## Notes

- Session logs often contain a lot of boilerplate. Trust the script's normalized activities more than raw line-by-line matches.
- Multiple sessions on the same date may cover the same task. Deduplicate aggressively for `summary` and `per_workspace`, but keep more granularity for `timeline`.
- If the user asks for a more casual tone, rewrite the bullets after extraction while keeping the selected language.
- The parser keeps `activities` for compatibility, but `workspace_summaries` and `timeline` should drive final answers depending on the requested view.
- If no language hint is available, default to English.
- For publishable usage, keep repo discovery configurable. Do not assume `.openclaw/workspace` exists for every user; treat it as a local example only.
