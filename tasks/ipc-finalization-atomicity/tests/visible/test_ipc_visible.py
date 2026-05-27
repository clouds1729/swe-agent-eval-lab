from __future__ import annotations

from pathlib import Path

from db import connect, init_db
from ipc import finalize_ipc_period


def seed_logs(conn) -> None:
    conn.executemany(
        'INSERT INTO plant_logs(work_date, description, units, rate, finalized) VALUES (?, ?, ?, ?, ?)',
        [
            ('2025-01-02', 'Excavation', 10, 100, 0),
            ('2025-01-05', 'Hauling', 3, 80, 0),
            ('2025-02-01', 'Out of range', 7, 50, 0),
        ],
    )
    conn.commit()


def test_successful_finalization_creates_period_lines_and_marks_only_in_range(tmp_path: Path) -> None:
    conn = connect(tmp_path / 'app.db')
    init_db(conn, Path(__file__).parents[2] / 'starter' / 'schema.sql')
    seed_logs(conn)

    result = finalize_ipc_period(conn, '2025-01-01', '2025-01-31')

    assert result.line_items_created == 2
    assert result.logs_marked == 2

    period = conn.execute('SELECT * FROM ipc_periods').fetchall()
    assert len(period) == 1

    lines = conn.execute('SELECT * FROM ipc_line_items').fetchall()
    assert len(lines) == 2

    statuses = conn.execute('SELECT id, finalized FROM plant_logs ORDER BY id').fetchall()
    assert [row['finalized'] for row in statuses] == [1, 1, 0]
