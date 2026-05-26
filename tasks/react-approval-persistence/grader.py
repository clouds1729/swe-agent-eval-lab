from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[bool, str, str]:
    completed = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    return completed.returncode == 0, completed.stdout, completed.stderr


def ensure_node_modules(workdir: Path) -> tuple[bool, str, str]:
    return run(["npm", "install", "--no-audit", "--no-fund"], workdir)


def run_tests(test_file: Path, workdir: Path) -> tuple[bool, str, str]:
    return run(["npx", "vitest", "run", str(test_file), "--reporter=dot"], workdir)


def main() -> None:
    task_dir = Path(__file__).resolve().parent
    starter_dir = task_dir / "starter"
    visible_test = task_dir / "tests" / "visible" / "test_approval_visible.test.tsx"
    hidden_test = task_dir / "tests" / "hidden" / "test_approval_hidden.test.tsx"

    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="eval-lab-") as tmp_dir:
        workdir = Path(tmp_dir) / "workspace"
        shutil.copytree(starter_dir, workdir)

        install_ok, install_out, install_err = ensure_node_modules(workdir)
        if not install_ok:
            result = {
                "task_id": task_dir.name,
                "passed": False,
                "score": 0.0,
                "visible_tests_passed": False,
                "hidden_tests_passed": False,
                "stdout": install_out,
                "stderr": install_err,
                "duration_seconds": round(time.perf_counter() - start, 6),
            }
            print(json.dumps(result))
            return

        visible_ok, visible_out, visible_err = run_tests(visible_test, workdir)
        hidden_ok, hidden_out, hidden_err = run_tests(hidden_test, workdir)

    duration = time.perf_counter() - start
    passed = visible_ok and hidden_ok
    print(
        json.dumps(
            {
                "task_id": task_dir.name,
                "passed": passed,
                "score": 1.0 if passed else 0.0,
                "visible_tests_passed": visible_ok,
                "hidden_tests_passed": hidden_ok,
                "stdout": (
                    "INSTALL\n"
                    + install_out
                    + "\nVISIBLE TESTS\n"
                    + visible_out
                    + "\nHIDDEN TESTS\n"
                    + hidden_out
                ),
                "stderr": (
                    "INSTALL\n"
                    + install_err
                    + "\nVISIBLE TESTS\n"
                    + visible_err
                    + "\nHIDDEN TESTS\n"
                    + hidden_err
                ),
                "duration_seconds": round(duration, 6),
            }
        )
    )


if __name__ == "__main__":
    main()
