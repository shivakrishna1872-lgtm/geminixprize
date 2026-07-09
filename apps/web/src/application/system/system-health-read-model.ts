import type { ServiceHealth } from "@antigravity/contracts";

export type SystemHealthReadModel = Readonly<{
  api: ServiceHealth;
  frontend: {
    service: "antigravity-web";
    status: "ok";
  };
}>;
