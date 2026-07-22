import uuid
import asyncio
import json
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from backend.core.auth import verify_token
from backend.models.schemas import LaunchRequest, LaunchResponse, Business
from backend.orchestrator.event_bus import EventBus
from backend.orchestrator.orchestrator import orchestrate_business

router = APIRouter()

# In-memory store for dev (Firestore in prod)
ACTIVE_BUSINESSES = {}

@router.post("/business/launch", response_model=LaunchResponse)
async def launch_business(
    req: LaunchRequest, 
    background_tasks: BackgroundTasks,
    user: dict = Depends(verify_token)
):
    business_id = f"biz_{uuid.uuid4().hex[:12]}"
    
    business = Business(
        id=business_id,
        prompt=req.prompt,
        status="queued",
        createdAt=datetime.utcnow().isoformat() + "Z"
    )
    ACTIVE_BUSINESSES[business_id] = business
    
    # Start the orchestrator DAG in the background
    background_tasks.add_task(orchestrate_business, business)
    
    return LaunchResponse(
        business_id=business_id,
        stream_url=f"/api/v1/business/{business_id}/stream"
    )

@router.get("/business/{business_id}/stream")
async def stream_business_events(business_id: str):
    if business_id not in ACTIVE_BUSINESSES:
        raise HTTPException(status_code=404, detail="Business not found")

    async def event_generator():
        try:
            # Yield initial state
            yield f"data: {json.dumps({'type': 'connection', 'status': 'connected'})}\n\n"
            
            # Tail the Event Bus
            async for line in EventBus.tail_events(business_id):
                # The line is a JSON string of AgentEvent
                yield f"data: {line}\n\n"
                
                # Check for termination events
                event_dict = json.loads(line)
                if event_dict.get("eventType") in ["business_live", "business_failed"]:
                    break
        except asyncio.CancelledError:
            pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.get("/business/{business_id}", response_model=Business)
async def get_business(business_id: str, user: dict = Depends(verify_token)):
    if business_id not in ACTIVE_BUSINESSES:
        raise HTTPException(status_code=404, detail="Business not found")
    return ACTIVE_BUSINESSES[business_id]
