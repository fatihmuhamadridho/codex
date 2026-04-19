# Anti-Patterns

Use this reference when reviewing work that may violate repo conventions.

## Pattern Drift

- Introducing a new implementation style when the repo already has one
- Creating a second abstraction for something the repo already models well
- Naming files or components in a style not used elsewhere nearby

## Scope Drift

- Sneaking unrelated cleanup into a focused task
- Making structural moves that the request did not require
- Touching many files when a local change would have solved the problem

## Incomplete Work Disguised as Done

- Leaving placeholder names or temporary branches in final code
- Wiring only part of the feature and stopping without calling it out
- Returning something that looks finished but still has obvious gaps

## Structural Smells

- Growing a file or page into a catch-all without clear ownership
- Adding wrappers that only increase indirection
- Creating shared code that is still effectively owned by one caller
- Ignoring a local abstraction and rebuilding the same thing nearby

## Reviewer Smell Test

If the diff raises the question "why was it done this way when the repo already has a pattern?", treat that as a likely convention failure and re-evaluate.
