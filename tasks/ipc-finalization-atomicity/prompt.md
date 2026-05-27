Build and fix a small Python + SQLite app that finalizes IPC periods from plant logs.

## Domain scenario
A construction SaaS finalizes IPC periods from plant logs. Finalization should:
1. Create an `ipc_period`
2. Insert corresponding `ipc_line_items`
3. Mark source `plant_logs` as finalized

## Current bug
The starter code performs multiple writes in sequence without transaction safety. If line-item insertion fails midway, the database can end up partially updated (period exists but lines incomplete, or logs finalized incorrectly).

## Your task
Refactor finalization so it is **atomic** using a database transaction.

## Files to work in
- `db.py`
- `ipc.py`
- `schema.sql`
- tests in `starter/tests/`

## Requirements
- Successful finalization creates period, lines, and marks only in-range logs as finalized.
- If insertion fails midway, **all writes are rolled back**.
- Repeated finalization should be idempotent or return a controlled error.
- Missing rate data must raise a validation error **before any writes**.
- Logs outside the date range must remain untouched.

Use SQLite only (no external services).
