import asyncio
import logging

logger = logging.getLogger(__name__)

class MockStripeService:
    @staticmethod
    async def create_payment_link(product_name: str, price: float) -> str:
        await asyncio.sleep(1)
        return f"https://buy.stripe.com/mock_{product_name.lower().replace(' ', '')}"

class MockDudaService:
    @staticmethod
    async def generate_website(brand_name: str, colors: list) -> str:
        await asyncio.sleep(2)
        return f"https://{brand_name.lower().replace(' ', '')}.duda.mock"

class MockPrintifyService:
    @staticmethod
    async def create_product(design_url: str, product_type: str) -> str:
        await asyncio.sleep(1.5)
        return f"mock_printify_{product_type}"

class MockCommerceLayerService:
    @staticmethod
    async def setup_inventory(products: list) -> bool:
        await asyncio.sleep(1)
        return True
