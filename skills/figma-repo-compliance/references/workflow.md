# Workflow

Use this reference when translating a Figma request into repo work.

## 1. Lock the Figma Target

Start by verifying what the user actually wants implemented.

Preferred order:
1. exact Figma node or frame that can be read
2. screenshot of the intended screen or section
3. clearer frame selection if the provided link is too broad or ambiguous

If the link cannot be read confidently, do not continue with best-effort assumptions. Ask for a screenshot.

## 2. Decide New Feature vs Existing Feature

Before coding, decide whether the design belongs to:
- a new feature that should get its own slice
- an existing feature that should be extended
- a route-only composition change

Use these signals:
- new navigation or distinct product capability usually means new feature
- small variant within an existing flow usually means existing feature
- route wrappers and page metadata usually stay at the page level

Do not attach a new Figma screen to an unrelated existing page just because that page already exists.

## 3. Inspect the Repo Before Building

Check for:
- existing page entrypoints
- existing feature folders that may own the behavior
- reusable UI components
- design-system primitives
- existing naming and composition patterns

The repo should shape the implementation. Figma should not cause a fresh pattern to appear without a good reason.

## 4. Reuse Before Recreate

Prefer this order:
1. existing repo component used as-is
2. existing repo component extended with a safe variant
3. new component composed from existing repo building blocks
4. narrow native HTML only when no fitting abstraction exists

Do not default to composing the full screen from raw HTML if the repo already provides most of the building blocks.

## 5. Enforce Correct Boundaries

Use the local skills for the decisions they own:
- `$fdd`: feature ownership, page boundaries, shared placement
- `$atomic-design`: atom/molecule/organism/template/page splits
- `$clean-architecture`: hooks, use cases, repositories, dependency direction

If the design adds only presentation, do not over-pull architecture concerns into the page.

## 6. Validate Before Completion

Check both dimensions:
- visual: the built screen matches the intended Figma target
- structural: the implementation matches repo rules and reuses the right components

If either dimension fails, the implementation is not done.
