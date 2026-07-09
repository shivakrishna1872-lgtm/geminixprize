import type { AgentCapability } from "./agent-capability";

export type AgentRequest<TInput> = Readonly<{
  businessId: string;
  input: TInput;
}>;

export type AgentResult<TOutput> = Readonly<{
  output: TOutput;
  auditSummary: string;
}>;

export interface AutonomousAgent<TInput, TOutput> {
  readonly capability: AgentCapability;
  execute(request: AgentRequest<TInput>): Promise<AgentResult<TOutput>>;
}
