import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.models.schemas import AgentId, AgentStatus, Business
from .base_agent import BaseAgent

class PulseAgent(BaseAgent):
    def __init__(self, business: Business):
        super().__init__(AgentId.PULSE, business)

    async def run(self) -> dict:
        await self._set_status(AgentStatus.WORKING, task="Crafting marketing strategy...", progress=10)
        
        blueprint = self.business.blueprint
        if not blueprint:
            raise ValueError("PulseAgent requires a BusinessBlueprint to proceed.")
            
        await self._emit_log("Crafting product descriptions...")
        
        prompt = f"""
        You are Pulse, a world-class marketer and copywriter.
        Business Niche: {blueprint.niche}
        Target Audience: {blueprint.target_audience}
        Value Proposition: {blueprint.value_proposition}
        
        Create a marketing content pack for this business. Return a JSON object with:
        - "hero_copy": {{"headline": "Catchy headline", "cta": "Call to action text"}}
        - "product_descriptions": A list of 3 compelling, SEO-optimized product descriptions for items fitting this niche.
        - "social_posts": A list of 3 social media post variants (e.g., Twitter, Instagram) to launch the brand.
        - "email_subjects": A list of 5 catchy email subject lines for the launch campaign.
        """
        
        result = await self.think_json(prompt, "Generating marketing content pack")
        await self._set_status(AgentStatus.WORKING, task="Writing social content...", progress=55)
        await self._emit_log("Writing email sequences...")
        
        await self._set_status(AgentStatus.WORKING, task="Finalizing marketing content...", progress=80)
        
        return {
            "product_descriptions": result.get("product_descriptions", []),
            "social_posts": result.get("social_posts", []),
            "email_subjects": result.get("email_subjects", []),
            "hero_copy": result.get("hero_copy", {})
        }
