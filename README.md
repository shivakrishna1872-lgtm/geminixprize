# AntiGravity

AntiGravity is an autonomous AI business operating system for the Google Gemini
XPRIZE Hackathon.

The MVP starts with product and strategy generation, but the architecture is
intentionally broader than dropshipping. Future agents should be able to research
markets, generate business strategy, create branding, prepare commerce listings,
launch storefronts, manage marketing, and analyze performance.

## Architecture

The application follows strict clean architecture boundaries:

- `src/domain`: business entities, value types, and agent contracts
- `src/application`: use cases and service interfaces
- `src/infrastructure`: framework, API, database, AI, and provider adapters
- `src/presentation`: React-facing view models and display configuration
- `src/app`: Next.js routes and page composition only

Business logic must not live in React components or API route handlers.

## Gemini Access

Milestones 0-4 use Google AI Studio through `GEMINI_API_KEY`. Vertex AI is not
part of the initial architecture unless the project explicitly migrates later.

## Development

```bash
npm install
npm run dev
```

Quality gates for every milestone:

```bash
npm run lint
npm run typecheck
npm run build
```
