---
name: acceptance-criteria-writer
description: Use when creating or revising business-facing acceptance criteria from BRDs, solutioning docs, or existing feature documents, especially when the output must stay non-technical, actor-based, and aligned to existing artifacts.
---

# Acceptance Criteria Writer

## Overview

Use this skill to turn BRD and solutioning inputs into acceptance criteria that read like business requirements, not API contracts.

This skill is especially important when the user wants acceptance criteria in Markdown, asks to follow an existing document, or keeps pushing the wording away from technical implementation details.

## Trigger Phrases

Use this skill when the request sounds like:

- "buatkan acceptance criteria"
- "bikin AC dari BRD dan solutioning"
- "rapihin AC biar ga teknikal"
- "ubah jadi tabel given when then"
- "fokus dulu di feature ini"
- "jangan pakai istilah endpoint atau backend"

## What Good Output Looks Like

Acceptance criteria produced with this skill should:

- center the actor, such as `Super Administrator`, `Operator`, or another business role
- describe visible user intent, action, and outcome
- stay anchored to BRD, solutioning, and current feature scope
- avoid implementation terms unless the artifact itself requires them
- separate business expectations from technical contract details
- use conservative assumptions when the source artifacts are incomplete
- cover positive flow and relevant blocked, invalid, or negative flow when implied by the source
- preserve the user's requested format, such as Markdown table with `Given`, `When`, `Then`, and optional `And`

## Default Workflow

1. Read the named BRD, solutioning file, and target feature file first.
2. Extract the primary actor, business goal, main action, expected result, and any access restriction.
3. Filter out technical transport details unless the user explicitly wants them.
4. Draft acceptance criteria in business language before thinking about endpoint names, status codes, or backend behavior.
5. If the user wants table output, use columns `AC`, `Given`, `When`, `Then`, and `And`.
6. Re-check each row against the source artifacts and remove invented behavior.
7. If the user reacts against technical wording, rewrite the AC around actor, action, and outcome without defending the technical draft.

## Writing Rules

- Prefer phrases like `Super Administrator membuka...`, `Operator mencoba...`, or `User melihat...`.
- Avoid phrases like `frontend memanggil`, `backend memproses`, `endpoint mengembalikan`, unless the user explicitly asks for technical AC.
- Avoid endpoint paths like `/admin/v1/...` in scope and AC wording when the user wants business-facing output.
- Avoid status code tables in acceptance-criteria documents unless the user asks to keep them.
- Keep scope sections non-technical and capability-based.
- Treat permission and role rules as user-access rules, not as API behavior descriptions.
- If a feature includes first login, reset password, revoke access, or similar lifecycle behavior, describe it from the user or actor perspective first.

## Table Pattern

When the user asks for table-style AC, prefer:

| AC | Given | When | Then | And |
|---|---|---|---|---|

Rules:

- `AC` contains the acceptance-criteria title or numbered identifier.
- `Given` describes actor and starting condition.
- `When` describes the user action or event.
- `Then` describes the main expected outcome.
- `And` captures follow-up outcome, guardrail, or restriction.
- Combine highly similar technical variants into one business row when that makes the AC cleaner.
- Split rows when different user-visible outcomes or restrictions exist.

## Source Priority

When multiple artifacts exist, prefer:

1. The current feature document the user named.
2. Existing solutioning that defines the same feature.
3. BRD statements that define actor, goal, or business rule.
4. Cross-feature user-flow summaries only when they clarify behavior already implied elsewhere.

Do not expand scope just because another artifact mentions adjacent capabilities.

## Red Flags

- Writing AC around `frontend`, `backend`, `endpoint`, `request`, or `response` when the user asked for business-facing AC.
- Leaving endpoint paths in the scope section.
- Adding status code tables into AC docs by default.
- Turning permission rules into implementation notes instead of access rules.
- Inventing actions that are not stated in the BRD or solutioning.
- Keeping technical terms after the user has already asked to remove them.

## Output Checklist

- The AC uses actor-first wording.
- The scope is non-technical.
- The table shape matches the user's requested format.
- Positive flow is present.
- Negative or blocked flow is present when implied.
- Technical contract details are excluded unless explicitly requested.
- Wording follows existing artifacts instead of creating a new product direction.

## Example Adjustments

Prefer:

- `Operator wajib mengganti password sebelum dapat menggunakan akun secara normal`
- `Super Administrator dapat melihat data sesuai hak akses yang dimiliki`
- `Operator tidak dapat mengakses User Management`

Avoid:

- `Frontend memanggil GET /admin/v1/profile`
- `Backend mengembalikan 401 Unauthorized`
- `Response memuat role dan permissions`
