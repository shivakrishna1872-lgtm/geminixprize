export type AgentCapability =
  | "market-research"
  | "business-strategy"
  | "brand-generation"
  | "product-generation"
  | "commerce-listing"
  | "storefront-launch"
  | "marketing-operations"
  | "performance-analysis";

export type AgentExecutionStatus = "queued" | "running" | "completed" | "failed";

export type AgentExecutionRecord = Readonly<{
  id: string;
  capability: AgentCapability;
  status: AgentExecutionStatus;
  startedAt: Date;
  completedAt?: Date;
}>;
