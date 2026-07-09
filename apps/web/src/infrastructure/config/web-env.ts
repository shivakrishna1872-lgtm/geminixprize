import { z } from "zod";

const webEnvSchema = z.object({
  NEXT_PUBLIC_API_BASE_URL: z.string().url().default("http://127.0.0.1:8000"),
});

const serverWebEnvSchema = z.object({
  ANTIGRAVITY_API_BASE_URL: z.string().url().default("http://127.0.0.1:8000"),
  ANTIGRAVITY_INTERNAL_API_KEY: z.string().min(1).default("dev-antigravity-internal-key"),
  APP_AUTH_PASSWORD: z.string().min(8).default("founder-pass"),
  APP_SESSION_TOKEN: z.string().min(16).default("dev-antigravity-session-token"),
});

export type WebEnv = z.infer<typeof webEnvSchema>;
export type ServerWebEnv = z.infer<typeof serverWebEnvSchema>;

export function readWebEnv(): WebEnv {
  return webEnvSchema.parse({
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
  });
}

export function readServerWebEnv(): ServerWebEnv {
  return serverWebEnvSchema.parse({
    ANTIGRAVITY_API_BASE_URL: process.env.ANTIGRAVITY_API_BASE_URL,
    ANTIGRAVITY_INTERNAL_API_KEY: process.env.ANTIGRAVITY_INTERNAL_API_KEY,
    APP_AUTH_PASSWORD: process.env.APP_AUTH_PASSWORD,
    APP_SESSION_TOKEN: process.env.APP_SESSION_TOKEN,
  });
}
