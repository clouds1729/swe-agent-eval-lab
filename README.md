# swe-agent-eval-lab

A minimal benchmark harness for evaluating frontier coding agents on realistic software-engineering tasks.

## Design

Each task lives under `tasks/<task_id>/` and includes:

- `prompt.md`: the prompt shown to the coding agent.
- `starter/`: a small, intentionally broken repository/codebase.
- `tests/visible/`: tests that can be shown to the agent.
- `tests/hidden/`: tests used for anti-shortcut evaluation.
- `grader.py`: deterministic grader that copies the starter into a temporary working directory and executes tests.
- `failure_analysis.md`: likely agent shortcuts and how hidden tests detect them.

## Why this resembles coding-agent evaluation

Real coding-agent evaluations generally:

- Use constrained prompts and imperfect starter code.
- Score based on executable outcomes (tests), not natural-language output.
- Include hidden checks to prevent overfitting to visible tests.
- Require deterministic orchestration for reproducible benchmarking.

This repo mirrors that pattern with a simple extensible structure and CLI.

## Requirements

- Python 3.11+
- `pytest`

Install dev dependencies:

```bash
python -m pip install -e .[dev]
```

## CLI

List tasks:

```bash
python -m eval_lab list
```

Run one task:

```bash
python -m eval_lab run sample_reverse_string
```

Run all tasks:

```bash
python -m eval_lab run-all
```

## Grader JSON schema

Each grader returns:

- `task_id`
- `passed`
- `score`
- `visible_tests_passed`
- `hidden_tests_passed`
- `stdout`
- `stderr`
- `duration_seconds`

## Current sample task

- `sample_reverse_string`: fixes a buggy `reverse_string` implementation.
