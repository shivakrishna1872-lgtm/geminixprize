# Infrastructure

AntiGravity will deploy to Google Cloud with Cloud Run, Pub/Sub, BigQuery, and
Secret Manager. Milestone 1 establishes the repository boundary for
infrastructure-as-code; Terraform resources and deployment automation belong
here once the application contracts stabilize.

Planned services:

- `apps/web`: Cloud Run service for the Next.js frontend
- `services/api`: Cloud Run service for the FastAPI orchestration backend
- Pub/Sub: asynchronous agent execution events
- BigQuery: audit logs, execution telemetry, and business metrics
- Secret Manager: Gemini, MCP provider, commerce, and payment credentials
