# MadeThis

## Autonomous AI Business Operating System

Built for the Google Gemini XPRIZE Hackathon.

---

# Overview

MadeThis is an autonomous AI-powered business operating system designed to transform ideas into executable businesses.

Rather than functioning as a single AI assistant, MadeThis operates as a coordinated network of specialized AI agents that collaborate to research markets, develop products, create branding, generate commerce assets, design marketing strategies, and analyze business performance.

The MVP begins with AI-powered product discovery and business strategy generation. However, the architecture is intentionally designed to support a much larger autonomous business platform capable of managing the complete lifecycle of a company.

The long-term vision is to provide every founder with an AI executive team capable of researching, planning, launching, and operating businesses autonomously.

---

# Product Vision

Building a company requires expertise across many different areas:

- Market research
- Competitive analysis
- Product development
- Branding
- Copywriting
- Pricing strategy
- Customer research
- Marketing
- Sales operations
- Financial planning
- Customer support

Traditionally, founders need employees, agencies, and expensive software tools to handle these responsibilities.

MadeThis introduces an AI-native business organization where each business function is represented by a specialized autonomous agent.

The evolution of the platform:

```
Founder Idea

      |

      v

AI Business Intelligence Layer

      |

      v

Specialized Agent Team

      |

      v

Launch-Ready Business Strategy
```

The future system architecture:

```
Founder

   |

   v

CEO Agent

   |

   +----------------+
   |                |
   v                v

Research Agent   Product Agent

   |

   v

Brand Agent

   |

   v

Store Agent

   |

   v

Marketing Agent

   |

   v

Sales Agent

   |

   v

Finance Agent

   |

   v

Support Agent
```

---

# Architecture Philosophy

MadeThis follows strict clean architecture and domain-driven design principles.

The primary engineering philosophy:

> Core business intelligence should never depend on frameworks, databases, user interfaces, or external providers.

The system is designed so that individual technologies can be replaced without rewriting the underlying business logic.

Examples:

- Gemini can be replaced with another AI provider.
- Databases can be migrated.
- Frontend frameworks can change.
- Cloud providers can change.

The core business engine remains independent.

---

# Repository Structure

```
MadeThis/

├── apps/
│
│   └── web/
│       ├── app/
│       ├── components/
│       ├── hooks/
│       └── presentation/
│
├── services/
│
│   └── api/
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       ├── presentation/
│       └── main.py
│
├── packages/
│
│   └── contracts/
│       ├── schemas/
│       └── types/
│
├── infra/
│   ├── terraform/
│   ├── docker/
│   └── deployment/
│
├── docs/
│
├── scripts/
│
├── package.json
└── README.md
```

---

# Application Architecture

MadeThis is separated into independent layers.

The architecture follows:

```
Domain

    |

    v

Application

    |

    v

Infrastructure

    |

    v

Presentation
```

Each layer has a specific responsibility.

---

# Frontend Application

Location:

```
apps/web
```

Technology:

- Next.js
- TypeScript
- React
- Modern frontend architecture

Responsibilities:

- Founder onboarding
- Idea submission
- Business generation interface
- Agent status visualization
- Strategy presentation
- User interaction

The frontend does not contain business rules.

Its purpose is to:

1. Collect user input.
2. Communicate with backend services.
3. Display generated results.

---

# Backend Intelligence Service

Location:

```
services/api
```

Technology:

- FastAPI
- Python
- Async processing
- AI orchestration services

Responsibilities:

- Agent execution
- Gemini communication
- Workflow management
- Authentication
- API routing
- Provider abstraction

The backend contains the core intelligence of the platform.

---

# Domain Layer

Location:

```
domain/
```

The domain layer contains the fundamental concepts of the business system.

Examples:

```
Agent
BusinessIdea
MarketAnalysis
ProductConcept
BrandIdentity
BusinessStrategy
```

The domain layer:

- Does not depend on frameworks.
- Does not call APIs.
- Does not access databases.
- Does not know about Gemini.
- Contains only business rules.

---

# Application Layer

Location:

```
application/
```

The application layer defines business workflows.

Examples:

```
GenerateBusinessPlan

ResearchMarket

CreateProductStrategy

GenerateBrandIdentity

AnalyzeOpportunity
```

