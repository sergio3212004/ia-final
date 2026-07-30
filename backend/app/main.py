from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from .engine import GeneticConfig, GeneticEngine
from .schemas import RunCommandResponse, RunCreate


RunStatus = Literal["paused", "running", "completed", "stopped", "failed"]


@dataclass
class RunSession:
    engine: GeneticEngine
    status: RunStatus = "paused"


app = FastAPI(title="OptiLab API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

runs: dict[str, RunSession] = {}


def get_session(run_id: str) -> RunSession:
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Ejecución no encontrada.")
    return runs[run_id]


def response(run_id: str, session: RunSession) -> RunCommandResponse:
    snapshot = session.engine.snapshot()
    snapshot["events"] = session.engine.events
    return RunCommandResponse(run_id=run_id, status=session.status, snapshot=snapshot)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "optilab-api"}


@app.post("/api/runs", response_model=RunCommandResponse, status_code=201)
async def create_run(payload: RunCreate) -> RunCommandResponse:
    config = GeneticConfig(**payload.model_dump(exclude={"auto_run"}))
    engine = GeneticEngine(config)
    run_id = f"AG-{uuid4().hex[:8].upper()}"
    session = RunSession(engine=engine)
    runs[run_id] = session
    if payload.auto_run:
        session.status = "running"
        engine.run()
        session.status = "completed"
    return response(run_id, session)


@app.get("/api/runs/{run_id}", response_model=RunCommandResponse)
async def get_run(run_id: str) -> RunCommandResponse:
    return response(run_id, get_session(run_id))


@app.post("/api/runs/{run_id}/step", response_model=RunCommandResponse)
async def step_run(run_id: str) -> RunCommandResponse:
    session = get_session(run_id)
    if session.status == "stopped":
        raise HTTPException(status_code=409, detail="La ejecución fue detenida.")
    session.engine.step()
    session.status = "completed" if session.engine.generation >= session.engine.config.generations else "paused"
    return response(run_id, session)


@app.post("/api/runs/{run_id}/run", response_model=RunCommandResponse)
async def complete_run(run_id: str) -> RunCommandResponse:
    session = get_session(run_id)
    if session.status == "stopped":
        raise HTTPException(status_code=409, detail="La ejecución fue detenida.")
    session.status = "running"
    session.engine.run()
    session.status = "completed"
    return response(run_id, session)


@app.post("/api/runs/{run_id}/pause", response_model=RunCommandResponse)
async def pause_run(run_id: str) -> RunCommandResponse:
    session = get_session(run_id)
    if session.status not in ("completed", "stopped"):
        session.status = "paused"
    return response(run_id, session)


@app.post("/api/runs/{run_id}/stop", response_model=RunCommandResponse)
async def stop_run(run_id: str) -> RunCommandResponse:
    session = get_session(run_id)
    session.status = "stopped"
    return response(run_id, session)


@app.get("/api/runs/{run_id}/events")
async def stream_events(run_id: str) -> StreamingResponse:
    session = get_session(run_id)

    async def generate():
        cursor = 0
        while True:
            while cursor < len(session.engine.events):
                event = session.engine.events[cursor] | {"run_id": run_id}
                yield f"id: {event['event_id']}\nevent: algorithm\ndata: {json.dumps(event)}\n\n"
                cursor += 1
            if session.status in ("completed", "stopped", "failed"):
                yield f"event: end\ndata: {json.dumps({'run_id': run_id, 'status': session.status})}\n\n"
                return
            yield ": keep-alive\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(generate(), media_type="text/event-stream")
