from dataclasses import dataclass
from typing import Literal


ServiceStatus = Literal["ok", "degraded"]
RuntimeEnvironment = Literal["development", "test", "production"]


@dataclass(frozen=True)
class ServiceHealth:
    service: Literal["antigravity-api"]
    status: ServiceStatus
    version: str
    environment: RuntimeEnvironment
    capabilities: tuple[str, ...]
