from __future__ import annotations

import argparse
import json
from pathlib import Path

from eval_lab.runner import run_all, run_task
from eval_lab.tasks import TaskRegistry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eval_lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available task IDs")

    run_parser = subparsers.add_parser("run", help="Run one task")
    run_parser.add_argument("task_id", help="Task identifier")

    subparsers.add_parser("run-all", help="Run all tasks")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    tasks_root = Path(__file__).resolve().parent.parent / "tasks"
    registry = TaskRegistry(tasks_root)

    if args.command == "list":
        for task in registry.list_tasks():
            print(task.task_id)
        return

    if args.command == "run":
        task = registry.get(args.task_id)
        print(json.dumps(run_task(task), indent=2))
        return

    if args.command == "run-all":
        results = run_all(tasks_root)
        print(json.dumps(results, indent=2))
        return

    parser.error("Unknown command")


if __name__ == "__main__":
    main()
