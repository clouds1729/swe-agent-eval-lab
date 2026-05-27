from __future__ import annotations

import sqlite3
from pathlib import Path


def connect(db_path: str | Path = ':memory:') -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db(conn: sqlite3.Connection, schema_path: str | Path = 'schema.sql') -> None:
    schema = Path(schema_path).read_text()
    conn.executescript(schema)
    conn.commit()
