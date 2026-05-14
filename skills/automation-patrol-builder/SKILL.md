---
name: automation-patrol-builder
description: Use when creating, repairing, or normalizing recurring patrol-style automations that must perform real work per cycle, keep thread continuity when needed, send Telegram status updates, and stop cleanly when the tracked work is finished
---

# Automation Patrol Builder

## Overview

Use this skill for patrol-style automation, not for generic reminders. The default target is a recurring automation that executes one clear unit of work per cycle, reports progress, preserves continuity, and stops when the job is actually done.

Primary output from this skill:
- automation spec decisions
- prompt update for `automation.toml`
- audit notes for existing automation config and memory

## When to Use

Use this skill when the user asks for any of these:
- buat automation patrol
- benerin automation yang tidak jalan
- buat recurring automation yang harus kirim Telegram
- pakai satu thread saja
- jangan jadi heartbeat atau no-op validation
- audit `automation.toml` yang sekarang

Do not use this skill for:
- one-shot reminders
- simple follow-up pings with no real work unit
- automations that do not need thread continuity, patrol review, or cycle status reporting

## Workflow

Follow these three stages in order.

### 1. Pahami unit kerja berulang dan condition selesai

Confirm these decisions first:
- apa unit kerja nyata per cycle
- apa source of truth untuk memilih item berikutnya
- kapan sebuah cycle dianggap `completed`
- kapan sebuah cycle dianggap `blocked`
- kapan automation harus mengirim pesan final dan berhenti total

If the automation is meant to process backlog-like work, prefer one work item per cycle. Do not let one cycle split focus across multiple unrelated items unless the user explicitly wants batch processing.

### 2. Validasi keputusan teknis automation

Before editing or generating the spec, verify these decisions:
- `kind`: gunakan `cron` untuk kerja nyata terjadwal; jangan pakai `heartbeat` kalau tujuannya eksekusi kerja
- `target_thread_id`: wajib jika user ingin satu thread yang sama
- `rrule`: wajib, gunakan format `RRULE:...`
- `cwds`: wajib untuk memberi workspace target yang jelas
- `model`
- `reasoning_effort`
- `execution_environment`
- aturan memory file di `$CODEX_HOME/automations/<automation_id>/memory.md`
- aturan notifikasi Telegram dan alias bot

If any of the fields above are missing, do not call the automation healthy yet.

### 3. Hasilkan prompt/spec final dan audit existing config

The deliverable should be concrete enough to apply directly:
- prompt final untuk automation
- keputusan field penting `automation.toml`
- audit checklist untuk config existing
- recovery notes kalau automation sedang rusak

When repairing an existing patrol, do not stop at “prompt sudah bagus”. Check the loader-sensitive fields and the memory flow too.

## Patrol Defaults

Use these defaults unless the user explicitly overrides them:

- one-cycle-one-unit-of-work
- state progres ringkas ditulis ke memory automation
- Telegram update wajib setelah cycle `completed` atau `blocked`
- final Telegram wajib sebelum automation dianggap selesai total
- gunakan `target_thread_id` bila user ingin continuity satu thread
- jangan pakai Bahasa Inggris jika user meminta Bahasa Indonesia only
- bedakan fitur `blocked karena missing existing` vs `greenfield boleh dibuat`
- cycle belum selesai kalau status Telegram belum terkirim

### Blocked vs Greenfield Rule

Use this distinction explicitly in the prompt when the automation writes docs or solutioning:

- `blocked`: item seharusnya punya baseline/existing, tetapi source existing belum tersedia atau belum diletakkan di lokasi yang dibutuhkan
- `greenfield`: item memang baru dan boleh dikerjakan dari source yang tersedia

Do not collapse all `no existing` cases into `blocked`.

## Required `automation.toml` Checklist

Use this checklist every time:

| Field | Why it matters | Patrol expectation |
| --- | --- | --- |
| `version` | loader compatibility | keep present and valid |
| `id` | stable automation identity | unique and unchanged unless intentionally replaced |
| `name` | UI discoverability | clear patrol name |
| `kind` | execution behavior | `cron` for real patrol work |
| `prompt` | worker instruction | must describe work, not validation chatter |
| `status` | activation state | usually `ACTIVE` when ready |
| `rrule` | schedule | must use `RRULE:` prefix |
| `model` | runtime quality/cost | explicitly set |
| `reasoning_effort` | runtime behavior | explicitly set |
| `execution_environment` | runtime target | explicitly set |
| `cwds` | workspace target | must not be empty |
| `target_thread_id` | thread continuity | set when single-thread behavior is desired |
| `created_at` / `updated_at` | loader metadata | preserve valid values when required by existing pattern |

