---
name: android-youtube-automation
description: Use for automating the Android YouTube app, including search, playback control, dialogs, and playback-state verification.
---

# Android YouTube Automation

Use this skill for YouTube-specific Android workflows.

This skill depends on `android-remote` for device readiness, wake and unlock handling, `scrcpy` fallback policy, ADB control, inspection flow, and guarded actions. Do not re-invent the low-level control rules here.
When the user explicitly forbids screenshots, do not use screenshots anywhere in the flow. Stay on `adb`, `uiautomator2`, `uiautomator dump`, `dumpsys`, and optionally `scrcpy` if visual confirmation was already allowed.

This skill is app-only. It must stay inside the Android YouTube app. Do not open `youtube.com`, `m.youtube.com`, Chrome, Mi Browser, WebView wrappers, or any other web fallback when the task is supposed to happen in the YouTube app.
Voice search is also out of scope for normal text search. Do not enter YouTube voice-search UI unless the user explicitly asked for voice search.
This skill must be evidence-driven. Do not claim search, result selection, or playback success without a matching post-action signal.
Do not claim a verification layer such as `scrcpy`, selector inspection, or UI dump was usable unless that layer produced usable evidence in the current session.
This skill must preserve momentum within and across sessions. Reuse known-good YouTube entrypoints, fields, and proven flow checkpoints instead of rediscovering them when they still match the live UI.
This skill must also be speed-biased for routine search-and-play tasks. If the request is a straightforward YouTube search and playback, default to the shortest selector-backed path and avoid heavyweight rediscovery.

## When To Use

Use this skill when the user wants to:

- open the Android YouTube app
- search for a video or channel
- open a result
- control playback
- navigate Home, Shorts, Subscriptions, or Library
- dismiss common YouTube popups safely
- inspect YouTube UI before acting

Literal trigger examples that should immediately route here after `android-remote`:

- "buka YouTube di Android gua"
- "cari video di YouTube HP gua"
- "play YouTube di device Android gua"
- "remote Android gua terus buka YouTube"

If the task becomes generic Android automation rather than YouTube-specific behavior, switch back to `android-remote`.

## Default Assumptions

- package: `com.google.android.youtube`
- Android YouTube UI can vary by version, account state, locale, experiment flags, and screen density
- selectors are preferred over coordinates
- account-changing actions are guarded

## Fast Search-To-Play Path

Use this path first for requests like "cari ini terus play":

1. verify the device is still the same known-good target
2. verify YouTube foreground or launch it
3. reuse the last known-good search entry selector
4. reuse the last known-good search text field selector
5. enter the final query once
6. verify the exact query text once
7. submit search once unless the intended result list is already visible after query entry
8. if the intended result list or exact requested title is already visible after query entry, treat search as successful and do not submit or re-submit again
9. open the first clearly playable result or the exact requested title if the user gave one
10. verify player screen or playback state

Do not do these on the fast path unless the selector path is blocked:

- full `uiautomator dump`
- repeated page-source inspection after every click
- re-checking `scrcpy`
- rediscovering selectors that already worked when the visible UI shape still matches

Latency target for normal search-and-play:

- warm session: 10 to 30 seconds
- cold-but-healthy session: under 60 seconds

If the flow exceeds 60 seconds, stop broad exploration and move to the shortest blocker-oriented diagnosis.

## Core Workflow

