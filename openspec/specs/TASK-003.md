# TASK-003: 邮件监听服务 — IMAP 轮询 + 附件下载 + MQ 投递

## Metadata

| Field       | Value                |
|-------------|----------------------|
| ID          | TASK-003             |
| Priority    | high                 |
| Depends On  | TASK-001, TASK-002   |
| Assigned To | unassigned           |
| Status      | backlog              |

---

## Objective

> 实现 IMAP 邮箱轮询服务，自动监听公共询价邮箱中的新邮件，下载附件，通过消息队列（RabbitMQ Adapter）投递给 AI 解析引擎处理。使用 Mock 邮箱服务器进行开发测试。

---

## Background & Context

- 接入层第一个输入渠道：企业邮箱 (IMAP/POP3)
- 邮箱连接信息尚未提供，使用 Mock IMAP 服务器进行开发
- 去重逻辑基于 `Message-ID` 头的幂等性控制
- 附件需上传到 MinIO/S3 文件存储

---

## Scope — Files Allowed to Modify

| File Path                                       | Action  |
|-------------------------------------------------|---------|
| `packages/api/src/services/mail/__init__.py`    | Create  |
| `packages/api/src/services/mail/listener.py`    | Create  |
| `packages/api/src/services/mail/parser.py`      | Create  |
| `packages/api/src/services/mail/adapter.py`     | Create  |
| `packages/api/src/services/mail/mock_imap.py`   | Create  |
| `packages/api/src/services/file_storage.py`     | Create  |
| `packages/api/tests/test_mail_listener.py`      | Create  |
| `packages/api/tests/fixtures/sample_email.eml`  | Modify  |

---

## Acceptance Criteria

- [ ] AC-1: `MailListener` 类可以连接 IMAP 服务器并轮询 INBOX
- [ ] AC-2: 邮件解析提取：发件人、收件人、主题、正文(HTML/Plain)、附件列表
- [ ] AC-3: 附件自动下载并上传到文件存储（MinIO adapter）
- [ ] AC-4: 基于 `Message-ID` 的幂等性去重，重复邮件不再处理
- [ ] AC-5: 解析完成的邮件数据通过 MQ Adapter 投递到 `quotation.parse` 队列
- [ ] AC-6: `MockIMAPServer` 可在无真实邮箱情况下完成完整流程测试
- [ ] AC-7: 邮件监听器使用 Adapter 模式 (`MailAdapter` 接口 + `IMAPAdapter` + `MockAdapter`)
- [ ] AC-8: 异常邮件（解析失败、附件过大）进入死信队列，不阻断主流程

---

## Verification Commands

```bash
cd packages/api
python -m pytest tests/test_mail_listener.py -v --cov=src/services/mail
mypy src/services/mail/ --strict
```

---

## Notes for the Agent

- 邮件解析使用 Python 标准库 `email` 模块
- 附件存储使用 `boto3` (S3 兼容接口，适用于 MinIO)
- MQ 投递使用 TASK-001 建立的 `MQAdapter` 接口
- 轮询间隔可配置（默认 30 秒）
- 创建 branch: `jules/TASK-003/mail-listener`
