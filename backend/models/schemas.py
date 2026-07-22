from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

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

class BrandIdentity(BaseModel):
    name: str
    tagline: str
    primaryColor: str
    secondaryColor: str
    accentColor: str
    fontHeading: str
    fontBody: str
    logoUrl: Optional[str] = None
    styleKeywords: List[str]

class Product(BaseModel):
    id: str
    name: str
    description: str
    priceUsd: float
    imageUrl: Optional[str] = None
    tags: List[str]

class AgentState(BaseModel):
    agentId: AgentId
    name: str
    role: str
    emoji: str
    status: AgentStatus = AgentStatus.IDLE
    currentTask: Optional[str] = None
    progress: int = 0
    logs: List[str] = []

class BusinessBlueprint(BaseModel):
    niche: str
    target_audience: str
    value_proposition: str
    competitors: List[str]
    pricing_strategy: str
    revenue_model: str
    launch_checklist: List[str]

class Business(BaseModel):
    id: str
    prompt: str
    status: str = "queued"
    blueprint: Optional[BusinessBlueprint] = None
    brand: Optional[BrandIdentity] = None
    products: List[Product] = []
    websiteUrl: Optional[str] = None
    agents: Dict[str, AgentState] = {}
    createdAt: str

class LaunchRequest(BaseModel):
    prompt: str

class LaunchResponse(BaseModel):
    business_id: str
    stream_url: str

class AgentEvent(BaseModel):
    businessId: str
    agentId: str
    eventType: EventType
    task: Optional[str] = None
    logLine: Optional[str] = None
    progress: Optional[int] = None
    payload: Optional[Dict[str, Any]] = None
    timestamp: str
