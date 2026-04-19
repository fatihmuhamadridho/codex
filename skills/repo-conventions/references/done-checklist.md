# Done Checklist

Use this checklist before deciding that the work is complete.

## Task Fit

- The implementation satisfies the user's actual request
- The change scope did not drift into unrelated work
- Any assumptions made are visible and reasonable

## Repo Fit

- The implementation follows an existing repo pattern where one exists
- New abstractions were introduced only when necessary
- The code lands in the place a repo maintainer would expect

## Quality Fit

- There is no obviously unfinished wiring
- There are no placeholder names, fake data, or temporary shortcuts presented as final work
- The result is coherent to read and maintain

## Integration Fit

- New code does not create an unnecessary competing pattern
- Reusable code is actually reusable
- Local changes do not leave obvious structural regressions behind

## Final Smell Check

If a maintainer reviewed the diff cold, it should look deliberate, scoped, and consistent with the rest of the repo.
