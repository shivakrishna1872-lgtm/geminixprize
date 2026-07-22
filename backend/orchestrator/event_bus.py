import json
import asyncio
from pathlib import Path
from typing import AsyncGenerator
from backend.models.schemas import AgentEvent

EVENT_LOGS_DIR = Path("/tmp/ag_events")
EVENT_LOGS_DIR.mkdir(parents=True, exist_ok=True)

class EventBus:
    @staticmethod
    def _get_file_path(business_id: str) -> Path:
        return EVENT_LOGS_DIR / f"{business_id}.jsonl"

    @staticmethod
    async def publish(event: AgentEvent):
        """Publish an event to the local JSONL file."""
        file_path = EventBus._get_file_path(event.businessId)
        with open(file_path, "a") as f:
            f.write(event.model_dump_json() + "\n")

    @staticmethod
    async def tail_events(business_id: str) -> AsyncGenerator[str, None]:
        """Tails the JSONL file and yields new lines as they are written."""
        file_path = EventBus._get_file_path(business_id)
        
        # Wait for file to exist
        while not file_path.exists():
            await asyncio.sleep(0.5)

        with open(file_path, "r") as f:
            while True:
                line = f.readline()
                if line:
                    yield line.strip()
                else:
                    await asyncio.sleep(0.5)
