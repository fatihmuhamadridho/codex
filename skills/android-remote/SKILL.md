---
name: android-remote
description: Use when controlling an Android phone remotely, inspecting Android UI, or automating app flows on a connected device. Use this when the task involves scrcpy live screen streaming, UIAutomator2, ADB taps/swipes/text/keyevents, device wake or unlock checks, UI tree dumps, package launch, text or resource-id lookup, element fallback handling, or safety checks before risky actions like payment, send, or delete.
---

# Android Remote

Use this skill for Android device remote control and UI-driven automation.

This skill separates responsibilities clearly:

- `UIAutomator2` = default selector and inspection layer
- `ADB` = default control, launch, recovery, and verification shell layer
- `scrcpy` = optional live UI streaming and visual confirmation

Prefer element-based automation first when it is usable. Use `scrcpy` only when live visual confirmation is needed. Use coordinate-based control only when the inspection path is unavailable or unstable.

This skill must be verification-first. Do not infer UI state from a successful shell command alone.
This skill must also be tool-state-first. Do not infer that a driver or visual layer is usable merely because a process was launched.
This skill must be session-efficient. Reuse known-good setup from the current session instead of repeating heavy initialization when the same device and layer are still valid.
This skill must also be latency-aware. Once a selector-backed layer is proven usable, stay on the fast path and do not keep re-running heavyweight inspection steps that are no longer needed.

## When To Use

Use this skill when the user wants to:

- remote-control an Android phone over USB or Wi-Fi ADB
- inspect visible UI before clicking
- automate one or more Android app steps
- launch a package and navigate inside it
- search UI by text, resource-id, content description, class, or package
- recover from missing elements by retrying inspection or falling back to ADB actions

Literal trigger examples that should immediately route here:

- "remote android gua"
- "akses device android gua"
- "kontrol HP Android gua"
- "cek layar Android gua"

Do not use this skill for app-specific workflows when a narrower Android app skill already exists for that app. Use this as the foundation skill.

## Default Driver Order

Always try tools in this order:

1. `UIAutomator2` direct inspection/action
2. `ADB` for control, launch, verification, and safe recovery
3. `scrcpy` live stream only if visual confirmation is explicitly needed
4. `adb uiautomator dump` and coordinate fallback only when the normal selector path is blocked

Why:

- `UIAutomator2` gives structured selectors without the startup cost of a heavier external automation stack
- `ADB` is the standard control and verification layer in this environment
- `scrcpy` can add continuous visual state when selector evidence alone is not enough

## Fast Path

Use the fast path by default when all of these are already true in the current session:

- one target device is already known and connected
- the screen is already awake and unlocked
- UIAutomator2 already succeeded against the current device
- the target package or app entrypoint is already known

Fast path rules:

1. do not re-check `scrcpy` unless live visual confirmation is newly required
2. do not run `uiautomator dump` before the first selector-backed attempt
3. do not dump full hierarchy repeatedly after every successful screen transition
4. prefer reusing the last verified selectors, package, activity, and serial
5. if the first selector-backed action fails, allow one targeted refresh only, not a full rediscovery loop

Target latency:

- readiness confirmation: under 10 seconds
- app launch or foreground verification: under 10 seconds
- first selector-backed interaction attempt: under 15 seconds
- fallback decision after selector failure: under 15 seconds

If the flow is trending past 60 seconds without meaningful progress, stop broad probing and switch to the shortest remaining diagnostic path.

## Preconditions

Before acting, verify:

- `adb` can see the device: `adb devices -l`
- if more than one device is connected, use `adb -s <serial>`
- whether the device is asleep or awake
- whether the device is already unlocked or still on the lock screen
- whether `scrcpy` is installed and can attach to the target device if live visual confirmation is needed
- if the task is selector-based, check whether UIAutomator2 is actually usable
- if coordinate actions may be needed, confirm the screen size first: `adb -s SERIAL shell wm size`

If `scrcpy` is missing, blocked, or cannot attach, do not stop. Continue to UIAutomator2 or ADB fallback and say that visual confidence is degraded.
If UIAutomator2 is missing or broken, do not stop unless the user explicitly asked for selector-only automation. Continue with ADB fallback and say that selector confidence is degraded.

Distinguish these states explicitly:

- installed or available
- launched
- attached
- usable for verification or inspection

## Core Workflow

