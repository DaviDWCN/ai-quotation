---
project: ai-quotation
repo: https://github.com/DaviDWCN/ai-quotation
sprint: "2026-W27"
---

# Sprint Tasks — 智能询报价系统

## Backlog

- [x] `TASK-001`: 项目脚手架搭建 — Monorepo 结构 + 基础设施 + AGENTS.md
  - assignee: unassigned
  - priority: critical
  - depends_on: []
  - spec: specs/TASK-001.md
  - pr: https://github.com/DaviDWCN/ai-quotation/pull/1

- [ ] `TASK-002`: AI 多模态解析引擎 — 从 Dify demo 迁移为独立 Python 服务
  - assignee: unassigned
  - priority: critical
  - depends_on: [TASK-001]
  - spec: specs/TASK-002.md

- [ ] `TASK-003`: 邮件监听服务 — IMAP 轮询 + 附件下载 + MQ 投递
  - assignee: unassigned
  - priority: high
  - depends_on: [TASK-001, TASK-002]
  - spec: specs/TASK-003.md

- [ ] `TASK-004`: 企微机器人服务 — WebHook 回调 + 消息处理 + 卡片推送
  - assignee: unassigned
  - priority: high
  - depends_on: [TASK-001, TASK-002]
  - spec: specs/TASK-004.md

- [ ] `TASK-005`: 业务逻辑服务层 — 草稿生成 + 主数据匹配 + 通知推送
  - assignee: unassigned
  - priority: critical
  - depends_on: [TASK-001]
  - spec: specs/TASK-005.md

- [ ] `TASK-006`: 人机协同前端 — 企微 H5 轻应用 + PC 端审核界面
  - assignee: unassigned
  - priority: medium
  - depends_on: [TASK-005]
  - spec: specs/TASK-006.md

- [ ] `TASK-007`: System Integration Gateway — OpenAPI 对接现有询报价系统 (Mock)
  - assignee: unassigned
  - priority: high
  - depends_on: [TASK-001, TASK-005]
  - spec: specs/TASK-007.md

## In Progress

<!-- Tasks are moved here automatically by the Master Orchestrator when dispatched -->

## Done

<!-- Completed tasks are archived here with PR links -->
