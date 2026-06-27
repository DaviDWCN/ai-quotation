# TASK-005: 业务逻辑服务层 — 草稿生成 + 主数据匹配 + 通知推送

## Metadata

| Field       | Value                |
|-------------|----------------------|
| ID          | TASK-005             |
| Priority    | critical             |
| Depends On  | TASK-001             |
| Assigned To | unassigned           |
| Status      | backlog              |

---

## Objective

> 实现核心业务逻辑：MQ 消费 AI 解析结果 → 主数据智能模糊匹配（客户/物料）→ 生成草稿单据 → 触发通知推送。这是整个系统的业务枢纽。

---

## Background & Context

- 消费 AI 引擎输出的结构化数据（通过 RabbitMQ）
- 将 AI 提取的非标准名称与主数据进行模糊匹配
- 主数据样本将后续提供，当前使用 Mock 数据结构
- 匹配结果生成草稿单据存入 PostgreSQL
- 草稿生成后触发企微通知

---

## Scope — Files Allowed to Modify

| File Path                                              | Action  |
|--------------------------------------------------------|---------|
| `packages/api/src/services/draft/__init__.py`          | Create  |
| `packages/api/src/services/draft/service.py`           | Create  |
| `packages/api/src/services/draft/models.py`            | Create  |
| `packages/api/src/services/matching/__init__.py`       | Create  |
| `packages/api/src/services/matching/engine.py`         | Create  |
| `packages/api/src/services/matching/fuzzy.py`          | Create  |
| `packages/api/src/services/notification/__init__.py`   | Create  |
| `packages/api/src/services/notification/service.py`    | Create  |
| `packages/api/src/services/consumer.py`                | Create  |
| `packages/api/src/routers/drafts.py`                   | Create  |
| `packages/api/src/db/models.py`                        | Create  |
| `packages/api/src/db/session.py`                       | Create  |
| `packages/api/src/db/migrations/`                      | Create  |
| `packages/api/tests/test_draft_service.py`             | Create  |
| `packages/api/tests/test_matching_engine.py`           | Create  |
| `packages/api/tests/fixtures/mock_master_data.json`    | Create  |
| `packages/shared/types/master_data.py`                 | Modify  |
| `packages/shared/types/quotation.py`                   | Modify  |

---

## Acceptance Criteria

- [ ] AC-1: MQ 消费者从 `quotation.parse` 队列读取 AI 解析结果
- [ ] AC-2: `MatchingEngine.match_customer(name)` 返回 Top-N 候选客户及匹配分数
- [ ] AC-3: `MatchingEngine.match_material(code_or_name)` 返回 Top-N 候选物料
- [ ] AC-4: 匹配分数 ≥ 0.85 的自动绑定，< 0.85 的标记为 `needs_confirmation`
- [ ] AC-5: `DraftService.create_draft(parsed_data)` 生成草稿单据并存入 PostgreSQL
- [ ] AC-6: 草稿单据包含所有 AI 提取字段 + 匹配结果 + 置信度 + 缺失字段标记
- [ ] AC-7: REST API `GET /api/drafts`, `GET /api/drafts/{id}`, `PATCH /api/drafts/{id}` 可用
- [ ] AC-8: 草稿生成后自动触发通知推送（调用通知服务接口）
- [ ] AC-9: Mock 主数据（至少 10 条客户 + 20 条物料）用于测试匹配效果
- [ ] AC-10: 数据库迁移脚本可通过 Alembic 执行

---

## Verification Commands

```bash
cd packages/api
python -m pytest tests/test_draft_service.py tests/test_matching_engine.py -v --cov=src/services
mypy src/services/draft/ src/services/matching/ --strict
alembic upgrade head  # 验证数据库迁移
```

---

## Notes for the Agent

- 模糊匹配可使用 `rapidfuzz` 库（Levenshtein 距离 + token sort ratio）
- PostgreSQL 数据模型使用 SQLAlchemy 2.0 (async) + Alembic
- 草稿状态枚举：`draft` → `confirmed` → `submitted` → `completed`
- Mock 主数据 JSON 结构参考 `packages/shared/types/master_data.py`
- 通知服务只需定义接口，具体推送逻辑由 TASK-004 的企微模块实现
- 创建 branch: `jules/TASK-005/business-logic`
