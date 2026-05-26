from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class GradeResult:
    task_id: str
    passed: bool
    score: float
    visible_tests_passed: bool
    hidden_tests_passed: bool
    stdout: str
    stderr: str
    duration_seconds: float

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)
