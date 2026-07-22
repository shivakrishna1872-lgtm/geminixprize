from fastapi import Header, HTTPException, status

from antigravity_api.infrastructure.settings import Settings, get_settings


def require_internal_api_key(
    x_antigravity_api_key: str = Header(default=""),
    settings: Settings = get_settings(),
) -> None:
    expected = settings.internal_api_key.get_secret_value()
    if not x_antigravity_api_key or x_antigravity_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid MadeThis API key.",
        )
