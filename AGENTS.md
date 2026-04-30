@C:/Users/fatih/.codex/RTK.md

## Tooling Preference

- Prefer `pnpm` over `npm` for Node.js package management and CLI installs when a Node-based tool is needed.
- Avoid `npm` unless there is no workable `pnpm` path for the task.
- For Python package installs, use `python -m pip` instead of relying on a bare `pip` command.

## Android Skill Routing

- Treat any request to control, inspect, or automate the user's Android device as an explicit trigger for the `android-remote` skill.
- Treat any request involving the Android YouTube app as an explicit trigger for `android-youtube-automation` after `android-remote`.
- For Android YouTube work, do not skip the skill path by jumping straight to ad hoc ADB probing or screenshot-led fallback.
- Prefer `Appium` or `UIAutomator2` as the default action layer once `adb` connectivity is verified.
- Use `scrcpy` only when live visual confirmation is needed, not as a replacement for selector-backed interaction.
- Use screenshots only as a fallback after the structured inspection path is unavailable or unstable.
- If the request clearly names Android remote control plus a specific Android app, start with the app-specific skill if one exists, while still using `android-remote` as the foundation workflow.
- If the user explicitly asks to "remote" the Android device, assume they want live remote-control workflow first, not a screenshot-first workflow.
- Do not claim an Android action succeeded unless the post-action state was verified from live UI, UI hierarchy, foreground activity, or another app-specific success signal.
- If the state is ambiguous, report the ambiguity directly instead of inferring success from a command returning `ok`.
- For Android app automation, treat "command delivered to top-most instance" as non-verifying; it does not prove the intended UI transition happened.
- If the workflow hits repeated ambiguous states, stop calling the task complete and report the exact boundary of what was and was not verified.
- If selector inspection, UI dump, and visual confirmation all fail for the same target, stop with a blocker instead of escalating to repeated guess-based coordinate attempts.
- Do not claim a tooling layer is active or usable just because its process was launched; verify attachment or usable output first.
- Reuse known-good local Android automation setup discovered earlier in the same session instead of re-proving every layer from scratch when the setup is still valid.

## Custom Subagents

### `project_analyst`

Use this subagent when the task is about product or project analysis before implementation.

Call `project_analyst` when you need to:
- analyze a feature or business requirement
- map user flow or system flow from a product perspective
- define scope, assumptions, dependencies, or risks
- write acceptance criteria
- break a feature into backlog items, stories, or tasks
- prepare story sizing in spreadsheet form when the user wants detailed acceptance criteria output similar to an existing sizing sheet

Do not use `project_analyst` for detailed backend API contract design when the main need is request payloads, response schemas, error formats, or endpoint behavior. Use `solutioning_analyst` for that.

Example prompts:
- "Use `project_analyst` to break this feature idea into flow, acceptance criteria, and backlog."
- "Spawn `project_analyst` to analyze the scope and list risks and open questions."
- "Use `project_analyst` to turn this feature into a story sizing sheet like the Example tab."
- "Use `project_analyst` to produce detailed positive flow and negative flow acceptance criteria in sheet form."

Output storage:
- Save `project_analyst` results in spreadsheet form for session-based tracking.
- Default template: `/home/fatihmuhamadridho/.codex/artifacts/templates/project-analysis-template.csv`
- Preferred usage: duplicate the template into a dated working file and update one row per analyzed feature or item.
- When the task is specifically story sizing, prefer writing directly to the target Google Sheet tab using an acceptance-criteria layout with `No`, `Acceptance Criteria`, `Given`, `When`, and `Then`, and make sure the sheet covers detailed positive flow and negative flow rows instead of a compressed summary.

### `solutioning_analyst`

Use this subagent when the task is about backend solution analysis or API design before implementation.

Call `solutioning_analyst` when you need to:
- analyze backend requirements for a feature
- define API flow end-to-end
- design request payloads, headers, params, and validation rules
- define response schema, status codes, and error contract
- analyze downstream integrations, idempotency, retries, side effects, or state changes
- break backend work into technical backlog items

Do not use `solutioning_analyst` for general product discovery, user journey framing, or acceptance criteria that are primarily product-facing unless backend contract design is the main concern. Use `project_analyst` for that.

Example prompts:
- "Use `solutioning_analyst` to define the API contract for this feature, including payload and response format."
- "Spawn `solutioning_analyst` to analyze backend flow, validation, error handling, and integration dependencies."

Output storage:
- Save `solutioning_analyst` results as Markdown technical analysis.
- Default template: `/home/fatihmuhamadridho/.codex/docs/solutioning/templates/solutioning-analysis-template.md`
- Preferred usage: create a dated file per feature under `docs/solutioning/<feature-slug>/`.
