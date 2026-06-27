# TASK-004: 企微机器人服务 — WebHook 回调 + 消息处理 + 卡片推送

## Metadata

| Field       | Value                |
|-------------|----------------------|
| ID          | TASK-004             |
| Priority    | high                 |
| Depends On  | TASK-001, TASK-002   |
| Assigned To | unassigned           |
| Status      | backlog              |

---

## Objective

> 实现企业微信机器人 WebHook 回调服务，处理来自企微群/私聊的询价消息和文件，通过 MQ 投递给 AI 引擎，并能推送审批卡片消息给业务员。使用 Mock API 进行开发测试。

---

## Background & Context

- 接入层第二个输入渠道：企业微信机器人
- 企微 API 凭据尚未提供，使用 Mock WebHook 和 Mock 推送服务
- 业务员可直接在企微中向机器人发送消息或文件进行询价
- 处理完成后需推送审批卡片，包含一键跳转链接

---

## Scope — Files Allowed to Modify

| File Path                                          | Action  |
|----------------------------------------------------|---------|
| `packages/api/src/services/wecom/__init__.py`      | Create  |
| `packages/api/src/services/wecom/webhook.py`       | Create  |
| `packages/api/src/services/wecom/message.py`       | Create  |
| `packages/api/src/services/wecom/card_push.py`     | Create  |
| `packages/api/src/services/wecom/adapter.py`       | Create  |
| `packages/api/src/services/wecom/mock_wecom.py`    | Create  |
| `packages/api/src/routers/wecom_callback.py`       | Create  |
| `packages/api/tests/test_wecom_webhook.py`         | Create  |
| `packages/api/tests/test_wecom_card_push.py`       | Create  |

---

## Acceptance Criteria

- [ ] AC-1: FastAPI 路由 `POST /api/wecom/callback` 可接收企微 WebHook 回调
- [ ] AC-2: 支持处理文本消息、文件消息、图片消息三种类型
- [ ] AC-3: 文件消息的附件自动下载并存储到文件存储
- [ ] AC-4: 解析后的消息通过 MQ Adapter 投递到 `quotation.parse` 队列
- [ ] AC-5: `send_approval_card(user_id, draft_id)` 推送审批卡片消息
- [ ] AC-6: 企微接口使用 Adapter 模式 (`WeComAdapter` + `MockWeComAdapter`)
- [ ] AC-7: Mock 模式下全流程可测试（回调 → 解析 → MQ → 卡片推送）
- [ ] AC-8: WebHook 签名验证逻辑（Mock 模式可跳过）

---

## Verification Commands

```bash
cd packages/api
python -m pytest tests/test_wecom_webhook.py tests/test_wecom_card_push.py -v --cov=src/services/wecom
mypy src/services/wecom/ --strict
```

---

## Notes for the Agent

- 企微 API 文档参考: https://developer.work.weixin.qq.com/document/
- 所有外部调用走 Adapter，方便后续切换真实 API
- 卡片消息模板需包含：草稿单号、客户名称、物料摘要、一键跳转 URL
- 基于会话 ID (conversation_id) 做幂等性控制
- 创建 branch: `jules/TASK-004/wecom-bot`
