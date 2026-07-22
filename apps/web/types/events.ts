/**
 * SSE event types for the AntiGravity agent streaming system.
 * Events flow from the backend orchestrator to the frontend via Server-Sent Events.
 */

export type EventType =
  | 'agent_started'
  | 'agent_thinking'
  | 'agent_log'
  | 'agent_done'
  | 'agent_error'
  | 'business_created'
  | 'business_live'
  | 'product_created'
  | 'website_updated'
  | 'payment_configured';

export interface AgentEvent {
  businessId: string;
  agentId: string;
  eventType: EventType;
  task?: string;
  logLine?: string;
  progress?: number;
  payload?: Record<string, unknown>;
  timestamp: string;
}
