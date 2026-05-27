from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[bool, str, str]:
    completed = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    return completed.returncode == 0, completed.stdout, completed.stderr


def main() -> None:
    task_dir = Path(__file__).resolve().parent
    starter_dir = task_dir / 'starter'
    visible_tests_dir = task_dir / 'tests' / 'visible'
    hidden_tests_dir = task_dir / 'tests' / 'hidden'

    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='eval-lab-') as tmp_dir:
        workdir = Path(tmp_dir) / 'workspace'
        shutil.copytree(starter_dir, workdir)

        install_ok, install_out, install_err = run(
            [sys.executable, '-m', 'pip', 'install', '-q', '-r', 'requirements.txt'],
            workdir,
        )
        if not install_ok:
            print(json.dumps({'task_id': task_dir.name, 'passed': False, 'score': 0.0, 'visible_tests_passed': False, 'hidden_tests_passed': False, 'stdout': install_out, 'stderr': install_err, 'duration_seconds': round(time.perf_counter() - start, 6)}))
            return

        vis_ok, vis_out, vis_err = run([sys.executable, '-m', 'pytest', str(visible_tests_dir), '-q'], workdir)
        hid_ok, hid_out, hid_err = run([sys.executable, '-m', 'pytest', str(hidden_tests_dir), '-q'], workdir)

    duration = time.perf_counter() - start
    passed = vis_ok and hid_ok
    print(json.dumps({'task_id': task_dir.name, 'passed': passed, 'score': 1.0 if passed else 0.0, 'visible_tests_passed': vis_ok, 'hidden_tests_passed': hid_ok, 'stdout': f'INSTALL\n{install_out}\nVISIBLE TESTS\n{vis_out}\nHIDDEN TESTS\n{hid_out}', 'stderr': f'INSTALL\n{install_err}\nVISIBLE TESTS\n{vis_err}\nHIDDEN TESTS\n{hid_err}', 'duration_seconds': round(duration, 6)}))


if __name__ == '__main__':
    main()
