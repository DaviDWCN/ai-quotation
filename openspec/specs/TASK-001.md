# TASK-001: 项目脚手架搭建 — Monorepo 结构 + 基础设施 + AGENTS.md

## Metadata

| Field       | Value                |
|-------------|----------------------|
| ID          | TASK-001             |
| Priority    | critical             |
| Depends On  | (none)               |
| Assigned To | unassigned           |
| Status      | backlog              |

---

## Objective

> 在 GitHub 仓库 `DaviDWCN/ai-quotation` 中搭建 Monorepo 结构，配置开发环境和共享基础设施，建立 `AGENTS.md` 全局规约。这是所有后续任务的基石。

---

## Background & Context

- 技术栈已确认：后端 Python FastAPI, 前端 Next.js (React), 消息队列 RabbitMQ (adapter 模式), 数据库 PostgreSQL, AI 调用 LiteLLM, 文件存储 MinIO/S3
- 项目源于一个 Dify advanced-chat workflow demo（已完成概念验证），现需升级为完整的工程化系统
- 架构设计文档参考仓库 Wiki 或 Issue 中的架构设计描述

---

## Scope — Files to Create

| File Path                              | Action  |
|----------------------------------------|---------|
| (仓库根目录)                           | Create  |
| `AGENTS.md`                            | Create  |
| `README.md`                            | Create  |
| `docker-compose.yml`                   | Create  |
| `.gitignore`                           | Create  |
| `.env.example`                         | Create  |
| `packages/api/pyproject.toml`          | Create  |
| `packages/api/src/__init__.py`         | Create  |
| `packages/api/src/config.py`           | Create  |
| `packages/api/src/main.py`             | Create  |
| `packages/api/tests/conftest.py`       | Create  |
| `packages/web/package.json`            | Create  |
| `packages/web/tsconfig.json`           | Create  |
| `packages/shared/types/quotation.py`   | Create  |
| `packages/shared/types/master_data.py` | Create  |
| `packages/shared/mq/__init__.py`       | Create  |
| `packages/shared/mq/adapter.py`        | Create  |
| `packages/shared/mq/rabbitmq.py`       | Create  |

---

## Acceptance Criteria

- [ ] AC-1: 仓库根目录包含完整 Monorepo 结构 (`packages/api`, `packages/web`, `packages/shared`)
- [ ] AC-2: `AGENTS.md` 包含项目身份、技术栈、构建命令、禁止修改文件列表
- [ ] AC-3: `docker-compose.yml` 可以 `docker compose up -d` 启动 PostgreSQL + RabbitMQ + MinIO
- [ ] AC-4: FastAPI 后端 `packages/api/` 可以 `uvicorn` 启动并返回健康检查
- [ ] AC-5: Next.js 前端 `packages/web/` 可以 `npm run dev` 启动
- [ ] AC-6: 消息队列使用 Adapter 模式 (`MQAdapter` 接口 + `RabbitMQAdapter` 实现)
- [ ] AC-7: 共享类型定义 `QuotationDraft`, `Customer`, `Material` 已建立
- [ ] AC-8: `.env.example` 包含所有必要的环境变量模板

---

## Verification Commands

```bash
# 后端启动
cd packages/api && pip install -e ".[dev]" && python -m pytest tests/ -v

# 前端启动
cd packages/web && npm install && npm run build

# Docker 基础设施
docker compose config --quiet  # 验证配置语法

# 类型检查
cd packages/api && mypy src/ --strict
```

---

## Notes for the Agent

- 消息队列 **必须使用 Adapter 模式**：定义 `MQAdapter` 抽象接口，实现 `RabbitMQAdapter`。后续可扩展 Kafka/Redis Streams
- `AGENTS.md` 参考 `d:\workspace\jules-team\AGENTS.md` 的格式，但内容适配 ai-quotation 项目
- 共享类型使用 Pydantic v2 models
- FastAPI 入口 `main.py` 只需包含健康检查端点 (`/healthz`)
- Next.js 使用 App Router 模式
