"""
main.py — FastAPI application for the AntiGravity Orchestrator.

Endpoints
─────────
POST  /api/launch               — Accept a LaunchRequest, start orchestration
GET   /api/stream/{business_id} — SSE stream of live agent events
GET   /api/business/{business_id} — Current business state snapshot
GET   /health                   — Liveness probe
"""

import asyncio
import json
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator

import uvicorn
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# ---------------------------------------------------------------------------
# Resolve shared / local imports regardless of CWD
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", ".."))   # for shared.*
sys.path.insert(0, _HERE)                              # for event_bus, orchestrator

from shared.types.models import (
    Business,
    BusinessStatus,
    EventType,
    LaunchRequest,
    LaunchResponse,
)
import orchestrator as _orch_module  # import module so we share ACTIVE_BUSINESSES
from orchestrator import orchestrate_business, ACTIVE_BUSINESSES
from event_bus import emit_event, tail_events, get_event_file

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — nothing to set up/tear down yet."""
    yield


app = FastAPI(
    title="AntiGravity Orchestrator",
    version="1.0.0",
    description="Backend orchestrator that drives the AntiGravity multi-agent pipeline.",
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────────────────────
# Allow all origins in development; tighten in production via env var.
_ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health", tags=["Meta"])
async def health() -> dict:
    """Liveness probe."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.post("/api/launch", response_model=LaunchResponse, tags=["Orchestration"])
async def launch(request: LaunchRequest, background_tasks: BackgroundTasks) -> LaunchResponse:
    """
    Accept a business prompt, create a Business object, persist it to
    ACTIVE_BUSINESSES, and kick off the orchestration pipeline as a
    non-blocking background task.
    """
    # Create the business record
    business = Business(
        user_id=request.user_id,
        prompt=request.prompt,
        status=BusinessStatus.QUEUED,
    )
    ACTIVE_BUSINESSES[business.id] = business

    # Emit a queued event so the SSE stream has something to read immediately
    emit_event(
        business.id,
        {
            "type": EventType.BUSINESS_CREATED.value,
            "business_id": business.id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": "Business queued for launch",
        },
    )

    # Start orchestration as a background asyncio Task (non-blocking)
    background_tasks.add_task(_run_orchestration, business)

    stream_url = f"/api/stream/{business.id}"
    return LaunchResponse(
        business_id=business.id,
        stream_url=stream_url,
        message="Business launch initiated",
    )


async def _run_orchestration(business: Business) -> None:
    """
    Thin wrapper that runs orchestrate_business and catches any unhandled
    exceptions so the background task never crashes silently.
    """
    try:
        await orchestrate_business(business)
    except Exception as exc:
        # Mark failed if orchestrator raised outside its own error handling
        biz = ACTIVE_BUSINESSES.get(business.id, business)
        biz.status = BusinessStatus.FAILED
        ACTIVE_BUSINESSES[business.id] = biz
        emit_event(
            business.id,
            {
                "type": EventType.AGENT_ERROR.value,
                "business_id": business.id,
                "error": str(exc),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        )


@app.get("/api/stream/{business_id}", tags=["Streaming"])
async def stream_events(business_id: str) -> StreamingResponse:
    """
    Server-Sent Events endpoint.

    Tails `/tmp/ag_events_{business_id}.jsonl` for new lines and streams each
    line as an SSE data frame.  A heartbeat is sent every 2 seconds while
    waiting for new events so the connection stays alive through proxies and
    load balancers.

    The stream closes automatically when the business reaches status
    ``live`` or ``failed``.
    """
    if business_id not in ACTIVE_BUSINESSES:
        raise HTTPException(status_code=404, detail=f"Business '{business_id}' not found")

    async def event_generator() -> AsyncGenerator[str, None]:
        cursor: int = 0         # next line index to read
        last_heartbeat: float = asyncio.get_event_loop().time()
        terminal_statuses = {BusinessStatus.LIVE, BusinessStatus.FAILED}

        while True:
            # ── Emit any new events ──────────────────────────────────────
            new_events = tail_events(business_id, from_line=cursor)
            for event in new_events:
                cursor += 1
                yield f"data: {json.dumps(event)}\n\n"

            # ── Check terminal state ─────────────────────────────────────
            biz = ACTIVE_BUSINESSES.get(business_id)
            if biz and biz.status in terminal_statuses:
                # Drain any remaining events written just before terminal
                remaining = tail_events(business_id, from_line=cursor)
                for event in remaining:
                    cursor += 1
                    yield f"data: {json.dumps(event)}\n\n"
                # Send a final close event so the client knows to disconnect
                close_payload = json.dumps({
                    "type": "stream_closed",
                    "business_id": business_id,
                    "final_status": biz.status.value,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                })
                yield f"data: {close_payload}\n\n"
                return

            # ── Heartbeat every 2 seconds ────────────────────────────────
            now = asyncio.get_event_loop().time()
            if now - last_heartbeat >= 2.0:
                yield 'data: {"type":"heartbeat"}\n\n'
                last_heartbeat = now

            # ── Yield control so the event loop can do other work ────────
            await asyncio.sleep(0.25)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # Disable nginx buffering
            "Connection": "keep-alive",
        },
    )


@app.get("/api/business/{business_id}", tags=["State"])
async def get_business(business_id: str) -> dict:
    """
    Return a snapshot of the current business state from the in-memory store.
    """
    biz = ACTIVE_BUSINESSES.get(business_id)
    if biz is None:
        raise HTTPException(status_code=404, detail=f"Business '{business_id}' not found")
    return biz.model_dump(mode="json")


# ---------------------------------------------------------------------------
# Dev entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        reload=True,
        log_level="info",
    )
