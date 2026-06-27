# AI Quotation System

A monorepo for the AI Quotation System.

## Structure
- `packages/api/`: Python FastAPI backend.
- `packages/web/`: Next.js React frontend.
- `packages/shared/`: Shared types and messaging adapters.

## Setup
1. Copy `.env.example` to `.env` and fill in the values.
2. Run `docker compose up -d` to start infrastructure.
3. Start backend: `cd packages/api && uvicorn src.main:app --reload`.
4. Start frontend: `cd packages/web && npm run dev`.
