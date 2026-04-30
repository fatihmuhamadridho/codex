# API Contract Shape

Use this guide to keep API contracts consistent and backend-focused.

Write the surrounding explanation in Bahasa Indonesia unless the user explicitly asks for English. Keep endpoint paths, field names, and codes unchanged.

## Endpoint Selection

Document only the endpoints needed to support the chosen feature. A typical set is:

- list endpoint when the UI obviously consumes a table/list view
- detail endpoint when the UI shows a selected row, modal, or detail drawer
- create, submit, update, approve, delete, activate, deactivate, or finish endpoints when the lifecycle requires them
- device or client-facing fetch endpoint only when the UI or workflow implies downstream runtime consumers

Do not inflate the contract with unrelated endpoints.

## Minimum Endpoint Content

For each endpoint include:

- endpoint name or purpose
- `URL`
- `Method`
- `Auth`
- request headers only when they matter
- path params, query params, and request body as relevant
- validation rules
- success response example
- negative cases tied to real business rules
- at least one example response for each important negative case
- write negative cases in a compact status-title format, then place `Example response:` and the JSON example directly underneath

## Default Path Pattern

When the screen shows a standard CRUD master-data flow, prefer these patterns unless the source suggests otherwise:

- `GET /<feature>/v1/list`
- `GET /<feature>/v1/detail/{id}`
- `POST /<feature>/v1/submit`
- `PUT /<feature>/v1/update/{id}`
- `DELETE /<feature>/v1/delete/{id}`

## Response Shape Guidance

Prefer a stable envelope:

```json
{
  "status": {
    "code": "FEAT20000",
    "message": "Success message."
  },
  "data": {}
}
```

Add `meta` for paginated list endpoints.

## Negative Case Guidance

Choose negative cases from the feature's real risks:

- validation failure
- invalid state transition
- duplicate or uniqueness conflict
- quota or inventory exhaustion
- access denied
- not found
- race condition or conflict
- downstream processing failure only when it materially affects the contract

## Status Code Table Alignment

Every internal code in `Table Status Code` should map to a case that appears in the API contract or is clearly implied by the same rules.

Recommended columns:

| HTTP Status | Internal Code | Title | Description |
| --- | --- | --- | --- |

## Style Notes From the Reference PDFs

- Favor business-meaningful error titles over generic labels.
- Include conflict or invalid-state cases when the feature has approval or lifecycle transitions.
- Include async side effects in endpoint logic when the workflow suggests broadcasts, scheduler jobs, notifications, or device sync.
