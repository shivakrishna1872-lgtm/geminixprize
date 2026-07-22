import os
import sys
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.models.schemas import AgentId, AgentStatus, Business, Product
from .base_agent import BaseAgent

class OrbitAgent(BaseAgent):
    def __init__(self, business: Business):
        super().__init__(AgentId.ORBIT, business)

    async def run(self) -> dict:
        await self._set_status(AgentStatus.WORKING, task="Searching product catalog...", progress=20)
        
        blueprint = self.business.blueprint
        if not blueprint:
            raise ValueError("OrbitAgent requires a BusinessBlueprint to proceed.")
            
        await self._emit_log("Configuring print-on-demand products...")
        
        prompt = f"""
        You are Orbit, an operations and logistics specialist.
        Business Niche: {blueprint.niche}
        Target Audience: {blueprint.target_audience}
        
        Select the 3 best print-on-demand product types for this business from this list:
        [t-shirt, hoodie, mug, phone case, tote bag, poster, sticker]
        
        For each product, generate a name, description, reasonable price in USD, and tags.
        Return a JSON object with:
        - "products": A list of objects with "name", "description", "price_usd", and "tags".
        """
        
        result = await self.think_json(prompt, "Selecting and configuring products")
        await self._set_status(AgentStatus.WORKING, task="Setting up fulfillment...", progress=50)
        await self._emit_log("Finalizing product configurations...")
        
        products = []
        for p in result.get("products", []):
            products.append({
                "name": p.get("name"),
                "description": p.get("description"),
                "price_usd": p.get("price_usd"),
                "tags": p.get("tags", []),
                "printify_id": f"mock_{uuid.uuid4().hex[:8]}"
            })
            
        await self._set_status(AgentStatus.WORKING, task="Products configured", progress=85)
        
        return {"products": products}
