# ai-quotation Monorepo

## Project Identity
- **Name**: ai-quotation
- **Description**: Monorepo for the AI Quotation System.
- **Backend Stack**: Python, FastAPI, LiteLLM
- **Frontend Stack**: TypeScript, Next.js (React), App Router
- **Database/MQ/Storage**: PostgreSQL, RabbitMQ, MinIO
- **Shared Code**: Pydantic v2 models, Adapter patterns for MQ.

## Build Commands
- **Backend**: `cd packages/api && pip install -e ".[dev]"`
- **Frontend**: `cd packages/web && npm install && npm run build`
- **Docker**: `docker compose config --quiet`
- **Type Checking**: `cd packages/api && mypy src/ --strict`
- **Testing**: `cd packages/api && python -m pytest tests/ -v`

## Forbidden Modifying Files
- DO NOT MODIFY this `AGENTS.md` without explicit instruction.
