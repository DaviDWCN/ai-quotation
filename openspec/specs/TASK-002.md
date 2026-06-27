# TASK-002: AI 多模态解析引擎 — 从 Dify Demo 迁移为独立 Python 服务

## Metadata

| Field       | Value                |
|-------------|----------------------|
| ID          | TASK-002             |
| Priority    | critical             |
| Depends On  | TASK-001             |
| Assigned To | unassigned           |
| Status      | backlog              |

---

## Objective

> 将 Dify demo（`商险询报价.yml`）的核心 AI 提取逻辑迁移为独立的 Python 模块，实现多模态文档解析 + LLM 结构化信息提取 + 置信度评分。完全用代码替代 Dify。

---

## Background & Context

### Dify Demo 分析

Dify workflow 核心流程：
1. **文档提取器 1** (`sys.files`): 提取上传附件的文本内容
2. **文档提取器 2** (`email` 变量): 提取邮件正文的文本内容
3. **LLM** (DeepSeek R1-0528, temperature=0.7): 接收 `用户查询 + 邮件内容JSON + 附件内容`，输出结构化结果

### 正式版增强要求

- **System Prompt**：Dify demo 的 system prompt 为空，正式版需要精心设计结构化提取 prompt
- **温度**：从 0.7 降到 0.1-0.3 以提高提取稳定性
- **输出校验**：添加 Pydantic model 强制校验 LLM 输出 JSON
- **置信度**：对每个提取字段标记置信度分数（high/medium/low）
- **多格式支持**：PDF, Excel, Word, 图片 OCR

---

## Scope — Files Allowed to Modify

| File Path                                          | Action  |
|----------------------------------------------------|---------|
| `packages/api/src/ai/__init__.py`                  | Create  |
| `packages/api/src/ai/parser.py`                    | Create  |
| `packages/api/src/ai/prompts.py`                   | Create  |
| `packages/api/src/ai/document_extractor.py`        | Create  |
| `packages/api/src/ai/schemas.py`                   | Create  |
| `packages/api/src/ai/confidence.py`                | Create  |
| `packages/api/tests/test_ai_parser.py`             | Create  |
| `packages/api/tests/test_document_extractor.py`    | Create  |
| `packages/api/tests/fixtures/sample_email.eml`     | Create  |
| `packages/api/tests/fixtures/sample_quotation.pdf` | Create  |
| `packages/shared/types/quotation.py`               | Modify  |

---

## Acceptance Criteria

- [ ] AC-1: `parse_quotation_request(email_file, chat_text)` 函数返回结构化 `QuotationDraft` 对象
- [ ] AC-2: LLM 使用 LiteLLM 调用，兼容 DeepSeek R1 和其他 OpenAI-compatible 模型
- [ ] AC-3: System prompt 明确定义提取字段（客户名称, Segmentation, 物料型号, 数量, 目标价等）和 JSON 输出 schema
- [ ] AC-4: 每个提取字段附带置信度分数 (`confidence: high | medium | low`)
- [ ] AC-5: 缺失的必填字段标记为 `missing: true`，不阻断流程但高亮警告
- [ ] AC-6: 支持至少 3 种文档格式解析（PDF, Excel, 纯文本）
- [ ] AC-7: LLM 输出通过 Pydantic model 严格校验，格式异常时自动重试一次
- [ ] AC-8: 单元测试覆盖率 ≥ 80%

---

## Verification Commands

```bash
cd packages/api
python -m pytest tests/test_ai_parser.py tests/test_document_extractor.py -v --cov=src/ai
mypy src/ai/ --strict
```

---

## Notes for the Agent

- **核心参考**: Dify workflow 位于同级目录下的 `商险询报价.yml`
- AI 调用使用 `litellm.acompletion()` 而非直接调用 openai SDK
- 文档提取可使用 `pypdf`, `openpyxl`, `python-docx` 等库
- 提取的字段至少包括：
  - `customer_name` (客户名称)
  - `segmentation` (产品线/业务分类)
  - `items[]` (物料明细列表)
    - `material_code` (物料编码/型号)
    - `quantity` (需求数量)
    - `target_price` (目标价)
    - `unit` (单位)
  - `delivery_date` (期望交期)
  - `remarks` (备注)
- 温度设为 0.2（可通过配置调整）
- 创建 branch: `jules/TASK-002/ai-parser-engine`
