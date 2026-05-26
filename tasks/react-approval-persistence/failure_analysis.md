# Failure analysis

## Likely coding-agent shortcut

A common shortcut is to store approval toggles in filter-local UI state (for example, a temporary list of rendered rows or per-view overrides), instead of updating the canonical transaction records.

That can make the checkbox appear to work in the current render, but the state disappears when the app recomputes a filtered view.

## Correct invariant

**Approval state belongs to transaction data, not transient rendered rows.**

In other words, when a transaction is toggled, the source transaction collection must be updated by stable transaction identity. Any filtered list should be derived from that source-of-truth state.

## Why visible tests are insufficient

Visible tests only assert that a checkbox can be toggled immediately in the current view.

A buggy implementation can satisfy this with ephemeral state and still lose updates during view transitions.

## Why hidden tests are fair

Hidden tests validate realistic user behavior:

1. Toggle approval on one transaction.
2. Switch to another employee filter.
3. Return to the original employee.
4. Confirm the original approval persists.
5. Confirm unrelated employees' transactions keep their original approval state.

These checks enforce the intended data invariant without depending on implementation details.
