from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from eval_lab.tasks import Task, TaskRegistry


def run_task(task: Task, *, python_executable: str = sys.executable) -> dict[str, object]:
    completed = subprocess.run(
        [python_executable, str(task.grader_path)],
        cwd=task.path,
        capture_output=True,
        text=True,
        check=False,
    )

    if completed.returncode != 0:
        return {
            "task_id": task.task_id,
            "passed": False,
            "score": 0.0,
            "visible_tests_passed": False,
            "hidden_tests_passed": False,
            "stdout": completed.stdout,
            "stderr": completed.stderr or f"Grader exited with {completed.returncode}",
            "duration_seconds": 0.0,
        }

    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {
            "task_id": task.task_id,
            "passed": False,
            "score": 0.0,
            "visible_tests_passed": False,
            "hidden_tests_passed": False,
            "stdout": completed.stdout,
            "stderr": f"Invalid grader output: {exc}",
            "duration_seconds": 0.0,
        }


def run_all(tasks_root: Path) -> list[dict[str, object]]:
    registry = TaskRegistry(tasks_root)
    return [run_task(task) for task in registry.list_tasks()]
