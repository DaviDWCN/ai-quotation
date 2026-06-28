# TASK-009: 统一 QuotationDraft 模型与修复 AI 解析数据流

## Metadata

| Field       | Value                |
|-------------|----------------------|
| ID          | TASK-009             |
| Priority    | critical             |
| Depends On  | TASK-008             |
| Assigned To | unassigned           |
| Status      | backlog              |

---

## Objective

> 解决 `QuotationDraft` 模型在实例化时的 Pydantic 校验错误，并将 AI 提取模块（`parse_quotation_request`）集成到 MQ 消费者逻辑中，打通“原始消息输入 -> AI 结构化提取 -> 模糊匹配 -> 草稿保存”的完整后台业务流程。

---

## Background & Context

- 核心数据模型 [quotation.py](file:///d:/workspace/ai-quotation/packages/shared/types/quotation.py) 中的 `QuotationDraft` 包含一个嵌套的 `parsed_data: ParsedQuotation` 对象。
- 目前，AI 解析引擎的 `convert_to_quotation_draft` 函数试图使用扁平字段（如 `customer_name`）直接创建 `QuotationDraft`，这在 [test_ai_parser.py](file:///d:/workspace/ai-quotation/packages/api/tests/test_ai_parser.py) 的测试运行中触发了校验异常导致失败。
- 此外，邮件监听和企微服务向队列投递的是原始 payload（如 `body_text`, `attachments`），而 MQ 消费者 [consumer.py](file:///d:/workspace/ai-quotation/packages/api/src/services/consumer.py) 却直接尝试解析为 AI 提取完的对象。必须串联 AI 解析逻辑以弥合这一架构断裂。

---

## Scope — Files Allowed to Modify

| File Path                                          | Action |
|----------------------------------------------------|--------|
| `packages/api/src/ai/parser.py`                    | Modify |
| `packages/api/src/services/consumer.py`            | Modify |
| `packages/api/tests/test_ai_parser.py`             | Modify |

---

## Acceptance Criteria

- [ ] AC-1: 重构 [parser.py](file:///d:/workspace/ai-quotation/packages/api/src/ai/parser.py) 中的 `convert_to_quotation_draft`，将 AI 提取的各字段值（`customer_name`, `segmentation`, `items`, `delivery_date`, `remarks`）正确包裹并实例化为嵌套的 `ParsedQuotation` 赋给 `QuotationDraft.parsed_data`
- [ ] AC-2: 修复 [test_ai_parser.py](file:///d:/workspace/ai-quotation/packages/api/tests/test_ai_parser.py) 中的单元测试并使其全部通过（尤其是 `test_convert_to_quotation_draft`）
- [ ] AC-3: 在 [consumer.py](file:///d:/workspace/ai-quotation/packages/api/src/services/consumer.py) 中引入并整合 `parse_quotation_request`。当收到包含原始邮件/消息内容的数据包时，先调用 AI 引擎进行提取，随后将提取出的 `ExtractedQuotation` 结果赋给后续匹配流程
- [ ] AC-4: 确保消费者在执行 AI 解析失败或 validation 报错时能正确打印异常并按照系统设计抛出，以便消息队列进行重试或落入死信队列
- [ ] AC-5: `python -m pytest tests/test_ai_parser.py tests/test_draft_service.py` 均完全通过

---

## Verification Commands

在提交 PR 之前运行以下命令：

```bash
# 运行 AI 解析引擎相关测试
cd packages/api
$env:PYTHONPATH="d:\workspace\ai-quotation;d:\workspace\ai-quotation\packages\shared"
python -m pytest tests/test_ai_parser.py tests/test_draft_service.py -v

# 类型检查与 Lint
mypy src/ai/ src/services/consumer.py --strict
```

---

## Notes for the Agent

- 在 `consumer.py` 中，调用 `parse_quotation_request` 时需要传入 `email_content`（若消息来自邮件）或 `chat_text`（若来自企微）。附件需要适配为包含 `(bytes, filename)` 的列表传给解析器。
