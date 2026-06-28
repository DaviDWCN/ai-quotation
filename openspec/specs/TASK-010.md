# TASK-010: 修复前后端草稿模型不匹配与注册集成网关路由

## Metadata

| Field       | Value                |
|-------------|----------------------|
| ID          | TASK-010             |
| Priority    | high                 |
| Depends On  | TASK-009             |
| Assigned To | unassigned           |
| Status      | backlog              |

---

## Objective

> 解决前后端草稿（Draft）数据模型不匹配导致的 Next.js 前端运行时崩溃，并注册标准集成网关（Gateway）路由，使外部能够通过 `/api/gateway/submit/{draft_id}` 触发询报价单据提交流程。

---

## Background & Context

- 移动端和 PC 端审核界面使用 `draft.fields` 展示提取出的各字段信息并收集人工输入。
- 然而，后端数据库及 [routers/drafts.py](file:///d:/workspace/ai-quotation/packages/api/src/routers/drafts.py) 返回的是包含 `parsed_data`（JSON 嵌套结构）和 `material_matches` 列表的直接模型。前端由于读取不到 `draft.fields` 属性会直接抛出运行期 `TypeError` 并崩溃。
- 系统网关路由器 [gateway.py](file:///d:/workspace/ai-quotation/packages/api/src/routers/gateway.py) 已建立，但是忘记导入并注册到 [main.py](file:///d:/workspace/ai-quotation/packages/api/src/main.py)，导致相关接口根本无法被访问。

---

## Scope — Files Allowed to Modify

| File Path                                          | Action |
|----------------------------------------------------|--------|
| `packages/api/src/main.py`                         | Modify |
| `packages/api/src/routers/drafts.py`               | Modify |
| `packages/web/src/lib/api.ts`                      | Modify |
| `packages/web/src/hooks/useDraft.ts`               | Modify |
| `packages/web/src/components/DraftForm.tsx`        | Modify |
| `packages/web/src/components/DraftList.tsx`        | Modify |

---

## Acceptance Criteria

- [ ] AC-1: 在 [main.py](file:///d:/workspace/ai-quotation/packages/api/src/main.py) 中导入并注册 `gateway_router` 模块，配置前缀为 `/api/gateway`，确保外部可以使用 `POST /api/gateway/submit/{draft_id}` 接口
- [ ] AC-2: 解决前后端数据结构失配问题。建议做法：修改后端 [routers/drafts.py](file:///d:/workspace/ai-quotation/packages/api/src/routers/drafts.py)，使 `DraftDetail` 和 `DraftSummary` 响应体包含一个虚拟的/动态拼装好的 `fields` 字典，该字典包含 `customer_name`、`segmentation` 等草稿字段，格式与前端 `DraftField` 契约一致
- [ ] AC-3: 前端 React 组件与 Hooks（`DraftList`、`DraftForm`、`useDraft` 等）能无报错地读取并正确绑定草稿属性
- [ ] AC-4: 确保前端能够成功执行 `npm run build` 和 `npm run lint` 且全绿通过，没有任何 TypeScript 报错
- [ ] AC-5: 后端网关相关测试用例 `tests/test_gateway.py` 成功运行

---

## Verification Commands

在提交 PR 之前运行以下命令：

```bash
# 后端测试与类型检查
cd packages/api
$env:PYTHONPATH="d:\workspace\ai-quotation;d:\workspace\ai-quotation\packages\shared"
python -m pytest tests/test_gateway.py tests/test_health.py -v
mypy src/ --strict

# 前端编译与 Lint
cd ../web
npm run build
npm run lint
```

---

## Notes for the Agent

- 拼装 `fields` 字段时，应当合并 AI 提取结果的置信度信息。例如，`fields["customer_name"]` 的 `confidence` 应读取自数据库里存的 AI 提取置信度，而 `value` 为其真实提取值。
- 后端 gateway 路由的 prefix 和 tags 配置要规范，避免出现 `/api/gateway/api/gateway/submit` 的嵌套路由前缀。
