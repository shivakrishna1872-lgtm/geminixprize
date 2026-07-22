"""
Atlas Agent — CEO
=================
The first agent in the AntiGravity pipeline.  It ingests the user's raw
business prompt and returns:
  • A fully-structured BusinessBlueprint (market research, business model,
    pricing strategy, competitor analysis)
  • An initial BrandIdentity skeleton for Nova to flesh out

All heavy reasoning is delegated to Gemini via think_json().
"""

import os
import sys

# ---------------------------------------------------------------------------
# Path setup — reach shared/types/models.py two directories above agents/
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.models.schemas import (
    AgentId,
    AgentStatus,
    Business,
    BusinessBlueprint,
    BrandIdentity,
)
from base_agent import BaseAgent


class AtlasAgent(BaseAgent):
    """
    Atlas is the CEO agent.  It performs strategic research and planning,
    then hands off a structured blueprint to the rest of the agent fleet.
    """

    def __init__(self, business: Business):
        super().__init__(AgentId.ATLAS, business)

    # -----------------------------------------------------------------------
    # Main entry point
    # -----------------------------------------------------------------------

    async def run(self) -> dict:
        """
        Execute Atlas's full strategic planning workflow:
          1. Market research & competitor analysis
          2. Business model selection
          3. Pricing strategy
          4. Brand skeleton generation
          5. Delegate checklist assembly
        """
        prompt_text = self.business.prompt

        # -- Step 1: Market research & competitor analysis -------------------
        await self._set_status(AgentStatus.WORKING, task="Analyzing market demand...", progress=10)
        await self._emit_log("🌍 Analyzing market demand...")
        await self._emit_log("📊 Pulling industry signals for: " + prompt_text[:80])

        market_data = await self.think_json(
            prompt=f"""You are a world-class market research analyst and startup strategist.

The user wants to launch the following business:
\"\"\"{prompt_text}\"\"\"

Conduct thorough market research and return a JSON object with these exact keys:
{{
  "niche": "A crisp 3-8 word niche description",
  "target_audience": "Detailed description of primary customer persona (age, interests, pain points)",
  "market_size": "Estimated addressable market (e.g., '$4.2B globally')",
  "demand_signals": ["signal 1", "signal 2", "signal 3"],
  "competitors": ["Competitor A", "Competitor B", "Competitor C", "Competitor D"],
  "competitive_advantages": ["advantage 1", "advantage 2", "advantage 3"],
  "market_gaps": "Key underserved needs or gaps this business can exploit"
}}

Be specific, realistic, and data-driven. Base your analysis on real market knowledge.""",
            task_description="Conducting market research and competitor analysis",
        )

        await self._emit_log(f"🔍 Identified niche: {market_data.get('niche', 'N/A')}")
        await self._emit_log(f"👥 Target audience mapped")

        # -- Step 2: Identify competitors ------------------------------------
        await self._set_status(AgentStatus.WORKING, task="Identifying competitors...", progress=30)
        await self._emit_log("🏆 Identifying competitors...")
        competitors = market_data.get("competitors", [])
        for c in competitors:
            await self._emit_log(f"   • Competitor found: {c}")

        # -- Step 3: Business strategy & model selection ---------------------
        await self._set_status(AgentStatus.WORKING, task="Crafting business strategy...", progress=60)
        await self._emit_log("⚙️  Crafting business strategy...")
        await self._emit_log("💡 Selecting optimal revenue model...")

        strategy_data = await self.think_json(
            prompt=f"""You are a startup CEO and business model expert.

Business niche: {market_data.get('niche', prompt_text)}
Target audience: {market_data.get('target_audience', 'general consumers')}
Market gaps: {market_data.get('market_gaps', 'N/A')}
Competitors: {', '.join(competitors)}

Design a complete go-to-market strategy. Return a JSON object:
{{
  "value_proposition": "A single powerful sentence that captures why customers will choose this business",
  "revenue_model": "Primary revenue model (e.g., 'Direct-to-consumer e-commerce with print-on-demand fulfillment')",
  "pricing_strategy": "Pricing approach (e.g., 'Value-based pricing at premium tier — 20-30% above commodity products')",
  "distribution_channels": ["channel 1", "channel 2", "channel 3"],
  "launch_checklist": [
    "Set up Shopify/e-commerce store",
    "Configure print-on-demand supplier (Printify)",
    "Design hero product line",
    "Launch social media presence",
    "Run first paid ad campaign",
    "Set up email marketing sequence",
    "Enable customer reviews",
    "Launch referral/loyalty program"
  ],
  "growth_levers": ["lever 1", "lever 2", "lever 3"],
  "moat": "What makes this business defensible long-term"
}}

Make this commercially compelling and actionable.""",
            task_description="Designing business model and pricing strategy",
        )

        await self._emit_log(f"✅ Value proposition: {strategy_data.get('value_proposition', '')[:80]}...")
        await self._emit_log(f"💰 Pricing strategy selected: {strategy_data.get('pricing_strategy', '')[:60]}")

        # -- Step 4: Brand skeleton for Nova ---------------------------------
        await self._set_status(AgentStatus.WORKING, task="Delegating to agents...", progress=90)
        await self._emit_log("🎨 Generating brand skeleton for Nova...")

        brand_skeleton_data = await self.think_json(
            prompt=f"""You are a senior brand strategist.

Business niche: {market_data.get('niche', prompt_text)}
Target audience: {market_data.get('target_audience', 'general consumers')}
Value proposition: {strategy_data.get('value_proposition', '')}
Competitive advantages: {market_data.get('competitive_advantages', [])}

Generate an initial brand skeleton. Return a JSON object:
{{
  "name_candidates": ["Name1", "Name2", "Name3"],
  "brand_personality": ["trait1", "trait2", "trait3"],
  "mood": "Brief description of brand mood/feeling (e.g., 'bold, rebellious, empowering')",
  "color_direction": "Color palette direction (e.g., 'dark backgrounds with electric blue accents')",
  "style_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}

Prioritize names that are memorable, .com-friendly, and 1-2 syllables when possible.""",
            task_description="Creating brand skeleton for Nova",
        )

        await self._emit_log(f"🚀 Brand candidates: {', '.join(brand_skeleton_data.get('name_candidates', []))}")
        await self._emit_log("📋 Delegate checklist assembled for all 7 specialist agents")
        await self._emit_log("✅ Atlas strategic planning complete!")

        # -- Assemble final return dicts ------------------------------------
        blueprint = BusinessBlueprint(
            niche=market_data.get("niche", prompt_text),
            target_audience=market_data.get("target_audience", "general consumers"),
            value_proposition=strategy_data.get("value_proposition", ""),
            competitors=competitors,
            pricing_strategy=strategy_data.get("pricing_strategy", "Value-based pricing"),
            revenue_model=strategy_data.get("revenue_model", "E-commerce"),
            launch_checklist=strategy_data.get("launch_checklist", []),
        )

        brand_skeleton = {
            "name_candidates": brand_skeleton_data.get("name_candidates", []),
            "brand_personality": brand_skeleton_data.get("brand_personality", []),
            "mood": brand_skeleton_data.get("mood", ""),
            "color_direction": brand_skeleton_data.get("color_direction", ""),
            "style_keywords": brand_skeleton_data.get("style_keywords", []),
            "niche": market_data.get("niche", prompt_text),
            "value_proposition": strategy_data.get("value_proposition", ""),
            "target_audience": market_data.get("target_audience", ""),
        }

        return {
            "blueprint": blueprint.model_dump(),
            "brand_skeleton": brand_skeleton,
            "market_research": {
                "market_size": market_data.get("market_size", ""),
                "demand_signals": market_data.get("demand_signals", []),
                "competitive_advantages": market_data.get("competitive_advantages", []),
                "market_gaps": market_data.get("market_gaps", ""),
                "distribution_channels": strategy_data.get("distribution_channels", []),
                "growth_levers": strategy_data.get("growth_levers", []),
                "moat": strategy_data.get("moat", ""),
            },
        }
