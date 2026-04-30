# Feature Inference Rules

Use this guide when the Figma source does not explicitly say what the feature is.

## Primary Heuristics

Choose the feature that is best supported by the strongest visual evidence:

1. dominant form or table title
2. main call-to-action button
3. repeated domain noun across screen elements
4. visible status chips, tabs, filters, or workflow controls
5. detail panel or modal that reveals the main entity lifecycle

## Candidate Feature Naming

Before locking the scope, derive 2-3 candidate feature names from the UI. Good names are domain-specific and lifecycle-aware, for example:

- `Organization Management`
- `Device Pairing`
- `Regular Campaign Submission`
- `Notification Template Management`

Then choose one primary feature and use that consistently across the document.

## One-Feature Boundary

Treat the source as one feature when the screens clearly belong to the same entity lifecycle, such as:

- list + create modal + edit modal
- detail + history tab + approval modal
- draft + submit + approval flow

Split scope mentally and choose only one primary feature when the screens mix unrelated domains, such as:

- dashboard metrics plus user management
- campaign setup plus organization settings
- device troubleshooting plus billing summary

## Conservative Inference Rules

- Infer backend entities only when the UI strongly implies persistence.
- Infer asynchronous processing only when the UI implies broadcasts, notifications, queued jobs, imports, device sync, scheduler behavior, or approval fan-out.
- Infer role-based authorization only when actor separation appears in the source or user prompt.
- Infer deletion, activation, approval, or inventory rules only when the workflow suggests those transitions are meaningful.

## Ambiguity Handling

If ambiguity remains:

1. choose the narrowest feature that still explains the main interaction
2. keep enum names and table names conservative
3. add a short `Assumptions` section after the mandatory 8 sections
4. never expand into a broad platform-wide design unless the user explicitly asks for it
