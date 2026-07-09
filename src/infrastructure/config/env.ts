import { z } from "zod";

const serverEnvSchema = z.object({
  GEMINI_API_KEY: z.string().min(1).optional(),
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
});

export type ServerEnv = z.infer<typeof serverEnvSchema>;

export function readServerEnv(): ServerEnv {
  return serverEnvSchema.parse({
    GEMINI_API_KEY: process.env.GEMINI_API_KEY,
    NODE_ENV: process.env.NODE_ENV,
  });
}
