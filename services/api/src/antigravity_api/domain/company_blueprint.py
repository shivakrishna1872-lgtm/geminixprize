from dataclasses import dataclass


@dataclass(frozen=True)
class CompanyBlueprint:
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
