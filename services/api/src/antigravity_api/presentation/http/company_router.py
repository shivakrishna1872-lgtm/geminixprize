from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import ValidationError

from antigravity_api.application.generate_company import GenerateCompany
from antigravity_api.presentation.http.auth import require_internal_api_key
from antigravity_api.presentation.http.schemas import (
    CompanyBlueprintResponse,
    GenerateCompanyRequest,
)
from antigravity_api.presentation.http.use_case_provider import provide_generate_company

router = APIRouter(tags=["companies"], dependencies=[Depends(require_internal_api_key)])


@router.post("/companies/generate", response_model=CompanyBlueprintResponse)
async def generate_company(
    request: Request,
    use_case: GenerateCompany = Depends(provide_generate_company),
) -> CompanyBlueprintResponse:
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
        status=blueprint.status,
    )
