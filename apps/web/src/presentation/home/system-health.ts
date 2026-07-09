import type { SystemHealthReadModel } from "@/application/system/system-health-read-model";

export const milestoneOneSystemHealth: SystemHealthReadModel = {
  frontend: {
    service: "antigravity-web",
    status: "ok",
  },
  api: {
    service: "antigravity-api",
    status: "ok",
    version: "0.1.0",
    environment: "development",
    capabilities: [
      "agent-registry",
      "health-check",
      "clean-architecture",
      "future-orchestration-ready",
    ],
  },
};
