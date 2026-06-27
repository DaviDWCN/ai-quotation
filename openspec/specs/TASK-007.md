# TASK-007: 系统集成网关 — OpenAPI 对接现有询报价系统 (Mock)

## Metadata

| Field       | Value                |
|-------------|----------------------|
| ID          | TASK-007             |
| Priority    | high                 |
| Depends On  | TASK-001, TASK-005   |
| Assigned To | unassigned           |
| Status      | backlog              |

---

## Objective

> 构建统一的系统集成网关（Integration Gateway），通过标准化接口对接"现有询报价系统"。由于现有系统 API 不可用，使用 Mock API 实现完整的对接流程验证。采用 Adapter 模式，后续可无缝切换为真实 API。

---

## Background & Context

- 架构设计要求"非侵入式对接（旁路模式）"
- 通过 OpenAPI 调用现有系统的 `CreateDraft`, `UpdateQuotation`, `SubmitQuotation` 等接口
- 若老系统不支持"智能草稿"状态，草稿暂存于本系统数据库，确认后一次性写入
- 现有系统 API 文档尚未提供，先用 Mock 实现完整流程

---

## Scope — Files Allowed to Modify

| File Path                                              | Action  |
|--------------------------------------------------------|---------|
| `packages/api/src/services/gateway/__init__.py`        | Create  |
| `packages/api/src/services/gateway/adapter.py`         | Create  |
| `packages/api/src/services/gateway/mock_adapter.py`    | Create  |
| `packages/api/src/services/gateway/client.py`          | Create  |
| `packages/api/src/services/gateway/schemas.py`         | Create  |
| `packages/api/src/services/gateway/sync_service.py`    | Create  |
| `packages/api/src/routers/gateway.py`                  | Create  |
| `packages/api/tests/test_gateway.py`                   | Create  |
| `packages/api/tests/test_gateway_sync.py`              | Create  |

---

## Acceptance Criteria

- [ ] AC-1: `GatewayAdapter` 抽象接口定义 `create_draft()`, `update_quotation()`, `submit_quotation()`, `get_status()`
- [ ] AC-2: `MockGatewayAdapter` 完整实现所有接口，使用内存存储模拟老系统行为
- [ ] AC-3: Mock 模拟真实延迟（200-500ms）和偶发错误（5% 概率返回 503）
- [ ] AC-4: 草稿确认后通过 Gateway 一次性推送到"现有系统"
- [ ] AC-5: 状态同步服务：定期拉取"现有系统"的单据状态并更新本地
- [ ] AC-6: Gateway 路由 `POST /api/gateway/submit/{draft_id}` 触发提交流程
- [ ] AC-7: 所有 Gateway 调用记录完整的审计日志（请求/响应/耗时）
- [ ] AC-8: 真实 API 地址和认证信息通过环境变量配置 (`LEGACY_SYSTEM_URL`, `LEGACY_API_KEY`)

---

## Verification Commands

```bash
cd packages/api
python -m pytest tests/test_gateway.py tests/test_gateway_sync.py -v --cov=src/services/gateway
mypy src/services/gateway/ --strict
```

---

## Notes for the Agent

- Adapter 模式是本项目的核心设计原则之一
- Mock Adapter 需要模拟足够真实的行为（延迟、偶发错误、状态流转）
- 真实 Adapter 预留 `httpx.AsyncClient` 调用位
- 审计日志使用 `structlog`
- 创建 branch: `jules/TASK-007/integration-gateway`
