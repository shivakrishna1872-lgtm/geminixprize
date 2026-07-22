from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from pydantic import SecretStr
from pydantic import ValidationError

from antigravity_api.application.generate_company import GenerateCompany
from antigravity_api.infrastructure.gemini_generation import GeminiGeneration
from antigravity_api.infrastructure.settings import Settings, get_settings
from antigravity_api.presentation.http.auth import require_internal_api_key
from antigravity_api.presentation.http.schemas import (
    CompanyBlueprintResponse,
    GenerateCompanyRequest,
    StorefrontProductResponse,
)

router = APIRouter(tags=["companies"], dependencies=[Depends(require_internal_api_key)])


@router.post("/companies/generate", response_model=CompanyBlueprintResponse)
async def generate_company(
    request: Request,
    x_gemini_api_key: Optional[str] = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> CompanyBlueprintResponse:
    request_scoped_key = SecretStr(x_gemini_api_key) if x_gemini_api_key else settings.gemini_api_key
    use_case = GenerateCompany(
        ai_generation=GeminiGeneration(
            api_key=request_scoped_key,
            model=settings.gemini_model,
        )
    )

    try:
        payload = GenerateCompanyRequest.model_validate(await request.json())
        blueprint = use_case.execute(idea=payload.idea)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    return CompanyBlueprintResponse(
        company_name=blueprint.company_name,
        tagline=blueprint.tagline,
        category=blueprint.category,
        audience=blueprint.audience,
        positioning=blueprint.positioning,
        starter_products=blueprint.starter_products,
        pricing_strategy=blueprint.pricing_strategy,
        storefront_sections=blueprint.storefront_sections,
        marketing_plan=blueprint.marketing_plan,
        launch_checklist=blueprint.launch_checklist,
        agent_log=blueprint.agent_log,
        product_catalog=tuple(
            StorefrontProductResponse(
                name=product.name,
                description=product.description,
                price_usd=product.price_usd,
                inventory_status=product.inventory_status,
                product_angle=product.product_angle,
            )
            for product in blueprint.product_catalog
        ),
        checkout_mode=blueprint.checkout_mode,
        storefront_slug=blueprint.storefront_slug,
        status=blueprint.status,
    )
