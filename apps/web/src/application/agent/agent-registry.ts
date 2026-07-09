import type { AgentCapability } from "@/domain/agent/agent-capability";
import type { AutonomousAgent } from "@/domain/agent/autonomous-agent";

export interface AgentRegistry {
  findByCapability<TInput, TOutput>(
    capability: AgentCapability,
  ): AutonomousAgent<TInput, TOutput> | null;
}
