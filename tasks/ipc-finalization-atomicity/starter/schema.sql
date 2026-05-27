CREATE TABLE IF NOT EXISTS plant_logs (
    id INTEGER PRIMARY KEY,
    work_date TEXT NOT NULL,
    description TEXT NOT NULL,
    units REAL NOT NULL,
    rate REAL,
    finalized INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS ipc_periods (
    id INTEGER PRIMARY KEY,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(start_date, end_date)
);

CREATE TABLE IF NOT EXISTS ipc_line_items (
    id INTEGER PRIMARY KEY,
    period_id INTEGER NOT NULL,
    plant_log_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY(period_id) REFERENCES ipc_periods(id) ON DELETE CASCADE,
    FOREIGN KEY(plant_log_id) REFERENCES plant_logs(id)
);
