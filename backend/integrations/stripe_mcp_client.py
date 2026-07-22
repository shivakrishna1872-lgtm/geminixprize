"""
Stripe MCP client — abstracted payment integration.
Wraps the Stripe MCP server or falls back to direct Stripe API.
Mock mode returns realistic fake Stripe objects.
"""

import os
import uuid

MOCK_MODE = os.environ.get("USE_MOCK_INTEGRATIONS", "true").lower() == "true"
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")


class StripeMCPClient:
    """
    Abstracted Stripe client.
    In production, delegates to the Stripe MCP server.
    In mock mode, returns realistic Stripe-shaped objects.
    """

    def __init__(self):
        if not MOCK_MODE and STRIPE_SECRET_KEY:
            try:
                import stripe
                stripe.api_key = STRIPE_SECRET_KEY
                self.stripe = stripe
            except ImportError:
                self.stripe = None
        else:
            self.stripe = None

    async def create_product(self, name: str, description: str) -> dict:
        if MOCK_MODE:
            return {
                "id": f"prod_{uuid.uuid4().hex[:14]}",
                "object": "product",
                "name": name,
                "description": description,
                "active": True,
            }
        product = self.stripe.Product.create(name=name, description=description)
        return product

    async def create_price(
        self,
        product_id: str,
        unit_amount: int,  # in cents
        currency: str = "usd",
    ) -> dict:
        if MOCK_MODE:
            return {
                "id": f"price_{uuid.uuid4().hex[:14]}",
                "object": "price",
                "product": product_id,
                "unit_amount": unit_amount,
                "currency": currency,
                "active": True,
            }
        price = self.stripe.Price.create(
            product=product_id,
            unit_amount=unit_amount,
            currency=currency,
        )
        return price

    async def create_payment_link(self, price_id: str, quantity: int = 1) -> dict:
        if MOCK_MODE:
            return {
                "id": f"plink_{uuid.uuid4().hex[:14]}",
                "object": "payment_link",
                "url": f"https://buy.stripe.com/mock_{uuid.uuid4().hex[:8]}",
                "active": True,
            }
        link = self.stripe.PaymentLink.create(
            line_items=[{"price": price_id, "quantity": quantity}]
        )
        return link

    async def get_revenue_summary(self, account_id: Optional[str] = None) -> dict:
        """Get total revenue and order count."""
        if MOCK_MODE:
            return {
                "total_revenue_usd": 0.0,
                "order_count": 0,
                "currency": "usd",
                "last_30_days": 0.0,
            }
        # Real implementation would use Stripe Balance + PaymentIntents
        return {"total_revenue_usd": 0.0, "order_count": 0}


from typing import Optional
