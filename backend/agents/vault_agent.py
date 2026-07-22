import os
import sys
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.models.schemas import AgentId, AgentStatus, Business
from .base_agent import BaseAgent

class VaultAgent(BaseAgent):
    def __init__(self, business: Business):
        super().__init__(AgentId.VAULT, business)

    async def run(self) -> dict:
        await self._set_status(AgentStatus.WORKING, task="Configuring payment infrastructure...", progress=30)
        
        blueprint = self.business.blueprint
        if not blueprint:
            raise ValueError("VaultAgent requires a BusinessBlueprint to proceed.")
            
        await self._emit_log("Setting product prices...")
        
        prompt = f"""
        You are Vault, a finance and payments specialist.
        Business Niche: {blueprint.niche}
        Pricing Strategy: {blueprint.pricing_strategy}
        Revenue Model: {blueprint.revenue_model}
        
        Generate a pricing and revenue plan for this business. Return a JSON object with:
        - "pricing": A dictionary outlining price points or tiers based on the strategy.
        - "revenue_projections": A dictionary with estimated revenue for "month_1", "month_3", and "month_6".
        """
        
        result = await self.think_json(prompt, "Calculating revenue projections and pricing")
        await self._set_status(AgentStatus.WORKING, task="Calculating revenue projections...", progress=60)
        await self._emit_log("Finalizing Stripe mock configuration...")
        
        stripe_config = {
            "account_id": f"acct_{uuid.uuid4().hex[:14]}",
            "mock_products_created": True
        }
            
        await self._set_status(AgentStatus.WORKING, task="Payment infrastructure ready", progress=90)
        
        return {
            "pricing": result.get("pricing", {}),
            "revenue_projections": result.get("revenue_projections", {}),
            "stripe_config": stripe_config
        }