1. Use `android-remote` to verify device connectivity.
2. Use `android-remote` to ensure the device is awake and unlocked before app actions.
3. Try `UIAutomator2` first for selector-backed interaction with the current YouTube UI, with `ADB` as the standard control and verification partner.
4. If live visual confirmation is needed, use `scrcpy` through `android-remote` as a visual companion for state verification.
4a. Treat `scrcpy` as a companion layer only after current-session attachment or observable usability is confirmed.
5. Confirm the YouTube package is installed.
6. Launch YouTube and verify it becomes the foreground app.
7. Inspect only the minimum current screen evidence needed before acting.
8. Prefer selectors by `resource-id`, `content-desc`, and visible text, but keep the selector scoped to the YouTube package or a verified YouTube hierarchy branch so similarly named SystemUI or launcher controls are not mistaken for in-app targets.
9. Treat YouTube search filters as the wrong state for normal search and back out of them immediately.
10. Treat the YouTube sidebar or navigation drawer as the wrong state for normal search and close it immediately.
11. Treat `VoiceSearchActivity` or any voice-search prompt as the wrong state for normal text search and back out immediately.
12. After every screen transition, refresh the UI source before the next selector-driven action.
12a. If an active edit field such as `com.google.android.youtube:id/search_edit_text` is visible with the intended query, treat the search UI as already open. Do not describe a prior search-button tap as failed just because `dumpsys window` still shows `HomeActivity`.
12b. If matching result titles, result rows, or other clearly playable entries for the intended query are already visible in hierarchy, treat search as already submitted successfully even if the activity name did not change.
12c. Do not treat `com.google.android.youtube:id/search_query` by itself as proof that the active editable field contains the new query, because it can reflect a prior query chip or non-edit display state. Re-anchor on `search_edit_text` or another verified editable field before assuming the new query was really entered.
13. If selectors fail, use the fallback chain from `android-remote`.
13a. If selectors were never proven usable in the current run, report that the flow is running without verified selector support.
14. Stop for confirmation before any state-changing account action.
15. If the search or playback target is still unverified after the allowed retries, stop with a blocker report instead of continuing speculative taps or intents.
15a. If `uiautomator2` and dump-based inspection are both unavailable and screenshots were disallowed by the user, stop with a blocker instead of introducing a screenshot fallback.
16. Do not submit search until the final intended query text is verified in the active search field.
17. For ordinary search-and-play tasks, prefer one exact selector path over broad source inspection.

## Package Verification And Launch

Use commands like:

```powershell
adb -s SERIAL shell pm list packages | Select-String -Pattern 'com.google.android.youtube'
adb -s SERIAL shell monkey -p com.google.android.youtube -c android.intent.category.LAUNCHER 1
adb -s SERIAL shell am start -W -n com.google.android.youtube/com.google.android.apps.youtube.app.WatchWhileActivity
adb -s SERIAL shell dumpsys window | Select-String -Pattern 'mCurrentFocus|mFocusedApp'
```

If the launch intent returns success but foreground focus is still another app, treat the launch as unverified and correct it before proceeding.
If the foreground app becomes a browser or non-YouTube package at any point, treat that as a failure and immediately return to the YouTube app instead of continuing there.
If the foreground app becomes `VoiceSearchActivity`, treat that as a failure for normal search and return to the plain text-search flow.
If an intent is merely delivered to the currently running top-most instance, treat that as unverified until the UI actually changes as intended.

## Preferred YouTube Targets

Look for stable identifiers first, then labels.

Typical target categories:

- search entry or search button
- search text field
- video result rows
- player surface
- play or pause controls
- navigation tabs such as Home, Shorts, Subscriptions, Library
- dismiss buttons for popups and prompts

Prefer:

- exact `resource-id`
- exact `content-desc`
- exact `text`

Selector notes for common YouTube search states:

- prefer `com.google.android.youtube:id/search_edit_text` as the active editable search field
- treat `com.google.android.youtube:id/search_query` as a display or chip-like state unless editability was verified in the current screen
- prefer YouTube-package bottom-tab targets over generic labels like `Home` that can also exist in launcher or SystemUI surfaces

Do not hard-code one selector and assume it will survive every device or app version. Re-check the current hierarchy, but prefer proven selectors before broad rediscovery.

## Standard Flows

### Open YouTube

- verify package
- launch
- confirm foreground app is YouTube

### Search

