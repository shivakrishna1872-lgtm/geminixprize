import asyncio
import logging
from datetime import datetime
from backend.models.schemas import Business, AgentEvent, EventType
from backend.orchestrator.event_bus import EventBus

logger = logging.getLogger(__name__)

async def emit_event(business_id: str, event_type: EventType, agent_id: str = "system", payload: dict = None, task: str = None, progress: int = None, log_line: str = None):
    event = AgentEvent(
        businessId=business_id,
        agentId=agent_id,
        eventType=event_type,
        task=task,
        progress=progress,
        logLine=log_line,
        payload=payload,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )
    await EventBus.publish(event)

async def run_agent_with_retry(agent, max_retries=2):
    for attempt in range(max_retries):
        try:
            return await agent.execute()
        except Exception as e:
            logger.warning(f"Agent {agent.agent_id} failed on attempt {attempt+1}: {e}")
            if attempt == max_retries - 1:
                # Last attempt failed, return graceful fallback
                return {"error": str(e), "status": "partial_failure"}
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

async def orchestrate_business(business: Business):
    """
    The main DAG execution loop for AntiGravity.
    """
    logger.info(f"Starting orchestration for business: {business.id}")
    await emit_event(business.id, EventType.BUSINESS_CREATED, payload={"prompt": business.prompt})

    try:
        from backend.agents.atlas_agent import AtlasAgent
        from backend.agents.nova_agent import NovaAgent
        from backend.agents.orbit_agent import OrbitAgent
        from backend.agents.vault_agent import VaultAgent
        from backend.agents.forge_agent import ForgeAgent
        from backend.agents.pulse_agent import PulseAgent
        from backend.agents.echo_agent import EchoAgent
        from backend.agents.insight_agent import InsightAgent
        
        # 1. Atlas (Planner)
        atlas = AtlasAgent(business)
        atlas_result = await run_agent_with_retry(atlas)
        business.blueprint = atlas_result.get("blueprint")
        
        # 2. Parallel: Nova, Orbit, Vault
        nova = NovaAgent(business)
        orbit = OrbitAgent(business)
        vault = VaultAgent(business)
        
        parallel_1_results = await asyncio.gather(
            run_agent_with_retry(nova),
            run_agent_with_retry(orbit),
            run_agent_with_retry(vault),
            return_exceptions=True
        )
        
        business.brand = parallel_1_results[0].get("brand") if not isinstance(parallel_1_results[0], Exception) else None
        business.products = parallel_1_results[1].get("products", []) if not isinstance(parallel_1_results[1], Exception) else []
        
        # 3. Forge
        forge = ForgeAgent(business)
        forge_result = await run_agent_with_retry(forge)
        business.websiteUrl = forge_result.get("website_url") if not isinstance(forge_result, Exception) else None
        
        # 4. Parallel: Pulse, Echo, Insight
        pulse = PulseAgent(business)
        echo = EchoAgent(business)
        insight = InsightAgent(business)
        
        await asyncio.gather(
            run_agent_with_retry(pulse),
            run_agent_with_retry(echo),
            run_agent_with_retry(insight),
            return_exceptions=True
        )
                
        # Finish
        business.status = "live"
        await emit_event(business.id, EventType.BUSINESS_LIVE, payload={"url": business.websiteUrl})
        logger.info(f"Orchestration complete for: {business.id}")

    except Exception as e:
        logger.error(f"Orchestration failed for {business.id}: {e}")
        business.status = "failed"
        await emit_event(business.id, EventType.AGENT_ERROR, log_line=f"FATAL ERROR: {str(e)}")
