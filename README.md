# 🌌 MadeThis / AntiGravity
## Autonomous AI Business Operating System

[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2015-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini%202.0-blue?logo=google)](https://deepmind.google/technologies/gemini/)
[![XPRIZE](https://img.shields.io/badge/Hackathon-Google%20Gemini%20XPRIZE%202026-purple)](#)

> An AI-native platform that autonomously creates, launches, and operates real online businesses from a single user prompt. Built for the Google Gemini XPRIZE Hackathon.

---

# Overview

**MadeThis** (with its **AntiGravity** experience frontend) is an autonomous AI-powered business operating system designed to transform ideas into executable businesses. 

Rather than functioning as a single AI assistant, the platform operates as a coordinated network of specialized AI agents that collaborate to research markets, develop products, create branding, generate commerce assets, design marketing strategies, and analyze business performance.

The MVP begins with AI-powered product discovery and business strategy generation. However, the architecture is intentionally designed to support a much larger autonomous business platform capable of managing the complete lifecycle of a company.

The long-term vision is to provide every founder with an AI executive team capable of researching, planning, launching, and operating businesses autonomously.

---

## 🚀 Key Features

*   **Cinematic, Pixel-Art User Experience**: A retro-futuristic dark mode interface featuring glassmorphic layout, fluid Framer Motion transitions, and animated pixel-art scenery.
*   **Multi-Agent DAG Orchestration**: Executes 8 specialized AI agents sequentially and in parallel in a robust Directed Acyclic Graph (DAG) flow.
*   **Real-Time SSE Streaming**: Uplinks logs, agent thoughts, progress meters, and payload assets instantly to the frontend using Server-Sent Events (SSE).
*   **Resiliency & Graceful Failures**: Wraps agents in exponential backoff retry loops, proceeding with partial completion and publishing errors to the stream if an agent fails.
*   **Live Mock Previews**: Generates dynamic storefront previews (name, logo, palettes, product cards, CTA) live as the engineering agent works.
*   **Financial Projections Dashboard**: Visualizes startup costs, annual recurring revenue (ARR), margins, and growth action plans computed by the finance agent.
*   **Clean Service Interfaces**: Abstracted providers for Stripe, Printify, Duda, and Commerce Layer, ready to swap from mock to live APIs seamlessly.

---

## 🧠 The Agent Fleet

The platform relies on 8 specialized agents, each managing a specific segment of the business creation process:

1.  **🧠 Atlas (CEO/Planner)**: Ingests the prompt, conducts competitor research, and constructs the initial **Business Blueprint**.
2.  **🎨 Nova (Brand Designer)**: Generates typography pairs, color palettes, taglines, and brand keywords.
3.  **🔄 Orbit (Operations Specialist)**: Selects products from a print-on-demand catalog, setting pricing and SKUs.
4.  **💰 Vault (Finance Director)**: Configures payment gateways, pricing tier structures, and calculates revenue projections.
5.  **⚙️ Forge (Software Engineer)**: Automatically synthesizes the page layouts and publishes the storefront preview.
6.  **📢 Pulse (Marketing Lead)**: Generates SEO-optimized product copy, social media ads, and newsletter scripts.
7.  **🎧 Echo (Support Specialist)**: Drafts customized customer support FAQs and return/refund policies.
8.  **📊 Insight (Analytics Lead)**: Defines targeted KPIs, launch readiness checklists, and a 30-day action plan.

---

# Architecture Philosophy

The platform follows strict clean architecture and domain-driven design principles:

> Core business intelligence should never depend on frameworks, databases, user interfaces, or external providers.

The system is designed so that individual technologies can be replaced without rewriting the underlying business logic:
*   Gemini can be replaced with another AI provider.
*   Databases can be migrated.
*   Frontend frameworks can change.
*   Cloud providers can change.
*   The core business engine remains independent.

---

## 🛠️ Project Structure

```
geminixprize/
├── apps/
│   └── web/                   # Next.js 15 Frontend (TypeScript, Tailwind, Framer Motion)
├── backend/
│   ├── agents/                # AI Agent definitions (Atlas, Nova, Forge, etc.)
│   ├── api/                   # FastAPI endpoints (Launch, Stream, Business State)
│   ├── core/                  # Core configurations, logging, and Firebase auth mock
│   ├── models/                # Pydantic schemas (Shared state validation)
│   ├── orchestrator/          # Event loop, Event Bus (JSONL tailing), DAG scheduler
│   └── services/              # Swappable Mock Service Providers (Stripe, Duda, Printify)
├── shared/
│   └── types/                 # Shared data models for cross-application type safety
├── services/
│   └── api/                   # Modular API Services (settings, schemas, health routers)
├── packages/
│   └── contracts/             # Shared typescript schemas and type definitions
├── infrastructure/            # Docker configurations and Terraform provisioning scripts
└── README.md                  # Project documentation
```

---

## 🏁 Getting Started

### Prerequisites

*   Python 3.10+
*   Node.js 18+ and npm
*   A Google Cloud Project (for Vertex AI Gemini API)

### 1. Setup the Backend API

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (copy `.env.example` to `.env` and fill in your details):
   ```bash
   cp .env.example .env
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn backend.api.main:app --port 8000 --reload
   ```

### 2. Setup the Frontend Web App

1. Navigate to the frontend folder:
   ```bash
   cd apps/web
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🏆 Hackathon Context

This application was developed as a submission for the **Google Gemini XPRIZE Hackathon**, demonstrating how Gemini 2.0 can act as a fully autonomous orchestration layer to build and scale online startups from scratch.
