from __future__ import annotations

import sqlite3
from dataclasses import dataclass


class FinalizationError(Exception):
    pass


class ValidationError(Exception):
    pass


@dataclass
class FinalizationResult:
    period_id: int
    line_items_created: int
    logs_marked: int


def finalize_ipc_period(
    conn: sqlite3.Connection,
    start_date: str,
    end_date: str,
    *,
    fail_after_items: int | None = None,
) -> FinalizationResult:
    # BUGGY starter: this does writes without transaction protection.
    cur = conn.execute(
        'SELECT id, units, rate FROM plant_logs WHERE work_date >= ? AND work_date <= ? AND finalized = 0 ORDER BY id',
        (start_date, end_date),
    )
    logs = cur.fetchall()
    if not logs:
        raise FinalizationError('No unfinalized logs found for range')

    # Validation before writes: no missing rates allowed.
    for row in logs:
        if row['rate'] is None:
            raise ValidationError(f'Missing rate for log {row["id"]}')

    # write 1: create period
    conn.execute('INSERT INTO ipc_periods(start_date, end_date) VALUES(?, ?)', (start_date, end_date))
    period_id = conn.execute('SELECT id FROM ipc_periods WHERE start_date = ? AND end_date = ?', (start_date, end_date)).fetchone()['id']

    # write 2: insert lines (can fail midway)
    inserted = 0
    for row in logs:
        amount = row['units'] * row['rate']
        conn.execute(
            'INSERT INTO ipc_line_items(period_id, plant_log_id, amount) VALUES (?, ?, ?)',
            (period_id, row['id'], amount),
        )
        inserted += 1
        if fail_after_items is not None and inserted >= fail_after_items:
            raise RuntimeError('Simulated failure while inserting line items')

    # write 3: mark logs finalized
    ids = [str(r['id']) for r in logs]
    conn.execute(f'UPDATE plant_logs SET finalized = 1 WHERE id IN ({",".join(ids)})')
    conn.commit()

    return FinalizationResult(period_id=period_id, line_items_created=inserted, logs_marked=len(logs))
