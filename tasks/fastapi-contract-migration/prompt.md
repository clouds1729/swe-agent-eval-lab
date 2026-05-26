Your task is to migrate a FastAPI backend contract for frontend compatibility while preserving documented behavior.

The app exposes `/health` and `/ask`.

A new frontend expects `/ask` responses to always have this shape:

```json
{
  "answer": "...",
  "metadata": {
    "model_available": true,
    "legal_moves_count": 20
  }
}
```

Current issues in the starter:

1. Inconsistent JSON response shape across different branches.
2. Missing local model causes unhandled failures and 500 errors.
3. Weak validation for malformed FEN-like input.

Requirements:

- Keep `/health` working.
- Update `/ask` so responses are consistent and include both `answer` and `metadata`.
- For malformed input, return either FastAPI validation 422 or a controlled 400.
- If model is unavailable, return 503 with a stable JSON response shape.
- Do not leak raw exception traces to API consumers.
- Preserve backward-compatible behavior where already documented by tests.
