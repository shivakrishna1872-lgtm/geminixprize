import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.models.schemas import AgentId, AgentStatus, Business
from .base_agent import BaseAgent

class EchoAgent(BaseAgent):
    def __init__(self, business: Business):
        super().__init__(AgentId.ECHO, business)

    async def run(self) -> dict:
        await self._set_status(AgentStatus.WORKING, task="Writing customer FAQ...", progress=33)
        
        blueprint = self.business.blueprint
        if not blueprint:
            raise ValueError("EchoAgent requires a BusinessBlueprint to proceed.")
            
        await self._emit_log("Drafting return policy...")
        
        prompt = f"""
        You are Echo, a customer support and legal specialist.
        Business Niche: {blueprint.niche}
        Value Proposition: {blueprint.value_proposition}
        
        Generate customer support and legal content for this business. Return a JSON object with:
        - "faq": A list of 8 common FAQ items (objects with "q" and "a" keys).
        - "return_policy": A comprehensive return/refund policy (string).
        - "privacy_policy": A short, standard privacy policy (string).
        """
        
        result = await self.think_json(prompt, "Generating support and legal content")
        await self._set_status(AgentStatus.WORKING, task="Generating privacy policy...", progress=66)
        await self._emit_log("Finalizing support documentation...")
        
        return {
            "faq": result.get("faq", []),
            "return_policy": result.get("return_policy", ""),
            "privacy_policy": result.get("privacy_policy", "")
        }
