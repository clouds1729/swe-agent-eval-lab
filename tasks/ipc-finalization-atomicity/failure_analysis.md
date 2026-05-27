# Failure analysis: ipc-finalization-atomicity

## Why coding agents often patch the symptom

Agents frequently optimize for making visible tests pass quickly. In this task, that can lead to narrow patches such as:
- wrapping only line-item insertion in a try/except,
- adding a compensating delete after failure,
- or reordering writes so failure seems less likely.

These approaches treat specific failure symptoms rather than the underlying consistency guarantee.

## Why atomicity is the real invariant

The business operation is a single unit of work:
1. create IPC period,
2. create all line items,
3. mark all relevant logs finalized.

Correctness requires **all-or-nothing** behavior. If any sub-step fails, the database must remain as if no finalization was attempted. That is exactly the atomicity property provided by a transaction.

## What hidden tests catch

Hidden tests intentionally detect superficial fixes by checking:
- rollback under simulated mid-insert failure,
- controlled behavior on repeated finalization (idempotent or explicit controlled error),
- no mutation of out-of-range logs,
- validation of missing rate before writes occur.

These tests ensure the solution enforces transaction-level invariants instead of patching one branch.