- find the search affordance
- activate it without tapping the microphone or voice-search entrypoint
- find the search input
- type the query
- verify the full final query text is present in the active editable field before submitting
- prefer `search_edit_text` for this verification; if only `search_query` is visible, confirm it is truly the active editable field before trusting it
- if clearly relevant search results are already visible after query entry, treat the search as successful and continue to result selection instead of submitting again
- submit search
- verify the result screen appeared before opening a result
- if the search field was already open before submission, verify the result list from hierarchy or another app-local signal instead of relying on an activity-name change
- if exact or close-match result titles are already visible in hierarchy, do not classify that state as "search not submitted"; move forward to `Open Result`
- if old suggestions remain visible after new query entry, treat the input state as stale rather than treating the suggestions as fresh results; re-anchor on the active editable field, clear it, and re-enter the query once
- if the result screen cannot be verified, do not claim the query was searched successfully
- do not open or use search filters for ordinary text search
- if a search filter sheet, popup, or filter button state appears, close it with `BACK` and return to plain search results
- do not open the sidebar or hamburger drawer during search
- if the sidebar opens, close it with `BACK` and return to the search field or result list
- do not enter voice-search mode for normal text search
- if voice search opens, close it with `BACK` and return to the search field or result list
- if search is not submitted successfully, retry the in-app search flow once from the YouTube search box
- after one failed in-app retry, stop and report the blocker unless a verified selector or visually confirmed low-risk fallback becomes available
- do not replace failed in-app search with website navigation
- prefer tapping the text field area itself over broad top-right taps that can hit the microphone icon
- do not report search success just because a text input or search intent command returned without error
- if using `adb shell input text`, encode spaces as `%s`, not `%20`
- treat `%20` in an `adb shell input text` command as a bug, because Android text input will type the percent sequence literally instead of a normal space
- for the query `moth to a flame tiktok mashup`, the correct fallback command is `adb -s SERIAL shell input text moth%sto%sa%sflame%stiktok%smashup`
- never send URL-style encoding such as `moth%20to%20a%20flame...` to the YouTube search field
- if `adb shell uiautomator dump` stalls on YouTube, pivot to `uiautomator2.dump_hierarchy()` instead of retrying the same dump path
- if the field contains partial or malformed text such as `moth%`, `20a%20flame`, or any visible `%20` fragment, clear it first and re-enter the full query before any submit action
- never press `ENTER` first and then type; the query text must be established before submission
- if a known-good selector already exists for the search entry or field, reuse it before any new discovery
- do not inspect full page source unless the known-good selector fails
- do not spend more than one retry cycle on ordinary search field discovery

### Open Result

- inspect visible result list
- prefer exact title match when provided
- if the intended title text node is non-clickable, click its verified clickable parent row or another clearly associated low-risk row container before falling back to coordinates
- after clicking a result, verify that the player page or player-adjacent metadata contains the same title before treating the navigation as successful
- if no exact title was requested, prefer the first clearly playable video result
- if exact title is not available, stop and present the closest visible candidates instead of guessing a risky match
- do not treat filter chips or popup items as playable results

### Playback Control

- confirm a player screen is active
- use visible controls or safe media actions
- verify whether the player is already in play or pause state before sending any playback command
- if playback state is already `state=3`, do not send pause, toggle, or play-pause actions just to "confirm" playback
- if playback state is not `state=3`, prefer an idempotent `PLAY` action over `PLAY_PAUSE` so a currently playing item is not accidentally paused
- do not use toggle-style playback commands unless a verified current state makes the toggle safe for the intended outcome
- treat `PlaybackState {state=3 ...}` as playback evidence only after the currently open player page was verified for the intended result in the same run
- if playback resumes at a non-zero position, report that clearly instead of implying a fresh start
- do not claim playback started unless the player screen or playback state was verified

### Navigation

- verify the visible nav tab before tapping
- do not tap generic `Home`, `Back`, or similarly named controls unless they were verified inside the YouTube package; avoid SystemUI or launcher controls that happen to share the same label
- after moving to Home, Shorts, Subscriptions, or Library, refresh inspection data

## Common Interruptions

Handle common non-destructive interruptions safely:

- sign-in prompts that can be dismissed
- update nudges
- cast prompts
- cookie or consent dialogs
- tooltip or coachmark overlays

If dismissing a dialog could change account, payment, or subscription state, stop and ask first.

Treat these as wrong-state UI for standard search playback tasks:

- search filter sheets
- search filter chips that take focus away from the result list
- refine panels that narrow results before any user asked for filtering
- sidebar or navigation drawer overlays
- `VoiceSearchActivity`
- any microphone-first voice input prompt
- browser tabs, browser custom tabs, WebView wrappers, or any page that is not the native YouTube app screen

Default recovery for wrong-state search UI:

1. press `BACK`
2. verify the search field or result list is visible again
3. continue the plain search flow

