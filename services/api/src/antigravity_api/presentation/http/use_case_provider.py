from antigravity_api.application.agent_catalog import AgentCatalog
from antigravity_api.application.generate_company import GenerateCompany
from antigravity_api.application.get_service_health import GetServiceHealth
from antigravity_api.infrastructure.gemini_generation import GeminiGeneration
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


def provide_generate_company(
    settings: Settings = get_settings(),
) -> GenerateCompany:
    return GenerateCompany(
        ai_generation=GeminiGeneration(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
        )
    )
