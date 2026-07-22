/**
 * Agent types for AntiGravity multi-agent system.
 * Each agent specializes in a domain of business creation.
 */

export type AgentId =
  | 'atlas'
  | 'nova'
  | 'forge'
  | 'pulse'
  | 'orbit'
  | 'vault'
  | 'echo'
  | 'insight';

export type AgentStatus = 'idle' | 'thinking' | 'working' | 'done' | 'error';

export interface AgentState {
  agentId: AgentId;
  name: string;
  role: string;
  emoji: string;
  status: AgentStatus;
  currentTask?: string;
  progress: number;
  logs: string[];
}
