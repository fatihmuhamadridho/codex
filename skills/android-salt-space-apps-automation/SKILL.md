---
name: android-salt-space-apps-automation
description: Use when automating the Android Salt Space app (`salt.id.space.android`) for attendance flows such as clock in and clock out. Trigger this skill for requests about opening Space Apps on the user's Android device, verifying the clock-in or clock-out detail page, tapping the home `Clock In` or `Clock Out` buttons, optionally submitting the matching detail button, and verifying post-submit attendance UI without relying on activity changes alone.
---

# Android Salt Space Apps Automation

Use this skill for Salt Space attendance workflows on Android.

This skill depends on `android-remote` for device readiness, wake and unlock handling, selector-first interaction policy, ADB verification, and guarded-action behavior. Reuse that skill's low-level rules instead of repeating them here.

This skill is app-specific. Keep the flow inside `salt.id.space.android`. Do not replace the app flow with browser automation, web fallback, or generic coordinate guessing when selector-backed inspection is still possible.
This skill must be evidence-driven. Do not claim a page transition, button click, or submit success from transport success alone.
This skill must treat detail `Clock In` and detail `Clock Out` as state-changing actions. Default to asking for approval before tapping those detail buttons unless the user explicitly asked for auto submit.

## When To Use

Use this skill when the user wants to:

- open Space Apps or the Salt Space attendance app on Android
- clock in from the app
- clock out from the app
- verify the clock-in detail page or clock-out detail page
- check whether the matching detail submit button exists before tapping it
- submit the detail `Clock In` or `Clock Out` button when the user explicitly asks for it

Literal trigger examples:

- "buka space apps terus clock in"
- "cek tombol clock out di detail"
- "auto submit clock in di salt app"
- "coba buka space apps android terus verifikasi clock in"

## Default Assumptions

- package: `salt.id.space.android`
- launcher activity: `salt.id.space.android/.MainActivity`
- device targeting should prefer explicit `adb -s SERIAL`
- selector-backed interaction is preferred over coordinates
- `Clock In` and `Clock Out` home flows may remain inside `.MainActivity`, so activity changes alone are not enough to prove navigation

## Core Verification Rule

Always separate these checkpoints:

- command delivery succeeded
- Salt Space is foreground
- the intended home button is visible
- the intended detail page is visible
- the detail submit button exists
- the detail submit button was actually tapped
- post-submit success was actually verified

Do not collapse them into one success statement.

## Known-Good Evidence

Prefer these verified signals first when the UI still matches:

- foreground app from `adb -s SERIAL shell dumpsys window | Select-String -Pattern 'mCurrentFocus|mFocusedApp'`
- home `Clock In` button:
  - `class="android.widget.Button"`
  - `content-desc="Clock In"`
- home `Clock Out` button:
  - `class="android.widget.Button"`
  - `content-desc="Clock Out"`
- clock-in detail page evidence:
  - header `Clock In`
  - `ATTENDANCE INFO`
  - detail button `Clock In`

Use the same pattern for `Clock Out`. If exact text differs slightly on the detail page, prefer the matching header plus the matching bottom button before considering the page ambiguous.

## Core Workflow

1. Use `android-remote` to verify the target device is connected, awake, and unlocked.
2. Verify whether Salt Space is already foreground.
3. If Salt Space is not foreground, launch `salt.id.space.android/.MainActivity` and re-check focus.
4. Use selector-backed inspection first.
5. Use ADB as the standard foreground verification layer.
6. Treat `.MainActivity` as a transport checkpoint only, not proof of which in-app page is open.
7. Verify the target home button before tapping it.
8. After tapping the home button, verify the detail page from hierarchy or other app-local UI evidence.
9. Verify the matching detail submit button exists before deciding whether to tap it.
10. By default, stop and ask the user for approval before tapping the detail submit button.
11. Only auto-submit when the user explicitly asks for direct submission.
12. If submission happened and the request expects final verification, look for a post-submit success signal before claiming completion.

## Clock In Flow

Use this flow for requests to clock in or inspect the clock-in detail page:

1. Verify Salt Space is foreground or launch it.
2. Verify the home `Clock In` button exists.
3. Tap the home `Clock In` button.
4. Verify the clock-in detail page with UI evidence, not just activity state.
5. Prefer this detail-page evidence:
   - header `Clock In`
   - `ATTENDANCE INFO`
   - detail submit button `Clock In`
6. If the detail button only needs verification, stop after confirming it exists.
7. If the user did not explicitly request auto submit, stop and ask for approval before tapping the detail `Clock In` button.
8. If the user explicitly requested auto submit, tap the detail `Clock In` button.
9. If post-submit verification is required, look for a success signal such as a toast, changed attendance status, a success page, or another clear in-app confirmation.
10. If no final success signal can be verified when post-submit verification was required, report the submit as unverified rather than successful.

## Clock Out Flow

Use this flow for requests to clock out or inspect the clock-out detail page:

1. Verify Salt Space is foreground or launch it.
2. Verify the home `Clock Out` button exists.
3. Tap the home `Clock Out` button.
4. Verify the clock-out detail page with UI evidence, not just activity state.
5. Prefer the matching `Clock Out` header plus the matching bottom `Clock Out` button as the primary evidence.
6. If `ATTENDANCE INFO` or similar attendance detail text appears alongside the `Clock Out` button, treat that as strong supporting evidence.
7. If the detail button only needs verification, stop after confirming it exists.
8. If the user did not explicitly request auto submit, stop and ask for approval before tapping the detail `Clock Out` button.
9. If the user explicitly requested auto submit, tap the detail `Clock Out` button.
10. If post-submit verification is required, look for a success signal such as a toast, changed attendance status, a success page, or another clear in-app confirmation.
11. If no final success signal can be verified when post-submit verification was required, report the submit as unverified rather than successful.

## Inspection Strategy

Prefer this order:

1. foreground check with `dumpsys window`
2. direct selector lookup with `uiautomator2`
3. `uiautomator2.dump_hierarchy()` for app-local UI evidence
4. `adb shell uiautomator dump` only if it is working reliably on the current screen
5. coordinate fallback only for low-risk navigation taps after evidence review

If `adb shell uiautomator dump` hangs or fails, prefer `uiautomator2.dump_hierarchy()` instead of retrying the same failing dump path.

## Fallback Rules

When a Salt Space target is missing:

1. refresh hierarchy once
2. verify Salt Space is still foreground
3. re-check the expected home or detail button
4. if the target is still missing, gather one bounded evidence pass from hierarchy
5. if the page remains ambiguous after that pass, stop with a blocker instead of stacking more guesses

Do not do these:

- do not claim success from `adb` returning `ok`
- do not claim detail-page navigation from `.MainActivity` alone
- do not keep tapping multiple buttons with the same label when the page state is not verified
- do not use browser fallback
- do not use repeated coordinate guesses for state-changing actions

## Stop Conditions

Stop and report a blocker when:

- the home target button is missing
- the detail page cannot be identified with reasonable confidence
- selector-backed inspection and dump-based inspection both fail
- auto submit was requested but the final success signal cannot be verified when post-submit verification is required

## Output Rules

Always report:

- target device serial or endpoint
- whether Salt Space was verified as foreground
- which layer was used first
- whether selector inspection or hierarchy dump was actually usable
- whether the home button was verified before tapping
- whether the detail page was verified from UI evidence
- whether the detail submit button was only verified or actually tapped
- whether post-submit success was verified or still ambiguous

If final success was not verified, say so explicitly.
