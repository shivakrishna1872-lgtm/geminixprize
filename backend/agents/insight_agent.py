import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.models.schemas import AgentId, AgentStatus, Business
from .base_agent import BaseAgent

class InsightAgent(BaseAgent):
    def __init__(self, business: Business):
        super().__init__(AgentId.INSIGHT, business)

    async def run(self) -> dict:
        await self._set_status(AgentStatus.WORKING, task="Establishing analytics framework...", progress=30)
        
        blueprint = self.business.blueprint
        if not blueprint:
            raise ValueError("InsightAgent requires a BusinessBlueprint to proceed.")
            
        await self._emit_log("Defining KPIs...")
        
        prompt = f"""
        You are Insight, a data analytics and business strategy specialist.
        Business Niche: {blueprint.niche}
        Revenue Model: {blueprint.revenue_model}
        
        Generate an analytics schema and initial business health report. Return a JSON object with:
        - "kpis": A list of 5 key performance indicators for this business (objects with "name", "target", and "unit").
        - "launch_checklist": A list of 8 launch readiness items (objects with "item" and "done" (boolean true)).
        - "growth_plan": A list of 5 actionable 30-day growth steps (strings).
        """
        
        result = await self.think_json(prompt, "Generating analytics and growth strategy")
        await self._set_status(AgentStatus.WORKING, task="Generating growth strategy...", progress=70)
        await self._emit_log("Finalizing analytics schema...")
        
        return {
            "kpis": result.get("kpis", []),
            "launch_checklist": result.get("launch_checklist", []),
            "growth_plan": result.get("growth_plan", [])
        }