Responsibilities:

- Coordinate domain objects.
- Execute business processes.
- Manage application state.
- Define service contracts.

---

# Infrastructure Layer

Location:

```
infrastructure/
```

The infrastructure layer connects the application to external systems.

Includes:

- Gemini adapters
- Database clients
- Authentication systems
- Cloud services
- Storage systems
- External APIs

Examples:

```
GeminiClient

DatabaseRepository

CloudStorageAdapter

AuthenticationProvider
```

Infrastructure can be replaced without modifying business logic.

---

# Presentation Layer

Location:

```
presentation/
```

Contains external interfaces.

Examples:

- REST API routes
- Request validation
- Response models
- UI adapters

Responsibilities:

- Accept external requests.
- Validate data.
- Execute application services.
- Return responses.

---

# Agent System

MadeThis is built around a multi-agent architecture.

Each agent represents a specialized business department.

The initial system includes:

- CEO Agent
- Research Agent
- Branding Agent
- Product Agent
- Store Agent
- Marketing Agent
- Sales Agent
- Finance Agent
- Support Agent

---

# CEO Agent

Purpose:

The executive intelligence layer.

Responsibilities:

- Understand founder objectives.
- Coordinate specialized agents.
- Prioritize tasks.
- Combine agent outputs.
- Generate final decisions.

Future capabilities:

- Autonomous planning.
- Business optimization.
- Resource allocation.
- Strategic decision making.

---

# Research Agent

Responsibilities:

- Market research.
- Industry analysis.
- Competitor evaluation.
- Customer discovery.
- Trend identification.

Outputs:

```
Market Report

Customer Personas

Competition Analysis

Opportunity Score
```

---

# Product Agent

Responsibilities:

- Product discovery.
- Product positioning.
- Feature generation.
- Pricing recommendations.

Outputs:

```
Product Concept

Specifications

Pricing Strategy

Launch Plan
```

---

# Branding Agent

Responsibilities:

- Brand identity creation.
- Naming.
- Messaging.
- Brand positioning.

Outputs:

```
Brand Name

Brand Voice

Visual Direction

Marketing Position
```

---

# Store Agent

Responsibilities:

- Commerce preparation.
- Product listing generation.
- Store structure creation.

Outputs:

```
Product Pages

SEO Metadata

Descriptions

Store Configuration
```

---

# Marketing Agent

Responsibilities:

- Campaign generation.
- Growth strategy.
- Content planning.
- Advertisement concepts.

Outputs:

```
Marketing Strategy

Content Calendar

Campaign Ideas

Growth Plan
```

---

# Sales Agent

Responsibilities:

- Customer acquisition.
- Sales messaging.
- Conversion optimization.

Outputs:

```
Sales Funnel

Customer Outreach

Email Sequences
```

---

# Finance Agent

Responsibilities:

- Financial modeling.
- Cost analysis.
- Revenue forecasting.
- Profit calculations.

Outputs:

```
Financial Model

Pricing Analysis

ROI Prediction
```

---

# Support Agent

Responsibilities:

- Customer communication.
- Knowledge base generation.
- Support automation.

Outputs:

```
Support Documentation

Response Templates

Customer Insights
```

---

# Agent Execution Architecture

Future execution model:

```
User Request

      |

      v

CEO Agent

      |

      v

Task Planning Engine

      |

      v

Agent Execution Graph

      |

      v

Parallel Agent Processing

      |

      v

Result Aggregation

      |

      v

Business Blueprint
```

---

# MVP Scope

The MVP focuses on proving autonomous business creation.

The primary user flow:

```
Founder enters business idea

        |

        v

AI analyzes opportunity

        |

        v

Research Agent evaluates market

        |

        v

Product Agent creates product strategy

        |

        v

Brand Agent generates identity

        |

        v

CEO Agent creates final business blueprint
```

---

# Current MVP Features

## Founder Authentication

Implemented:

- Founder passcode protection.
- HttpOnly session cookies.
- Server-side authentication.

---

## Gemini Integration

Current architecture:

```
GEMINI_API_KEY

       |

       v

FastAPI Backend

       |

       v

Gemini Model
```

