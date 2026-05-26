# Task: Fix approval persistence in a React + TypeScript app

A small transaction approval UI has a subtle state bug.

In the starter app, toggling a transaction's `approved` checkbox appears to work at first, but the change is lost when switching employee filters and coming back.

Your job is to fix the bug so approval state behaves correctly across derived views.

## Requirements

- Do **not** hardcode behavior for specific transactions, employees, or test cases.
- Preserve app behavior and keep the implementation simple.
- The core invariant is:
  - **Approval state belongs to the transaction data itself, not a transient rendered/filter-specific row list.**

## What should work

- Toggling approval updates the correct transaction.
- Switching selected employee away and back keeps prior approval decisions.
- Toggling one employee's transaction does not mutate unrelated employees' transactions.
