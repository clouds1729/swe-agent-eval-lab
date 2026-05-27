from __future__ import annotations

from pathlib import Path

import pytest

from db import connect, init_db
from ipc import FinalizationError, ValidationError, finalize_ipc_period


SCHEMA = Path(__file__).parents[2] / 'starter' / 'schema.sql'


def seed(conn) -> None:
    conn.executemany(
        'INSERT INTO plant_logs(work_date, description, units, rate, finalized) VALUES (?, ?, ?, ?, ?)',
        [
            ('2025-01-02', 'Excavation', 10, 100, 0),
            ('2025-01-03', 'Concrete', 5, 120, 0),
            ('2025-02-01', 'Outside period', 7, 50, 0),
        ],
    )
    conn.commit()


def test_simulated_line_insertion_failure_rolls_back_everything(tmp_path: Path) -> None:
    conn = connect(tmp_path / 'rollback.db')
    init_db(conn, SCHEMA)
    seed(conn)

    with pytest.raises(RuntimeError):
        finalize_ipc_period(conn, '2025-01-01', '2025-01-31', fail_after_items=1)

    assert conn.execute('SELECT COUNT(*) AS c FROM ipc_periods').fetchone()['c'] == 0
    assert conn.execute('SELECT COUNT(*) AS c FROM ipc_line_items').fetchone()['c'] == 0
    statuses = conn.execute('SELECT finalized FROM plant_logs ORDER BY id').fetchall()
    assert [r['finalized'] for r in statuses] == [0, 0, 0]


def test_repeated_finalization_controlled_behavior(tmp_path: Path) -> None:
    conn = connect(tmp_path / 'idempotent.db')
    init_db(conn, SCHEMA)
    seed(conn)

    finalize_ipc_period(conn, '2025-01-01', '2025-01-31')
    line_item_count_before_repeat = conn.execute('SELECT COUNT(*) AS c FROM ipc_line_items').fetchone()['c']

    try:
        finalize_ipc_period(conn, '2025-01-01', '2025-01-31')
    except (FinalizationError, ValidationError, RuntimeError, ValueError):
        pass

    # should not create second period and should not duplicate line items
    assert conn.execute('SELECT COUNT(*) AS c FROM ipc_periods').fetchone()['c'] == 1
    assert conn.execute('SELECT COUNT(*) AS c FROM ipc_line_items').fetchone()['c'] == line_item_count_before_repeat


def test_out_of_range_logs_untouched(tmp_path: Path) -> None:
    conn = connect(tmp_path / 'range.db')
    init_db(conn, SCHEMA)
    seed(conn)

    finalize_ipc_period(conn, '2025-01-01', '2025-01-31')
    outside = conn.execute("SELECT finalized FROM plant_logs WHERE work_date = '2025-02-01'").fetchone()
    assert outside['finalized'] == 0


def test_missing_rate_fails_before_any_writes(tmp_path: Path) -> None:
    conn = connect(tmp_path / 'validation.db')
    init_db(conn, SCHEMA)
    conn.executemany(
        'INSERT INTO plant_logs(work_date, description, units, rate, finalized) VALUES (?, ?, ?, ?, ?)',
        [
            ('2025-01-02', 'Excavation', 10, None, 0),
            ('2025-01-03', 'Concrete', 5, 120, 0),
        ],
    )
    conn.commit()

    with pytest.raises(ValidationError):
        finalize_ipc_period(conn, '2025-01-01', '2025-01-31')

    assert conn.execute('SELECT COUNT(*) AS c FROM ipc_periods').fetchone()['c'] == 0
    assert conn.execute('SELECT COUNT(*) AS c FROM ipc_line_items').fetchone()['c'] == 0
    statuses = conn.execute('SELECT finalized FROM plant_logs ORDER BY id').fetchall()
    assert [r['finalized'] for r in statuses] == [0, 0]
