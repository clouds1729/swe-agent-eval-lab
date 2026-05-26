from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def run_pytest(test_dir: Path, workdir: Path) -> tuple[bool, str, str]:
    command = [sys.executable, "-m", "pytest", str(test_dir), "-q"]
    completed = subprocess.run(command, cwd=workdir, capture_output=True, text=True, check=False)
    return completed.returncode == 0, completed.stdout, completed.stderr


def main() -> None:
    task_dir = Path(__file__).resolve().parent
    starter_dir = task_dir / "starter"
    visible_tests_dir = task_dir / "tests" / "visible"
    hidden_tests_dir = task_dir / "tests" / "hidden"

    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="eval-lab-") as tmp_dir:
        workdir = Path(tmp_dir) / "workspace"
        shutil.copytree(starter_dir, workdir)

        visible_ok, visible_stdout, visible_stderr = run_pytest(visible_tests_dir, workdir)
        hidden_ok, hidden_stdout, hidden_stderr = run_pytest(hidden_tests_dir, workdir)

    duration = time.perf_counter() - start
    passed = visible_ok and hidden_ok
    result = {
        "task_id": task_dir.name,
        "passed": passed,
        "score": 1.0 if passed else 0.0,
        "visible_tests_passed": visible_ok,
        "hidden_tests_passed": hidden_ok,
        "stdout": f"VISIBLE TESTS\n{visible_stdout}\nHIDDEN TESTS\n{hidden_stdout}",
        "stderr": f"VISIBLE TESTS\n{visible_stderr}\nHIDDEN TESTS\n{hidden_stderr}",
        "duration_seconds": round(duration, 6),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
