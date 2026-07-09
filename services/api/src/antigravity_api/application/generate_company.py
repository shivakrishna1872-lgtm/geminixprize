from antigravity_api.application.ai_text_generation import AiTextGeneration
from antigravity_api.domain.company_blueprint import CompanyBlueprint


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
agent_log, status.

Rules:
- Make the company distinct and legally ownable.
- Do not claim that external stores, payments, domains, or supplier products
  were actually provisioned.
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
