from pydantic import BaseModel, ConfigDict, Field


class ServiceHealthResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    service: str = Field(pattern="^antigravity-api$")
    status: str
    version: str
    environment: str
    capabilities: tuple[str, ...]


class GenerateCompanyRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    idea: str = Field(min_length=8, max_length=800)


class CompanyBlueprintResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    company_name: str
    tagline: str
    category: str
    audience: str
    positioning: str
    starter_products: tuple[str, ...]
    pricing_strategy: str
    storefront_sections: tuple[str, ...]
    marketing_plan: tuple[str, ...]
    launch_checklist: tuple[str, ...]
    agent_log: tuple[str, ...]
    status: str