1. Identify the target device.
2. State which execution layer will be used first: `UIAutomator2`, `ADB`, or `scrcpy`.
3. Verify the device is online and authorized.
4. Check whether the screen is asleep, awake, locked, or already unlocked.
5. If the screen is asleep, wake it first.
6. If the device is on the lock screen, run the swipe-only unlock sequence before assuming the device needs credentials.
7. If unlocking requires PIN, password, pattern, or biometric confirmation, stop and ask the user for credentials or ask the user to unlock the device manually.
8. If selector-backed interaction is relevant to the task, test that `UIAutomator2` is usable before dropping to ADB-guided fallback.
9. If live visual confirmation is needed and `scrcpy` is available, attach it after the device is awake and unlocked so the current screen can be monitored live alongside the action layer.
10. If the task targets an app, confirm the package is installed and launch it.
11. For selector-based actions, inspect only the minimum UI evidence needed before clicking.
12. Prefer element actions by `resource-id`, then `text`, then `content-desc`, then stable class/package combinations.
13. If the target element is not found, refresh inspection data and retry once.
14. If still not found, gather UI tree evidence only, search nearby candidates, and only then consider coordinate fallback.
15. Before any risky action, stop and ask for confirmation.
16. After each important state change, verify foreground app or visible UI before continuing.
16a. Do not treat an unchanged activity name by itself as proof that nothing happened when selector evidence or in-app hierarchy shows a more specific state transition inside the same host activity.
17. If the intended post-action state cannot be verified, report it as unverified and do not describe the action as completed.
18. If inspection remains unavailable after one refresh and one evidence pass, stop with a blocker instead of looping through more speculative retries.
19. If a known-good flow already exists in the current session, resume from the last verified checkpoint instead of rebuilding the automation stack from zero.

## Device Readiness

Check device connectivity first:

```powershell
adb devices -l
adb -s SERIAL shell dumpsys window | Select-String -Pattern 'mCurrentFocus|mFocusedApp'
adb -s SERIAL shell dumpsys power | Select-String -Pattern 'Display Power|mWakefulness'
adb -s SERIAL shell dumpsys window policy | Select-String -Pattern 'isStatusBarKeyguard|showing|occluded'
scrcpy --version
```

Interpret common failures:

- `unauthorized`: the phone has not approved ADB yet
- `offline`: reconnect USB or Wi-Fi ADB, then retry
- missing from list: cable, driver, network, or ADB server problem

If multiple devices are connected, never guess. Use an explicit serial or network endpoint.

## scrcpy Live View

Use `scrcpy` only when the task benefits from live visual confirmation beyond what selector-backed evidence already provides.

Use it to:

- stream the current device UI live
- confirm wake, unlock, launcher, and app transitions without needing image capture on every step
- visually validate coordinate fallback before tapping
- detect wrong-state UI earlier, such as lock screen, dialogs, sidebars, filters, or app drift

Useful commands:

```powershell
scrcpy -s SERIAL
scrcpy --serial SERIAL
scrcpy --tcpip=DEVICE_IP:5555
scrcpy --stay-awake -s SERIAL
```

Rules:

- attach `scrcpy` only after `adb` can already see the device
- if there are multiple devices, pass an explicit serial
- prefer `scrcpy` for live verification, but do not treat it as a replacement for `UIAutomator2` selectors
- if `scrcpy` disconnects or fails to attach, continue with the next layer instead of blocking the task
- when `scrcpy` is active, use it as the visual layer instead of screenshot checkpointing
- if the environment cannot render or expose the `scrcpy` window to the operator, treat it as unavailable and fall back cleanly
- do not claim `scrcpy` is active for verification unless attachment or observable usability was confirmed in the current session

## Screen State And Unlock

Always determine whether the device is:

- asleep with the display off
- awake but still showing a lock screen
- awake and already unlocked

Use `dumpsys power`, `dumpsys window`, and `dumpsys window policy` as the first checks. If those signals are messy or vendor-specific, prefer `scrcpy` or additional selector evidence. Do not fall back to screenshots unless the user explicitly asks for them.

Safe wake and unlock helpers:

```powershell
adb -s SERIAL shell input keyevent KEYCODE_WAKEUP
adb -s SERIAL shell input keyevent KEYCODE_MENU
adb -s SERIAL shell input swipe 540 1800 540 600
adb -s SERIAL shell input swipe 120 2100 960 200 250
adb -s SERIAL shell input swipe 900 2100 180 200 250
adb -s SERIAL shell wm dismiss-keyguard
```

Rules:

- if the device is asleep, wake it before anything else
- if the lock screen is supposed to be swipe-only, do not give up after one short swipe
- for swipe-only lock screens, use this order:
  1. `KEYCODE_WAKEUP`
  2. `KEYCODE_MENU`
  3. one centered vertical swipe from near the bottom to near the top
  4. one diagonal swipe from lower-left to upper-right
  5. one diagonal swipe from lower-right to upper-left
  6. `wm dismiss-keyguard`
- after each unlock attempt batch, verify whether `showing=false` or `mIsShowing=false`
- if the device requests PIN, password, pattern, OTP, or biometric confirmation after the swipe-only sequence, do not guess
- if credentials are required, ask the user for them or ask the user to unlock the device manually before continuing
- after wake or unlock attempts, verify the new state before launching apps or tapping UI
- if keyguard is gone but the device lands in recents or another SystemUI surface, send it to the launcher before starting app work