Default recovery for stale or wrong editable-query state:

1. verify the active editable field inside the YouTube package, preferably `search_edit_text`
2. clear the field completely
3. enter the full final query once
4. verify the exact text in the editable field
5. submit once

Default recovery for browser drift or non-app drift:

1. stop interacting with the browser immediately
2. force-stop the browser package if needed so it cannot keep stealing focus
3. return focus to the YouTube app package
4. verify `com.google.android.youtube` is foreground again
5. restart the plain in-app search flow

Default recovery for voice-search drift:

1. press `BACK`
2. return focus to the YouTube app package
3. verify `com.google.android.youtube` is foreground again
4. restart the plain text-search flow from the search field

## Fallback Rules

When a YouTube selector fails:

1. refresh hierarchy
2. confirm the app is still in the foreground
3. if the current target looks like a filter affordance, filter popup, sidebar state, or voice-search state, back out immediately
4. if foreground moved to a browser or non-YouTube app, return to the YouTube package immediately
5. search alternative label variants
6. inspect dumped hierarchy only if selector evidence is still blocked
7. if `scrcpy` is active because visual confirmation was needed, verify the target visually there before coordinate fallback
8. use coordinate fallback only for low-risk targets that are visually confirmed inside the YouTube app and not on the microphone region
9. if the same search target has already failed through selector refresh plus one low-risk fallback, stop instead of trying more coordinates or intents

Do not expand a failed fast-path search into a long open-ended probe. Keep the diagnostic bounded and report the blocker quickly.

Examples of low-risk fallback:

- opening the search UI
- closing a tooltip
- closing a filter popup with `BACK`
- closing the sidebar with `BACK`
- closing voice search with `BACK`
- back navigation
- opening a clearly labeled non-account video result

Examples that should not be guessed:

- microphone icon or voice-search affordance when the task is plain text search
- browser address bars
- web search boxes
- external browser result pages
- `Subscribe`
- `Join`
- `Buy`
- `Rent`
- `Send`
- posting comments
- account switching
- whether a search result list is open
- whether the intended video is now playing
- repeated taps around the top-right area when search versus microphone is not verified
- repeated search intents after the first unverified delivery

## Safety Rules

Do not perform these without explicit confirmation:

- like
- dislike
- subscribe
- unsubscribe
- comment
- share externally
- cast
- buy
- rent
- paid membership or join
- account switch or account setting changes

Safe-by-default YouTube actions:

- open app
- search
- inspect screen
- open a clearly requested result
- play or pause
- close search filter UI with `BACK`
- close sidebar UI with `BACK`
- close voice-search UI with `BACK`
- back
- home navigation inside the app

## Output Rules

Always report:

- that YouTube was verified as foreground or not
- which selector or fallback method was used
- whether `scrcpy`, selector inspection, or UI dump was actually usable in this session
- whether the chosen result was exact or approximate
- whether voice-search drift happened
- whether any browser drift or non-app drift happened
- whether any guarded action was refused pending confirmation
- which outcomes were verified versus still ambiguous

If the YouTube UI state is ambiguous, stop with a blocker report instead of guessing.
If the only apparent fallback is opening a website, stop and report failure instead of leaving the app.
If search repeatedly drifts into `VoiceSearchActivity`, launcher, browser, or another unverified state, stop and report that the text-search entrypoint could not be verified on the current UI.

## Known-Good Flows

When already verified in the current or a recent matching run, prefer reusing:

- working YouTube search field identifier such as `com.google.android.youtube:id/search_edit_text`
- working search box identifiers such as `com.google.android.youtube:id/search_box`, `com.google.android.youtube:id/search_query`, and `com.google.android.youtube:id/search_clear`
- working result-row identifiers or title/subtitle patterns that already produced playable results
- the last verified foreground app checkpoint
- the last verified distinction between editable-field state and prior-query display state
- the last verified mini-player or watch-page exit path that safely returns to an in-app searchable state without leaving YouTube

Do not redo setup or rediscovery unnecessarily if those checkpoints are still valid.

## Proven Flows

When a YouTube flow succeeds with stable selectors or recovery logic, append or refresh the relevant entry here instead of rediscovering it next time.

