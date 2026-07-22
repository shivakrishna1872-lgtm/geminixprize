from fastapi import APIRouter, Depends

from antigravity_api.application.get_service_health import GetServiceHealth
from antigravity_api.presentation.http.schemas import ServiceHealthResponse
from antigravity_api.presentation.http.use_case_provider import provide_get_service_health

router = APIRouter(tags=["system"])


@router.get("/health", response_model=ServiceHealthResponse)
def get_health(
    use_case: GetServiceHealth = Depends(provide_get_service_health),
) -> ServiceHealthResponse:
    health = use_case.execute()
    return ServiceHealthResponse(
        service=health.service,
        status=health.status,
        version=health.version,
        environment=health.environment,
        capabilities=health.capabilities,
    )
