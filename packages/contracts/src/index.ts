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

export const companyBlueprintSchema = z.object({
  company_name: z.string().min(1),
  tagline: z.string().min(1),
  category: z.string().min(1),
  audience: z.string().min(1),
  positioning: z.string().min(1),
  starter_products: z.array(z.string().min(1)),
  pricing_strategy: z.string().min(1),
  storefront_sections: z.array(z.string().min(1)),
  marketing_plan: z.array(z.string().min(1)),
  launch_checklist: z.array(z.string().min(1)),
  agent_log: z.array(z.string().min(1)),
  status: z.string().min(1),
});

export type CompanyBlueprint = z.infer<typeof companyBlueprintSchema>;
