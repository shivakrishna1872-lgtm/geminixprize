from antigravity_api.application.agent_catalog import AgentCatalog
from antigravity_api.domain.service_health import RuntimeEnvironment, ServiceHealth


class GetServiceHealth:
    def __init__(
        self,
        *,
        version: str,
        environment: RuntimeEnvironment,
        agent_catalog: AgentCatalog,
    ) -> None:
        self._version = version
        self._environment = environment
        self._agent_catalog = agent_catalog

    def execute(self) -> ServiceHealth:
        agent_capabilities = tuple(f"agent:{role.value}" for role in self._agent_catalog.list_roles())
        return ServiceHealth(
            service="antigravity-api",
            status="ok",
            version=self._version,
            environment=self._environment,
            capabilities=(
                "health-check",
                "agent-registry",
                "mcp-connector-boundary",
                "cloud-run-ready",
                *agent_capabilities,
            ),
        )