The backend controls AI access.

The frontend never directly exposes API credentials.

---

## Agent Registry

Current milestone includes:

- Agent registration.
- Agent metadata.
- Agent health checks.
- Agent availability tracking.

Future milestones add:

- Autonomous execution.
- Agent communication.
- Multi-step reasoning.
- Tool usage.

---

# Gemini Configuration

Milestones 0-4 use Google AI Studio through:

```
GEMINI_API_KEY
```

Vertex AI is not included in the initial implementation.

Migration to Vertex AI may occur when production requirements require:

- Enterprise authentication.
- Advanced monitoring.
- Large-scale deployment.

---

# Development Setup

## Requirements

Required:

- Node.js 20+
- Python 3.11+
- npm
- Git

---

# Installation

Clone repository:

```bash
git clone <repository-url>

cd MadeThis
```

Install frontend dependencies:

```bash
npm install
```

Install backend dependencies:

```bash
python3 -m pip install -r services/api/requirements-dev.txt
```

---

# Running Development Environment

Start frontend:

```bash
npm run dev
```

Start backend:

```bash
npm run dev:api
```

---

# Environment Configuration

Create:

```
services/api/.env.local
```

Example:

```
GEMINI_API_KEY=your_key_here
```

Never commit:

```
.env
.env.local
.env.production
```

---

# Browser Gemini Setup

For browser-only development:

1. Founder enters Gemini API key.
2. Key is stored in an HttpOnly cookie.
3. Backend retrieves the key.
4. FastAPI communicates with Gemini.

The key:

- Is not stored in source code.
- Is not committed to GitHub.
- Is not exposed to client JavaScript.

---

# Authentication Configuration

Development defaults:

```
APP_AUTH_PASSWORD=founder-pass

APP_SESSION_TOKEN=dev-antigravity-session-token

ANTIGRAVITY_INTERNAL_API_KEY=dev-antigravity-internal-key
```

These values are development-only.

Production environments must use:

- Secret Manager.
- Environment-specific credentials.
- Rotated secrets.

---

# Security Principles

MadeThis follows:

- Server-side secret management.
- Secure session handling.
- Environment-based configuration.
- Minimal client exposure.
- Provider abstraction.

---

# Cloud Deployment Strategy

Future Google Cloud architecture:

```
Google Cloud

|

+-- Cloud Run

+-- Cloud SQL

+-- Secret Manager

+-- Cloud Storage

+-- Vertex AI

+-- Monitoring
```

---

# Development Standards

Every feature must maintain:

## Type Safety

Avoid:

- Unnecessary any types.
- Unsafe casting.
- Ignored errors.

---

## Architecture Rules

Never place:

```
Business Logic
        |
        v
React Components
```

or:

```
Business Logic
        |
        v
API Routes
```

Correct:

```
Domain

    |

Application

    |

Infrastructure

    |

Presentation
```

---

# Quality Checks

Every milestone must pass:

```bash
npm run lint

npm run typecheck

npm run build

npm run check:api
```

---

# Git Workflow

Every milestone follows:

1. Create implementation changes.
2. Run quality checks.
3. Commit changes.
4. Push to GitHub.

Example:

```bash
git add .

git commit -m "feat: add agent registry system"

git push origin main
```

---

# Roadmap

## Phase 1: Intelligent Generation

Goals:

- Gemini reasoning workflows.
- Multi-agent execution.
- Business reports.
- Product scoring.

---

## Phase 2: Commerce Automation

Goals:

- Store integrations.
- Product publishing.
- Inventory management.
- Payment workflows.

---

## Phase 3: Marketing Automation

Goals:

- Social media agents.
- Advertising automation.
- Analytics.
- Growth optimization.

---

## Phase 4: Autonomous Companies

Goals:

- Real-time business monitoring.
- Automated decisions.
- Revenue optimization.
- Customer lifecycle management.

---

# Hackathon Objective

MadeThis is not designed as another AI wrapper.

The goal is to demonstrate a scalable autonomous business architecture where AI agents collaborate to perform real-world company operations.

The project explores a future where entrepreneurship becomes accessible through intelligent systems capable of transforming ideas into functioning businesses.

---

# License

MIT License
