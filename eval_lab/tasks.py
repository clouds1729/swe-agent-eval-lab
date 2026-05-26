from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Task:
    task_id: str
    path: Path

    @property
    def prompt_path(self) -> Path:
        return self.path / "prompt.md"

    @property
    def starter_path(self) -> Path:
        return self.path / "starter"

    @property
    def tests_path(self) -> Path:
        return self.path / "tests"

    @property
    def grader_path(self) -> Path:
        return self.path / "grader.py"


class TaskRegistry:
    def __init__(self, tasks_root: Path) -> None:
        self.tasks_root = tasks_root

    def list_tasks(self) -> list[Task]:
        tasks: list[Task] = []
        if not self.tasks_root.exists():
            return tasks

        for entry in sorted(self.tasks_root.iterdir()):
            if entry.is_dir() and (entry / "grader.py").exists():
                tasks.append(Task(task_id=entry.name, path=entry))
        return tasks

    def get(self, task_id: str) -> Task:
        task_path = self.tasks_root / task_id
        if not task_path.exists() or not (task_path / "grader.py").exists():
            raise KeyError(f"Unknown task_id: {task_id}")
        return Task(task_id=task_id, path=task_path)
