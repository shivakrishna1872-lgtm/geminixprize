from antigravity_api.domain.agent_role import AgentRole


class AgentCatalog:
    """Authoritative list of agent roles the orchestration layer will support."""

    def list_roles(self) -> tuple[AgentRole, ...]:
        return (
            AgentRole.CEO,
            AgentRole.RESEARCH,
            AgentRole.BRANDING,
            AgentRole.PRODUCT,
            AgentRole.STORE,
            AgentRole.MARKETING,
            AgentRole.SALES,
            AgentRole.FINANCE,
            AgentRole.SUPPORT,
        )