Prefer these flows first when the package, screen shape, and foreground app all still match. Re-verify the live state before each important action, but treat these as the stored happy path for future sessions.

### Proven search and play flow on POCO F1 YouTube app

1. Verify the target device explicitly with `adb -s SERIAL`.
2. Verify YouTube is foreground with `adb -s SERIAL shell dumpsys window | Select-String -Pattern 'mCurrentFocus|mFocusedApp'`.
3. If YouTube is not foreground, relaunch it and re-check focus before continuing.
4. Open search from the top-right search affordance. Proven candidates:
   `content-desc='Search'`
   `resource-id='com.google.android.youtube:id/menu_item_view'`
5. Prefer these proven search-field selectors before new discovery:
   `com.google.android.youtube:id/search_edit_text`
   `com.google.android.youtube:id/search_query`
   `com.google.android.youtube:id/search_box`
   `com.google.android.youtube:id/search_clear`
5a. Treat `search_edit_text` as the preferred active editable field. Do not assume `search_query` means the new query was successfully typed unless editability was verified on the current screen.
5b. If the watch page is still active and top-bar search is not cleanly available, prefer a verified in-app exit path such as minimizing the player into mini-player and then reopening search, rather than leaving YouTube or tapping generic system navigation targets.
6. Enter the final query once and verify the exact full text in the active editable field before submit.
6a. When ADB text fallback is needed, convert spaces to `%s` only. Do not use browser or URL escaping.
6b. If the field shows any literal percent fragments like `%20`, treat the entry as failed, clear the field completely, and re-enter the query from the start before submit.
6c. If old suggestion rows remain on screen after entering a different query, do not trust them as current search results. Re-anchor on the editable field, clear it fully, and verify the new text again before submit.
7. If search submission is ambiguous, re-anchor on the verified field and submit once more. Do not fan out into browser, voice search, or repeated top-right taps.
7a. If matching result titles are already visible in hierarchy after query entry, do not treat the state as ambiguous only because the search field disappeared or the activity stayed the same. Proceed directly to result selection.
8. Treat browser drift, voice search, filter UI, sidebar UI, and overlay UI as wrong-state branches. Back out, re-verify `com.google.android.youtube` foreground, and resume the plain text-search flow.
9. If `adb shell uiautomator dump` fails or hangs on YouTube, pivot to `uiautomator2.dump_hierarchy()` and keep using XML-backed selector inspection.
10. Prefer the exact proven result title when visible:
    `Moth To A Flame x After Hours - The weeknd (Tiktok Mashup)`
11. After opening a result, verify playback with `adb -s SERIAL shell dumpsys media_session` and require YouTube `PlaybackState {state=3 ...}` before calling it successful.
11a. Also verify that the watch page still corresponds to the intended title before treating `state=3` as success, because media-session playback alone can reflect a resumed prior item.
11b. If media session already shows the intended item is playing, do not send a toggle command. Only send `PLAY` when the verified state is not already `state=3`.
12. If an ad appears, prefer the proven selector `resource-id=com.google.android.youtube:id/skip_ad_button` with `content-desc='Skip ad'`, then re-check playback state.

## Time Budget

For a routine search-and-play request, use these limits unless the user explicitly asks for deeper debugging:

- at most 1 UIAutomator2 reconnect if direct inspection already worked earlier in the session
- at most 1 selector rediscovery pass for search entry and search field combined
- at most 1 selector rediscovery pass for result-row detection
- at most 1 fallback hop from selector-backed flow to visual or ADB-assisted flow

If those limits are exhausted, stop and report the concrete blocker instead of stretching the run.

## Trigger Examples

Use this skill for prompts like:

- "buka YouTube di HP Android gua terus cari video ini"
- "cek dulu apakah app YouTube kebuka, habis itu play hasil search pertama"
- "otomasi YouTube Android pake selector dulu, jangan asal tap koordinat"
- "kalau popup nongol di YouTube, dismiss yang aman aja"
- "jangan buka search filter, gua cuma mau search biasa terus play"
- "tetep di app YouTube, jangan pindah ke browser atau website"
- "pake uiautomator2 sama adb aja, jangan layer lain atau screenshot dulu"
- "jangan pernah pake screenshot, pakai adb dan uiautomator2 aja"
