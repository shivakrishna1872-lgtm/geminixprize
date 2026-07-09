import { z } from "zod";

export const serviceHealthSchema = z.object({
  service: z.literal("antigravity-api"),
  status: z.enum(["ok", "degraded"]),
  version: z.string().min(1),
  environment: z.enum(["development", "test", "production"]),
  capabilities: z.array(z.string().min(1)),
});

export type ServiceHealth = z.infer<typeof serviceHealthSchema>;

export const agentRoleSchema = z.enum([
  "ceo",
  "research",
  "branding",
  "product",
  "store",
  "marketing",
  "sales",
  "finance",
  "support",
]);

export type AgentRole = z.infer<typeof agentRoleSchema>;
