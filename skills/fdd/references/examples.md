# Examples

Use these examples when placement is unclear or when reviewing a proposed refactor.

## Example 1: Keep logic inside a feature

Scenario:
- `src/features/checkout` contains form state, pricing summary, submit flow, and error handling for checkout

Correct decision:
- keep pricing recalculation, submit orchestration, and checkout validation inside `src/features/checkout`

Why:
- these rules belong to one capability and would be misleading in shared code

## Example 2: Keep page routing-only

Scenario:
- `src/pages/checkout.tsx` parses query params, chooses the checkout feature screen, and exports `getServerSideProps`

Correct decision:
- keep route parsing and `getServerSideProps` in the page
- move checkout-specific transformation or orchestration into `src/features/checkout`

Why:
- the page owns the route boundary
- the feature owns the checkout behavior

## Example 3: Promote only truly shared non-UI code

Scenario:
- multiple features need the same currency formatting helper

Correct decision:
- place the formatting helper in `src/commons/*`

Why:
- it is non-UI and domain-neutral across features

Counterexample:
- a helper named `normalizeCheckoutItems` should stay in checkout unless it becomes generic and renamed to match that abstraction

## Example 4: Shared UI goes to `commons-ui`

Scenario:
- multiple screens need a generic modal with title, body, and action slots

Correct decision:
- put the modal in `src/commons-ui/*`

Why:
- it is reusable presentation and should not know any feature workflow

Counterexample:
- `CheckoutPaymentModal` with payment branching and submit rules stays in the checkout feature

## Example 5: Reject feature-to-feature import

Scenario:
- `src/features/orders` imports a hook directly from `src/features/checkout`

Correct decision:
- reject the direct dependency

Better options:
- keep each feature isolated
- extract a generic shared abstraction only if it is truly stable and domain-neutral
- otherwise duplicate a small helper locally

## Anti-Patterns

Watch for these failures:
- pages becoming the real feature container
- `commons` filling with disguised feature code
- `commons-ui` containing data fetching or domain branching
- one feature importing another feature's hooks, state, or UI directly
- extracting to shared before reuse is real
