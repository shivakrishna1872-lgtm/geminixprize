"""
Duda MCP client — website builder integration.
Creates and manages Duda sites programmatically.
Mock mode returns a realistic preview URL.
"""

import os
import uuid
import httpx

MOCK_MODE = os.environ.get("USE_MOCK_INTEGRATIONS", "true").lower() == "true"
DUDA_API_KEY = os.environ.get("DUDA_API_KEY", "")
DUDA_API_SECRET = os.environ.get("DUDA_API_SECRET", "")
DUDA_BASE_URL = "https://api.duda.co/api"


class DudaMCPClient:
    """
    Abstracted Duda website builder client.
    """

    def __init__(self):
        self.auth = (DUDA_API_KEY, DUDA_API_SECRET) if DUDA_API_KEY else None

    async def create_site(
        self,
        template_id: str,
        default_domain_prefix: str,
        lang: str = "en",
    ) -> dict:
        """Create a new Duda site from a template."""
        if MOCK_MODE:
            site_name = f"{default_domain_prefix}-{uuid.uuid4().hex[:6]}"
            return {
                "site_name": site_name,
                "preview_site_url": f"https://preview.antigravity.store/{site_name}",
                "site_domain": f"{default_domain_prefix}.antigravity.store",
                "account_name": "antigravity",
                "first_published_date": None,
                "last_published_date": None,
            }

        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{DUDA_BASE_URL}/sites/multiscreen/create",
                auth=self.auth,
                json={"template_id": template_id, "default_domain_prefix": default_domain_prefix, "lang": lang},
            )
            r.raise_for_status()
            return r.json()

    async def update_site_theme(self, site_name: str, colors: dict) -> dict:
        """Apply brand colors to a Duda site."""
        if MOCK_MODE:
            return {"updated": True, "site_name": site_name}

        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{DUDA_BASE_URL}/sites/multiscreen/{site_name}/content/color",
                auth=self.auth,
                json=colors,
            )
            r.raise_for_status()
            return r.json()

    async def publish_site(self, site_name: str) -> dict:
        """Publish a Duda site to its live URL."""
        if MOCK_MODE:
            return {
                "published": True,
                "site_name": site_name,
                "site_url": f"https://{site_name}.antigravity.store",
            }

        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{DUDA_BASE_URL}/sites/multiscreen/{site_name}/publish",
                auth=self.auth,
            )
            r.raise_for_status()
            return {"published": True, "site_name": site_name}

    async def get_site_url(self, site_name: str) -> str:
        """Get the live URL of a published site."""
        if MOCK_MODE:
            return f"https://{site_name}.antigravity.store"
        return f"https://{site_name}.multiscreensite.com"
