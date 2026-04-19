# Repo Rules

Use this reference when deciding how to implement work in a way that feels native to the repository.

## Follow Existing Patterns First

Before adding a new pattern, check whether the repo already has:
- a similar file structure
- a matching component or utility
- a naming convention for the same kind of responsibility
- an established way to pass data, props, or configuration

If the repo already solved the same problem, follow that pattern unless there is a concrete reason not to.

## Keep Scope Tight

Prefer the smallest change that satisfies the request.

Avoid:
- broad refactors hidden inside a narrow task
- touching unrelated files just because they are nearby
- renaming or moving code without a task-driven reason

A local inconsistency can be acceptable temporarily if the alternative is widening the task beyond what the user asked for.

## Reuse Before Reinventing

Prefer this order:
1. reuse an existing abstraction as-is
2. extend an existing abstraction safely
3. create a new abstraction only when the repo does not already have a fit

Do not create a second pattern for the same job without a strong reason.

## Naming and Structure

Use names that match the repo's existing vocabulary.

Prefer:
- domain or responsibility-driven names
- file placement that mirrors similar code nearby
- predictable exports and imports

Avoid:
- vague wrapper names
- one-off naming styles
- folder structures that ignore the existing repo layout

## Maintainability

A valid implementation should be easy for a repo maintainer to recognize and continue.

Aim for:
- readable composition
- clear ownership
- minimal surprise
- low accidental complexity

If the change looks foreign to the rest of the repo, treat that as a warning sign.
