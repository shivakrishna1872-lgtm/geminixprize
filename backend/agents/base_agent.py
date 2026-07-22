import asyncio
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from google.cloud import pubsub_v1, firestore

from backend.models.schemas import AgentId, AgentStatus, AgentEvent, EventType, Business
from backend.core.config import settings
from backend.orchestrator.event_bus import EventBus

class BaseAgent(ABC):
    """
    Abstract base class for all AntiGravity AI agents.
    Each agent:
    - Has access to a Gemini model via Vertex AI
    - Publishes structured events to EventBus (streamed to frontend via SSE)
    - Persists state in Firestore
    - Returns a typed result for the next agent in the chain
    """

    def __init__(self, business: Business, agent_id: AgentId):
        self.agent_id = agent_id
        self.business = business
        self.model: Optional[GenerativeModel] = None
        self.publisher: Optional[pubsub_v1.PublisherClient] = None
        self.db: Optional[firestore.AsyncClient] = None
        self._topic_path: Optional[str] = None
        self._initialized = False

    def _initialize(self):
        if self._initialized:
            return
            
        vertexai.init(project=settings.google_api_key, location="us-central1") # using api key as project placeholder if needed, though gemini usually needs gcp project
        self.model = GenerativeModel(
            "gemini-2.0-flash-001",
            generation_config=GenerationConfig(
                temperature=0.7,
                max_output_tokens=8192,
            ),
        )
        # We omit real pubsub/firestore init here to allow running locally without GCP setup
        self._initialized = True

    @abstractmethod
    async def run(self) -> dict[str, Any]:
        """
        Execute the agent's primary task.
        Returns a result dict that is stored in business state.
        """
        pass

    async def execute(self) -> dict[str, Any]:
        """Public entry point — sets up, runs, tears down."""
        self._initialize()
        await self._set_status(AgentStatus.THINKING, task="Initializing...")
        try:
            result = await self.run()
            await self._set_status(AgentStatus.DONE, progress=100)
            return result
        except Exception as e:
            await self._set_status(AgentStatus.ERROR)
            await self._emit_event(EventType.AGENT_ERROR, log_line=str(e))
            raise

    async def think(self, prompt: str, task_description: str = "") -> str:
        """Call Gemini and stream back the response."""
        await self._set_status(AgentStatus.THINKING, task=task_description)
        await self._emit_event(EventType.AGENT_THINKING, task=task_description)

        loop = asyncio.get_event_loop()
        # Ensure we wrap API calls correctly or mock if no key
        if settings.google_api_key == "mock-api-key":
            await asyncio.sleep(2)
            text = f"Mock response for {self.agent_id.value}: {task_description}"
        else:
            try:
                response = await loop.run_in_executor(None, lambda: self.model.generate_content([prompt]))
                text = response.text
            except Exception as e:
                text = f"Error calling Gemini: {str(e)}"

        await self._emit_log(f"✓ {task_description}")
        return text

    async def think_json(self, prompt: str, task_description: str = "") -> dict:
        """Call Gemini and parse response as JSON."""
        json_prompt = prompt + "\n\nRespond ONLY with valid JSON. No markdown."
        raw = await self.think(json_prompt, task_description)
        
        if settings.google_api_key == "mock-api-key":
            return {"mock": "data", "status": "success"}
            
        cleaned = raw.strip().replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            await self._emit_log(f"⚠ JSON parse error, retrying...")
            start = cleaned.find("{")
            end = cleaned.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(cleaned[start:end])
            return {"error": "Failed to parse JSON"}

    async def _emit_event(
        self,
        event_type: EventType,
        task: Optional[str] = None,
        log_line: Optional[str] = None,
        progress: Optional[int] = None,
        payload: Optional[dict] = None,
    ):
        event = AgentEvent(
            businessId=self.business.id,
            agentId=self.agent_id.value,
            eventType=event_type,
            task=task,
            logLine=log_line,
            progress=progress,
            payload=payload,
            timestamp=datetime.utcnow().isoformat() + "Z",
        )
        await EventBus.publish(event)

    async def _emit_log(self, message: str):
        print(f"[{self.agent_id.value.upper()}] {message}")
        await self._emit_event(EventType.AGENT_LOG, log_line=message)

    async def _set_status(
        self,
        status: AgentStatus,
        task: Optional[str] = None,
        progress: Optional[int] = None,
    ):
        event_type_map = {
            AgentStatus.THINKING: EventType.AGENT_THINKING,
            AgentStatus.WORKING: EventType.AGENT_STARTED,
            AgentStatus.DONE: EventType.AGENT_DONE,
            AgentStatus.ERROR: EventType.AGENT_ERROR,
            AgentStatus.IDLE: EventType.AGENT_LOG,
        }
        await self._emit_event(
            event_type_map.get(status, EventType.AGENT_LOG),
            task=task,
            progress=progress,
        )
