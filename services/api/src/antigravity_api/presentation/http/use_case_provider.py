from antigravity_api.application.agent_catalog import AgentCatalog
from antigravity_api.application.get_service_health import GetServiceHealth
from antigravity_api.infrastructure.settings import Settings, get_settings


def provide_agent_catalog() -> AgentCatalog:
    return AgentCatalog()


def provide_get_service_health(
    settings: Settings = get_settings(),
) -> GetServiceHealth:
    return GetServiceHealth(
        version=settings.version,
        environment=settings.environment,
        agent_catalog=provide_agent_catalog(),
    )
