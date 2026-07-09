# MadeThis

MadeThis is an autonomous AI business operating system for the Google Gemini
XPRIZE Hackathon.

The MVP starts with product and strategy generation, but the architecture is
intentionally broader than dropshipping. Future agents should be able to research
markets, generate business strategy, create branding, prepare commerce listings,
launch storefronts, manage marketing, and analyze performance.

## Architecture

The application follows strict clean architecture boundaries:

- `apps/web`: Next.js frontend
- `services/api`: FastAPI orchestration backend
- `packages/contracts`: shared TypeScript contracts
- `infra`: Google Cloud infrastructure-as-code

Within each application, code follows these boundaries:

- `domain`: business entities, value types, and agent contracts
- `application`: use cases and service interfaces
- `infrastructure`: framework, API, database, AI, and provider adapters
- `presentation`: HTTP/UI adapters and view models

Business logic must not live in React components or API route handlers.

## Agent System

The backend is structured for these specialized agents:

- CEO
- Research
- Branding
- Product
- Store
- Marketing
- Sales
- Finance
- Support

Milestone 1 registers the roles and health surface only. Autonomous execution,
Gemini reasoning, MCP connectors, and storefront provisioning are implemented in
later milestones after the foundation is stable.

## Gemini Access

Milestones 0-4 use Google AI Studio through `GEMINI_API_KEY`. Vertex AI is not
part of the initial architecture unless the project explicitly migrates later.

## Development

```bash
npm install
python3 -m pip install -r services/api/requirements-dev.txt
npm run dev
```

Run the backend separately:

```bash
npm run dev:api
```

For local Gemini development, copy `services/api/.env.example` into
`services/api/.env.local` or export `GEMINI_API_KEY` in your shell. The API
automatically loads `services/api/.env.local` and `services/api/.env`. Do not
commit real API keys.

The web app protects generation behind a founder passcode and an HttpOnly
session cookie. Local defaults are intentionally development-only:

- `APP_AUTH_PASSWORD=founder-pass`
- `APP_SESSION_TOKEN=dev-antigravity-session-token`
- `ANTIGRAVITY_INTERNAL_API_KEY=dev-antigravity-internal-key`

Use Secret Manager-backed values for deployed environments.

Quality gates for every milestone:

```bash
npm run lint
npm run typecheck
npm run build
npm run check:api
```
