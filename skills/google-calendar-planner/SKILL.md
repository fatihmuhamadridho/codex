---
name: google-calendar-planner
description: Use for turning natural-language plans like "hari ini jam 6 belajar skripsi" into Google Calendar events.
---

# Google Calendar Planner

Use this skill when the user is not just asking about existing calendar state, but wants Codex to help shape a plan and convert it into Google Calendar events.

This skill is planning-first, then calendar-write-ready.
Do not leave vague time phrases unresolved.
Do not write vague event titles like `something` or `task` if the user's intent can be clarified from context.

## When To Use

Use this skill when the user wants to:

- create one or more Google Calendar events from casual language
- turn a rough idea into a concrete schedule
- plan today, tomorrow, or the next few days
- block time for studying, work, errands, exercise, rest, or personal routines
- ask things like "besok gua mau ngapain aja" and expects a suggested agenda
- transform a todo list into calendar slots
- build a simple day plan before writing events into Google Calendar

Typical trigger examples:

- "buatkan calendar buat hari ini jam 6 belajar skripsi"
- "besok gua mau ngapain aja"
- "lusa gua mau ngerjain revisi proposal"
- "tolong bikinin schedule minggu ini"
- "masukin ke Google Calendar ya"

Do not use this skill when the user only wants availability checks, conflict review, or event inspection without planning intent. In that case, use the regular Google Calendar skill flow.

## Core Behavior

Treat the request as one of these modes:

1. `Direct event creation`
The user already gave a clear activity and time.
Example: "hari ini jam 6 belajar skripsi"

2. `Guided planning`
The user gave a day or date, but not a complete schedule.
Example: "besok gua mau ngapain aja"

3. `Todo to calendar`
The user gave several activities that need to be turned into time blocks.
Example: "besok kerjain deck, review PR, terus gym malam"

4. `Draft first, write after`
The user wants a proposed plan before calendar writes happen.

If the user intent is ambiguous, prefer producing a concrete proposed schedule first, then convert it into calendar events.

## Time Normalization

Always normalize relative time into explicit local date and time before reasoning or writing.

Assume the user's working timezone is `Asia/Jakarta` unless the request says otherwise.

Normalize phrases like:

- `hari ini`
- `besok`
- `lusa`
- `minggu depan`
- `jam 6`
- `jam 6 sore`
- `jam 7 malam`
- `abis maghrib`
- `pagi`, `siang`, `sore`, `malam`

Rules:

- Never leave `hari ini`, `besok`, or `lusa` unresolved in the final plan.
- Convert ambiguous time like `jam 6` into an explicit assumption and state it. If context does not disambiguate, prefer `18:00` for evening personal planning requests and flag the assumption.
- If the user gives only a day without time, propose sensible blocks instead of forcing immediate writes with guessed hours.
- If duration is missing, infer a practical default and state it.

Suggested default durations:

- study block: 1.5 to 2 hours
- focused work task: 1 to 2 hours
- quick errand: 30 to 60 minutes
- exercise: 1 hour
- meal block: 1 hour
- commute or buffer: 30 minutes

## Planning Workflow

1. Identify whether the user wants one event, a day plan, or a multi-day plan.
2. Convert all relative dates and times into explicit calendar-ready values.
3. Read relevant calendar state first when collision risk matters.
4. If the user gave a fixed time, preserve it unless there is a conflict the user should know about.
5. If the user did not give a time, propose a practical schedule with short reasoning.
6. Keep the agenda realistic. Add buffers when multiple tasks are packed together.
7. Use concise, human event titles derived from the user's actual activity.
8. Before writing multiple events, present the draft schedule if assumptions are doing meaningful work.
9. When the user clearly wants execution, proceed from draft to Google Calendar event creation/update.
10. After writing, report the exact events created with date, time, duration, and timezone.

## Write Rules

- Preserve exact user-specified dates and times where possible.
- Prefer explicit start and end times over all-day events unless the task is truly all-day.
- Use one event per concrete activity block.
- Avoid over-fragmenting small plans into too many calendar entries.
- For repeated routines, only create recurrence if the user asked for repetition or the intent is clearly recurring.
- If the prompt implies a tentative plan rather than a commitment, say it is a draft before writing.

## Event Naming

Use short, clear titles.

Good examples:

- `Belajar Skripsi`
- `Review PR`
- `Kerjain Deck Presentasi`
- `Gym`
- `Fokus Revisi Proposal`

Avoid:

- `Something`
- `Task`
- `Meeting`
- `Belajar`

If the user's wording is vague, tighten the title using the nearest clear noun or objective from context.

## Output Style

When proposing a plan, present it as a short agenda with exact day, date, start time, end time, and timezone.

When creating events, report:

- event title
- explicit date
- start time
- end time
- timezone
- whether it was newly created or updated

When assumptions were needed, separate them clearly from confirmed details.

## Examples

### Direct event

User:
`hari ini jam 6 belajar skripsi`

Expected behavior:

- interpret `hari ini` using the current local date
- treat `jam 6` as an explicit time assumption if ambiguous
- propose or create an event such as `Belajar Skripsi` from `18:00` to `20:00` in `Asia/Jakarta`

### Guided planning

User:
`besok gua mau ngapain aja`

Expected behavior:

- inspect tomorrow's existing calendar first
- if light or empty, propose a practical agenda
- keep the proposal concise and realistic
- if the user approves or clearly asked to create it, write the events

### Todo to calendar

User:
`besok kerjain skripsi, sore meeting, malam gym`

Expected behavior:

- normalize `besok` to an explicit date
- turn it into separate blocks with reasonable defaults
- check conflicts before writing

## Safety

- Do not silently invent a packed agenda when the user only asked for one event.
- Do not claim calendar creation happened unless the write step actually completed.
- If current calendar state could materially affect the plan, inspect it first rather than assuming the day is empty.
- If the request is too vague for direct writing, return a concrete draft instead of pretending the missing details are known.
