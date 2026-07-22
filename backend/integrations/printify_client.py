"""
Printify API client — abstracted integration layer.
In mock mode (USE_MOCK_INTEGRATIONS=true), returns realistic fake data.
"""

import os
import uuid
import httpx
from typing import Optional

MOCK_MODE = os.environ.get("USE_MOCK_INTEGRATIONS", "true").lower() == "true"
PRINTIFY_API_KEY = os.environ.get("PRINTIFY_API_KEY", "")
PRINTIFY_SHOP_ID = os.environ.get("PRINTIFY_SHOP_ID", "")
BASE_URL = "https://api.printify.com/v1"


class PrintifyClient:
    """
    Abstracted Printify client.
    Supports real API calls and mock mode for development.
    """

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {PRINTIFY_API_KEY}",
            "Content-Type": "application/json",
        }
        self.shop_id = PRINTIFY_SHOP_ID

    async def get_catalog_blueprints(self, query: str = "") -> list[dict]:
        """Fetch product blueprints from Printify catalog."""
        if MOCK_MODE:
            return self._mock_blueprints(query)

        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{BASE_URL}/catalog/blueprints.json",
                headers=self.headers,
            )
            r.raise_for_status()
            blueprints = r.json()
            if query:
                blueprints = [
                    b for b in blueprints
                    if query.lower() in b.get("title", "").lower()
                ]
            return blueprints[:10]

    async def create_product(
        self,
        title: str,
        description: str,
        blueprint_id: int,
        print_provider_id: int,
        variants: list[dict],
        print_areas: list[dict],
    ) -> dict:
        """Create a product in Printify."""
        if MOCK_MODE:
            return self._mock_product(title, description)

        payload = {
            "title": title,
            "description": description,
            "blueprint_id": blueprint_id,
            "print_provider_id": print_provider_id,
            "variants": variants,
            "print_areas": print_areas,
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{BASE_URL}/shops/{self.shop_id}/products.json",
                headers=self.headers,
                json=payload,
            )
            r.raise_for_status()
            return r.json()

    async def publish_product(self, product_id: str) -> dict:
        """Publish a product to the connected store."""
        if MOCK_MODE:
            return {"published": True, "product_id": product_id}

        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{BASE_URL}/shops/{self.shop_id}/products/{product_id}/publish.json",
                headers=self.headers,
                json={"title": True, "description": True, "images": True, "variants": True},
            )
            r.raise_for_status()
            return r.json()

    # -------------------------------------------------------------------------
    # Mock Data
    # -------------------------------------------------------------------------

    def _mock_blueprints(self, query: str) -> list[dict]:
        return [
            {"id": 5, "title": "Unisex Jersey Short Sleeve Tee", "brand": "Bella+Canvas"},
            {"id": 92, "title": "Unisex Heavy Blend Hooded Sweatshirt", "brand": "Gildan"},
            {"id": 77, "title": "White Glossy Mug", "brand": "Orca"},
            {"id": 248, "title": "Premium Tote Bag", "brand": "Econscious"},
            {"id": 371, "title": "Sticker", "brand": "StickerMule"},
        ]

    def _mock_product(self, title: str, description: str) -> dict:
        return {
            "id": f"mock_{uuid.uuid4().hex[:8]}",
            "title": title,
            "description": description,
            "status": "draft",
            "images": [
                {"src": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"}
            ],
            "variants": [
                {"id": 1, "title": "S / Black", "price": 2999},
                {"id": 2, "title": "M / Black", "price": 2999},
                {"id": 3, "title": "L / Black", "price": 2999},
                {"id": 4, "title": "XL / Black", "price": 2999},
            ],
        }
