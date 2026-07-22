import { create } from 'zustand';
import { Business } from '../types/business';
import { AgentState, AgentId } from '../types/agent';
import { AgentEvent, EventType } from '../types/events';

interface BusinessStore {
  business: Business | null;
  setBusiness: (business: Business | null) => void;
  applyEvent: (event: AgentEvent) => void;
}

const defaultAgents: Record<string, AgentState> = {
  atlas: { agentId: 'atlas', name: 'Atlas', role: 'CEO', emoji: '🧠', status: 'idle', progress: 0, logs: [] },
  nova: { agentId: 'nova', name: 'Nova', role: 'Designer', emoji: '🎨', status: 'idle', progress: 0, logs: [] },
  forge: { agentId: 'forge', name: 'Forge', role: 'Engineer', emoji: '⚙️', status: 'idle', progress: 0, logs: [] },
  pulse: { agentId: 'pulse', name: 'Pulse', role: 'Marketing', emoji: '📢', status: 'idle', progress: 0, logs: [] },
  orbit: { agentId: 'orbit', name: 'Orbit', role: 'Operations', emoji: '🔄', status: 'idle', progress: 0, logs: [] },
  vault: { agentId: 'vault', name: 'Vault', role: 'Finance', emoji: '💰', status: 'idle', progress: 0, logs: [] },
  echo: { agentId: 'echo', name: 'Echo', role: 'Support', emoji: '🎧', status: 'idle', progress: 0, logs: [] },
  insight: { agentId: 'insight', name: 'Insight', role: 'Analytics', emoji: '📊', status: 'idle', progress: 0, logs: [] },
};

export const useBusinessStore = create<BusinessStore>((set) => ({
  business: null,
  setBusiness: (business) => set({ business }),
  applyEvent: (event) => set((state) => {
    if (!state.business || state.business.id !== event.businessId) return state;

    const b = { ...state.business };
    
    // Global business events
    if (event.eventType === 'business_created') b.status = 'running';
    if (event.eventType === 'business_live') b.status = 'live';
    if (event.eventType === 'product_created' && event.payload) {
      b.products = [...b.products, event.payload as unknown as import('../types/business').Product];
    }
    if (event.eventType === 'website_updated' && event.payload?.url) {
      b.websiteUrl = event.payload.url as string;
    }

    // Agent specific events
    if (event.agentId) {
      const agents = { ...b.agents };
      if (!agents[event.agentId]) {
        agents[event.agentId] = defaultAgents[event.agentId] || {
          agentId: event.agentId as AgentId, name: event.agentId, role: 'Agent', emoji: '🤖', status: 'idle', progress: 0, logs: []
        };
      }
      
      const agent = { ...agents[event.agentId] };
      
      if (event.eventType === 'agent_started') agent.status = 'working';
      if (event.eventType === 'agent_thinking') agent.status = 'thinking';
      if (event.eventType === 'agent_done') agent.status = 'done';
      if (event.eventType === 'agent_error') agent.status = 'error';
      
      if (event.task) agent.currentTask = event.task;
      if (event.progress !== undefined) agent.progress = event.progress;
      if (event.logLine) {
        agent.logs = [...agent.logs, event.logLine].slice(-20); // Keep last 20 logs per agent
      }
      
      agents[event.agentId] = agent;
      b.agents = agents;
    }

    return { business: b };
  }),
}));
