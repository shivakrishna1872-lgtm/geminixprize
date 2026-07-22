"""
Shared data models for the AntiGravity platform.
Used by the orchestrator, agents, and integrations.
"""

from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AgentId(str, Enum):
    ATLAS = "atlas"
    NOVA = "nova"
    FORGE = "forge"
    PULSE = "pulse"
    ORBIT = "orbit"
    VAULT = "vault"
    ECHO = "echo"
    INSIGHT = "insight"


class AgentStatus(str, Enum):
    IDLE = "idle"
    THINKING = "thinking"
    WORKING = "working"
    DONE = "done"
    ERROR = "error"


class BusinessStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    LIVE = "live"
    FAILED = "failed"


class EventType(str, Enum):
    AGENT_STARTED = "agent_started"
    AGENT_THINKING = "agent_thinking"
    AGENT_LOG = "agent_log"
    AGENT_DONE = "agent_done"
    AGENT_ERROR = "agent_error"
    BUSINESS_CREATED = "business_created"
    BUSINESS_LIVE = "business_live"
    PRODUCT_CREATED = "product_created"
    WEBSITE_UPDATED = "website_updated"
    PAYMENT_CONFIGURED = "payment_configured"


# ---------------------------------------------------------------------------
# Core Models
# ---------------------------------------------------------------------------

class BrandIdentity(BaseModel):
    name: str
    tagline: str
    primary_color: str  # hex
    secondary_color: str  # hex
    accent_color: str  # hex
    background_color: str = "#0A0A0F"
    font_heading: str
    font_body: str
    logo_url: Optional[str] = None
    style_keywords: list[str] = []


class BusinessBlueprint(BaseModel):
    niche: str
    target_audience: str
    value_proposition: str
    competitors: list[str] = []
    pricing_strategy: str
    revenue_model: str
    launch_checklist: list[str] = []


class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    printify_id: Optional[str] = None
    name: str
    description: str
    price_usd: float
    image_url: Optional[str] = None
    tags: list[str] = []
    variants: list[dict] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AgentState(BaseModel):
    agent_id: AgentId
    status: AgentStatus = AgentStatus.IDLE
    current_task: Optional[str] = None
    progress: int = 0  # 0–100
    logs: list[str] = []
    result: Optional[dict] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Business(BaseModel):
    id: str = Field(default_factory=lambda: f"biz_{uuid.uuid4().hex[:8]}")
    user_id: str
    prompt: str
    status: BusinessStatus = BusinessStatus.QUEUED
    brand: Optional[BrandIdentity] = None
    blueprint: Optional[BusinessBlueprint] = None
    products: list[Product] = []
    website_url: Optional[str] = None
    stripe_account_id: Optional[str] = None
    agents: dict[str, AgentState] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    launched_at: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Pub/Sub Event Schema
# ---------------------------------------------------------------------------

class AgentEvent(BaseModel):
    business_id: str
    agent_id: AgentId
    event_type: EventType
    task: Optional[str] = None
    log_line: Optional[str] = None
    progress: Optional[int] = None
    payload: Optional[dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# API Request/Response
# ---------------------------------------------------------------------------

class LaunchRequest(BaseModel):
    prompt: str
    user_id: str = "anonymous"


class LaunchResponse(BaseModel):
    business_id: str
    stream_url: str
    message: str = "Business launch initiated"
