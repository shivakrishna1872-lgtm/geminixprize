from pydantic import BaseModel, ConfigDict, Field


class ServiceHealthResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    service: str = Field(pattern="^antigravity-api$")
    status: str
    version: str
    environment: str
    capabilities: tuple[str, ...]