## Prompt Rules

The prompt must clearly separate:
- actual work per cycle
- review/fix loop within that same cycle
- notification requirement
- stop condition when all work is done

The prompt must not sound like a health check. It should instruct execution, not validation.

### Anti-Patterns

Do not produce prompts that:
- change real work into heartbeat validation
- omit `cwds`
- omit the done rule
- say only `Instruksi automation masih relevan`
- say only `lanjutkan jika perlu` without defining the cycle
- send Telegram optionally when the user asked it as mandatory

## Failure Recovery Checklist

Use this when the automation misbehaves.

### 1. Automation muncul tapi tidak jalan

Check:
- `status = "ACTIVE"`
- `kind` sesuai tujuan
- `rrule` valid
- `cwds` ada dan benar
- prompt memang berisi instruksi kerja nyata

### 2. Automation hilang dari UI

Check:
- file `automation.toml` masih ada
- format TOML valid
- field loader-sensitive masih lengkap: `version`, `id`, `name`, `kind`, `status`, `rrule`, `model`, `reasoning_effort`, `execution_environment`, `cwds`

### 3. Automation masuk mode heartbeat padahal harus kerja nyata

Check:
- `kind` jangan `heartbeat`
- prompt jangan berbunyi seperti validasi no-op
- jangan biarkan cycle berakhir tanpa unit kerja yang dikerjakan

### 4. Thread pecah terus

Check:
- `target_thread_id` sudah dipasang
- prompt menyebut untuk lanjut di thread yang sama
- pahami bahwa prompt membantu, tapi `target_thread_id` adalah sinyal teknis yang lebih kuat

### 5. Telegram tidak terkirim

Check:
- alias bot benar
- prompt mewajibkan Telegram sebagai bagian dari completion cycle
- message format sudah jelas: nama item, status, sisa pekerjaan

## Existing Automation Audit Template

Use this audit shape when inspecting an existing patrol:

1. `automation.toml`
   - apakah `kind` benar
   - apakah `rrule` valid
   - apakah `cwds` ada
   - apakah `target_thread_id` perlu atau sudah ada
   - apakah prompt jelas menginstruksikan kerja nyata
2. memory
   - apakah file memory ada
   - apakah state terbaru tercatat
   - apakah ada drift antara memory dan prompt saat ini
3. thread target
   - apakah automation memang diarahkan ke satu thread bila diminta
4. Telegram
   - apakah alias bot disebut jelas
   - apakah notifikasi per cycle dan final sudah mandatory
5. loader-sensitive fields
   - `version`
   - `id`
   - `name`
   - `status`
   - `rrule`
   - `model`
   - `reasoning_effort`
   - `execution_environment`
   - `cwds`

## Patrol Prompt Template

Use the template in [`templates/patrol-prompt.md`](C:/Users/fatih/.codex/skills/automation-patrol-builder/templates/patrol-prompt.md). Fill in these inputs:
- objective
- source of truth
- per-cycle unit of work
- blocked vs greenfield rule
- notification behavior
- done/stop rule

## Telegram Status Template

Use the message shapes in [`templates/telegram-status.txt`](C:/Users/fatih/.codex/skills/automation-patrol-builder/templates/telegram-status.txt).

## Debug Reference

Use [`references/automation-debug-checklist.md`](C:/Users/fatih/.codex/skills/automation-patrol-builder/references/automation-debug-checklist.md) when the automation is visible but broken, missing from UI, stuck in heartbeat behavior, splitting threads, or failing to send Telegram.

## Quick Output Shape

When applying this skill, prefer output in this structure:

1. Patrol objective
2. Unit of work per cycle
3. Required `automation.toml` decisions
4. Final prompt update
5. Audit findings on current config
6. Recovery fixes, if any
7. Done rule and final notification rule

## Common Mistakes

- Menganggap patrol sama dengan heartbeat
- Menulis prompt yang terlalu umum sampai automation hanya membalas status
- Lupa `cwds`
- Lupa `target_thread_id` saat user minta satu thread
- Tidak menulis aturan stop final
- Tidak membedakan `blocked` dan `greenfield`
- Menganggap edit prompt saja cukup tanpa audit field teknis
