from antigravity_api.application.ai_text_generation import AiTextGeneration
import re

from antigravity_api.domain.company_blueprint import CompanyBlueprint, StorefrontProduct


class GenerateCompany:
    def __init__(self, *, ai_generation: AiTextGeneration) -> None:
        self._ai_generation = ai_generation

    def execute(self, *, idea: str) -> CompanyBlueprint:
        cleaned_idea = idea.strip()
        if len(cleaned_idea) < 8:
            raise ValueError("Business idea must be at least 8 characters.")

        prompt = _build_company_prompt(cleaned_idea)
        raw_blueprint = self._ai_generation.generate_json(prompt=prompt)

        return CompanyBlueprint(
            company_name=_as_text(raw_blueprint.get("company_name"), "Signal Bottle Co."),
            tagline=_as_text(raw_blueprint.get("tagline"), "Hydration engineered for modern momentum."),
            category=_as_text(raw_blueprint.get("category"), "Premium hydration"),
            audience=_as_text(raw_blueprint.get("audience"), "Active professionals and commuters"),
            positioning=_as_text(
                raw_blueprint.get("positioning"),
                "A design-led water bottle company built around durability, daily carry, and clean brand storytelling.",
            ),
            starter_products=_as_text_tuple(
                raw_blueprint.get("starter_products"),
                ("Insulated everyday bottle", "Filtered travel bottle", "Modular bottle sling"),
            ),
            pricing_strategy=_as_text(
                raw_blueprint.get("pricing_strategy"),
                "Launch with a $39 hero bottle and $59 premium bundle to validate demand before expanding variants.",
            ),
            storefront_sections=_as_text_tuple(
                raw_blueprint.get("storefront_sections"),
                ("Hero offer", "Product benefits", "Material story", "Reviews", "FAQ"),
            ),
            marketing_plan=_as_text_tuple(
                raw_blueprint.get("marketing_plan"),
                ("SEO launch page", "Founder story email", "Short-form product demos"),
            ),
            launch_checklist=_as_text_tuple(
                raw_blueprint.get("launch_checklist"),
                ("Validate supplier costs", "Finalize brand identity", "Publish storefront preview"),
            ),
            agent_log=_as_text_tuple(
                raw_blueprint.get("agent_log"),
                (
                    "CEO agent converted the prompt into a staged operating plan.",
                    "Research agent identified initial market and audience assumptions.",
                    "Store agent prepared a storefront structure for review.",
                ),
            ),
            product_catalog=_as_product_tuple(
                raw_blueprint.get("product_catalog"),
                (
                    StorefrontProduct(
                        name="Signal One Insulated Bottle",
                        description="A stainless-steel daily bottle with a soft-touch finish, leakproof lid, and 24-hour cold retention.",
                        price_usd=39.0,
                        inventory_status="product_discovered_supplier_required",
                        product_angle="Hero everyday hydration product for commuters, gym bags, and work desks.",
                    ),
                    StorefrontProduct(
                        name="Signal Filtered Travel Bottle",
                        description="A premium travel bottle concept with a replaceable filter cartridge and carry loop for city movement.",
                        price_usd=49.0,
                        inventory_status="product_discovered_supplier_required",
                        product_angle="Upsell product for travelers who care about taste and portability.",
                    ),
                    StorefrontProduct(
                        name="Signal Launch Bundle",
                        description="A starter kit pairing the hero bottle with a sling and cleaning brush for a complete launch offer.",
                        price_usd=69.0,
                        inventory_status="bundle_ready_for_provider_mapping",
                        product_angle="Bundle offer designed to raise average order value during launch.",
                    ),
                ),
            ),
            checkout_mode=_as_text(raw_blueprint.get("checkout_mode"), "local_test"),
            storefront_slug=_slugify(_as_text(raw_blueprint.get("company_name"), "Signal Bottle Co.")),
            status=_as_text(raw_blueprint.get("status"), "draft_ready"),
        )


def _build_company_prompt(idea: str) -> str:
    return f"""
You are MadeThis, an autonomous AI company builder for the Google Gemini XPRIZE.
Create a production-ready company blueprint for this founder prompt:

{idea}

Return only valid JSON with these keys:
company_name, tagline, category, audience, positioning, starter_products,
pricing_strategy, storefront_sections, marketing_plan, launch_checklist,
agent_log, product_catalog, checkout_mode, storefront_slug, status.

Rules:
- Make the company distinct and legally ownable.
- Do not claim that external stores, payments, domains, or supplier products
  were actually provisioned.
- product_catalog must contain exactly 3 products. Each product must include
  name, description, price_usd, inventory_status, and product_angle.
- checkout_mode must be "local_test" unless payment provider credentials are provided.
- starter_products, storefront_sections, marketing_plan, launch_checklist,
  and agent_log must be arrays of concise strings.
- status should be "draft_ready" unless something is unsafe.
"""


def _as_text(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def _as_text_tuple(value: object, fallback: tuple[str, ...]) -> tuple[str, ...]:
    if isinstance(value, list):
        cleaned = tuple(item.strip() for item in value if isinstance(item, str) and item.strip())
        if cleaned:
            return cleaned
    return fallback


def _as_product_tuple(
    value: object,
    fallback: tuple[StorefrontProduct, ...],
) -> tuple[StorefrontProduct, ...]:
    if not isinstance(value, list):
        return fallback

    products: list[StorefrontProduct] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        products.append(
            StorefrontProduct(
                name=_as_text(item.get("name"), "Launch Product"),
                description=_as_text(item.get("description"), "A launch-ready product concept."),
                price_usd=_as_price(item.get("price_usd"), 39.0),
                inventory_status=_as_text(
                    item.get("inventory_status"),
                    "product_discovered_supplier_required",
                ),
                product_angle=_as_text(
                    item.get("product_angle"),
                    "Designed as a high-converting launch product.",
                ),
            )
        )

    return tuple(products[:3]) if products else fallback


def _as_price(value: object, fallback: float) -> float:
    if isinstance(value, (int, float)) and value > 0:
        return float(value)
    if isinstance(value, str):
        try:
            parsed = float(value.replace("$", "").strip())
        except ValueError:
            return fallback
        return parsed if parsed > 0 else fallback
    return fallback


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "generated-storefront"