Do not treat a woken device as usable until the lock state is confirmed.

## App Launch And Verification

Use one of these launch strategies:

```powershell
adb -s SERIAL shell pm list packages | Select-String -Pattern 'target.package'
adb -s SERIAL shell monkey -p target.package -c android.intent.category.LAUNCHER 1
adb -s SERIAL shell am start -W -n target.package/.TargetActivity
```

After launch, verify the foreground app:

```powershell
adb -s SERIAL shell dumpsys window | Select-String -Pattern 'mCurrentFocus|mFocusedApp'
```

Do not assume a launch command succeeded just because `adb` returned success.
If the device fell back to the lock screen or turned off again, recover screen state first and then relaunch.
Treat `Status: ok`, `Warning: Activity not started`, or delivery to a top-most instance as transport-level success only, not UI-level success.

## Control Actions

Use ADB for direct screen control and recovery:

```powershell
adb -s SERIAL shell input tap X Y
adb -s SERIAL shell input text "hello%sworld"
adb -s SERIAL shell input swipe X1 Y1 X2 Y2 300
adb -s SERIAL shell input keyevent KEYCODE_BACK
adb -s SERIAL shell input keyevent KEYCODE_HOME
adb -s SERIAL shell input keyevent KEYCODE_ENTER
```

Notes:

- `input text` is best for simple ASCII
- for non-ASCII or special characters, prefer ADB Keyboard if available
- coordinate taps are a fallback, not the first choice
- a successful tap or keyevent does not prove the intended control received focus
- for spaces in `adb shell input text`, use `%s`, not `%20`
- do not assume URL-style encoding works for Android text fields

## Session Reuse

When the same device is still connected in the current session, prefer reusing:

- verified device serial
- verified foreground package knowledge
- verified UIAutomator2 connectivity and selectors that already worked
- verified UI entrypoints that already resolved correctly

Do not restart or reinstall heavy layers unless:

- the previous layer is no longer responding
- the device changed
- the app state invalidated the old checkpoint
- the prior setup was never actually verified

When a layer is already known-good in the current session:

- prefer a health probe over a full restart
- prefer the existing session over recreating it
- prefer targeted selector lookup over full-page hierarchy dumps
- avoid page-source collection unless the next action is blocked

## Inspection And Evidence

Take evidence before fragile actions:

```powershell
adb -s SERIAL shell uiautomator dump /sdcard/window_dump.xml
adb -s SERIAL pull /sdcard/window_dump.xml ./window_dump.xml
```

Use inspection data to search for:

- `resource-id`
- exact visible `text`
- `content-desc`

Do not collect all evidence types by default. Use the lightest evidence that can answer the current question:

1. foreground app or activity check
2. direct selector lookup in UIAutomator2
3. targeted hierarchy refresh
4. full dump only if the selector path is blocked

## Verification Rules

Always distinguish between:

- command accepted
- app foreground verified
- target UI visible
- intended action outcome verified

Never collapse these into one "success" statement unless all relevant levels were checked.
If `scrcpy`, UI hierarchy, and foreground activity disagree or remain ambiguous, say so explicitly.
- `class`
- `package`

Prefer stable identifiers over visible text when both exist.
If `scrcpy` is live, use it to confirm that the dumped hierarchy still matches the actual visible state before acting on a fragile target.

## Selector Strategy

Prefer selectors in this order:

1. exact `resource-id`
2. exact `content-desc`
3. exact visible `text`
4. anchored text with nearby class/package context
5. coordinate fallback after evidence refresh

If an element is ambiguous:

- prefer the visible candidate inside the expected package
- prefer the candidate nearest the expected screen region only after confirming layout evidence
- do not guess across multiple similar buttons when one of them can change account or payment state

## Fallback When Element Not Found

When the element is missing, do this in order:

1. refresh UIAutomator2 source and retry once
2. if `scrcpy` is live, inspect the current screen visually to catch drift or overlays
3. check whether the screen changed and confirm foreground app
4. check whether the device slipped into sleep or lock state
5. search alternative text, content description, or sibling identifiers
6. dump UI tree
7. if the target is visually obvious in `scrcpy` and low-risk, use coordinate fallback after confirming screen size
8. if the action is risky or ambiguous, stop and ask instead of guessing
9. if the dump fails and no selector is available, stop and report that the target is not actionable with current evidence

Do not loop through the same missing-element path more than once for the same target in one turn. Repeated broad retries are a latency bug, not persistence.

If the app or launcher falls into `RecentsActivity` or another SystemUI surface during recovery, re-anchor the device first:

```powershell
adb -s SERIAL shell am start -W -a android.intent.action.MAIN -c android.intent.category.HOME
```

When falling back, explain what degraded. Example:

- `UIAutomator2 selector failed after refresh; using ADB plus UI dump fallback`
- `scrcpy unavailable in this environment; staying on ADB plus selector evidence only`

## Retry Limits

Use these hard limits unless the user explicitly asks for deeper manual probing:

- at most 1 hierarchy refresh for the same target
- at most 1 dump-based evidence pass for the same target
- at most 1 coordinate fallback for the same low-risk target after evidence review
- at most 1 UIAutomator2 reconnect attempt if direct inspection already worked earlier in the session

If those limits are exhausted without verification, stop and report the blocker.

## UIAutomator2 And ADB Expectations

Use `UIAutomator2` when:

- selector-backed inspection is possible
- the task needs stable element targeting
- the app flow has multiple UI transitions and exact state verification matters

Use `ADB` alongside it when:

- launching packages, sending keyevents, or recovering focus
- verifying foreground app, power state, or playback state
- submitting low-risk control actions after the target state is already verified

If `UIAutomator2` is not ready in the environment:

- continue with `ADB` control
- use dumped hierarchy as the inspection source only if the normal selector path is blocked
- state that selector-backed verification is unavailable in the current run

If selectors are unavailable and `scrcpy` is ready:

- use `scrcpy` for live confirmation only if that extra visual layer is actually needed
- use `ADB` control plus dumped hierarchy for evidence
- state that this is a fallback path, not the normal happy path

If `UIAutomator2` was not actually queried successfully in the current session:

- do not imply selector-backed inspection is available
- report that selector availability is unverified or unavailable

If `adb` connectivity is healthy and the task needs UI interaction:

- attempt `UIAutomator2` before falling back to coordinate-driven inspection
- treat `ADB` as the standard control layer, not an inferior emergency path

## Proven Flows

When a flow succeeds with stable selectors or recovery logic, append or refresh the relevant entry here instead of rediscovering it next time.

Prefer reusing proven flows across sessions when the device, package, and visible UI shape still match. Re-verify the live state before acting, but do not throw away a working path just because the session is new.

### Proven device targeting and readiness

- prefer explicit targeting with `adb -s SERIAL` whenever more than one device or transport is visible
- verify wake state with `adb -s SERIAL shell dumpsys power | Select-String -Pattern 'Display Power|mWakefulness'`
- verify foreground and lock-state clues with `adb -s SERIAL shell dumpsys window | Select-String -Pattern 'mCurrentFocus|mFocusedApp'`
- treat wake, unlock, and foreground verification as separate checkpoints

### Proven YouTube inspection pivot

- if `adb shell uiautomator dump` stalls or returns idle-state failures on YouTube, pivot early to `uiautomator2.dump_hierarchy()`
- do not burn retries on repeated `adb uiautomator dump` attempts once YouTube has already shown it does not settle cleanly
- prefer XML-based selector targeting from `uiautomator2.dump_hierarchy()` over screenshot-led guessing

### Proven verification rule

- treat successful command delivery as transport success only
- require a live post-action signal such as foreground app change, visible selector change, or app-specific verification like media state before calling the task successful
- if the post-action state is still ambiguous after one focused refresh, stop and report the ambiguity instead of stacking more guesses

## Safety Rules

Do not perform these actions without explicit user confirmation:

- payment or checkout
- buy, order, rent, subscribe with payment
- send, submit, post, publish, or confirm irreversible forms
- delete, remove, clear data, uninstall, logout, factory reset
- security-sensitive account changes
- entering device credentials or account credentials supplied by the user

Treat labels and intents such as these as guarded:

- `bayar`
- `beli`
- `checkout`
- `order`
- `kirim`
- `send`
- `submit`
- `post`
- `publish`
- `delete`
- `hapus`
- `remove`
- `unsubscribe`
- `logout`

Safe-by-default actions that do not require extra confirmation:

- navigate
- open app
- search
- inspect UI
- wake the screen
- run the swipe-only unlock sequence
- dump hierarchy
- scroll
- back
- home
- play and pause media

## Output Rules

Always report:

- target device serial or endpoint
- which layer was used first
- whether `scrcpy` live view was active or unavailable
- whether fallback happened
- what evidence was used for any fragile step

If you could not verify the final state, say so explicitly.

## Trigger Examples

Use this skill for prompts like:

- "coba kontrol HP Android gua dari adb wifi"
- "launch app ini terus cari tombol login dari resource-id"
- "cek device connected lalu dump UI tree"
- "stream UI Android pakai scrcpy dulu, kalau ga ada baru fallback"
- "kalau elemen ga ketemu, fallback ke dump dan tap"
- "kontrol layar Android pakai uiautomator2 sama adb, jangan screenshot dulu"
