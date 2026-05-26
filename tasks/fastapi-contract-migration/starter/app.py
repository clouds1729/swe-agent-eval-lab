from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class AskRequest(BaseModel):
    fen: str


def local_model_answer(fen: str) -> str:
    if os.getenv("LOCAL_MODEL_AVAILABLE", "1") != "1":
        raise RuntimeError("local model is unavailable")
    return f"best move for {fen}: e2e4"


def count_legal_moves(fen: str) -> int:
    parts = fen.strip().split(" ")
    if len(parts) < 2:
        return 0
    return 20 if parts[1] in {"w", "b"} else 0


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask")
def ask(payload: AskRequest) -> dict[str, object]:
    fen = payload.fen
    # intentionally weak: accepts many malformed values
    if len(fen) < 3:
        raise HTTPException(status_code=400, detail="fen is too short")

    answer = local_model_answer(fen)
    moves = count_legal_moves(fen)

    # intentionally inconsistent response shape
    if moves > 0:
        return {
            "answer": answer,
            "metadata": {
                "model_available": True,
                "legal_moves_count": moves,
            },
        }

    return {
        "result": answer,
        "legal_moves": moves,
    }
