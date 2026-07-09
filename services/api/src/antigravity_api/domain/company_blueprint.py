from dataclasses import dataclass


@dataclass(frozen=True)
class StorefrontProduct:
    name: str
    description: str
    price_usd: float
    inventory_status: str
    product_angle: str


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
    product_catalog: tuple[StorefrontProduct, ...]
    checkout_mode: str
    storefront_slug: str
    status: str
