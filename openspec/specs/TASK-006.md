# TASK-006: 人机协同前端 — 企微 H5 轻应用 + PC 端审核界面

## Metadata

| Field       | Value                |
|-------------|----------------------|
| ID          | TASK-006             |
| Priority    | medium               |
| Depends On  | TASK-005             |
| Assigned To | unassigned           |
| Status      | backlog              |

---

## Objective

> 构建两个前端界面：企微 H5 轻应用（移动端快速审核）和 PC 端深度审核界面（左右分栏对比），实现草稿查看、缺失信息高亮提示、人工补充填写、确认提交的完整 Human-in-the-Loop 流程。

---

## Background & Context

- 架构设计要求：当 AI 提取信息不全或匹配置信度低时，阻断自动提交，生成"待确认草稿"
- 移动端 H5 嵌入企微，支持从审批卡片一键跳转
- PC 端支持左右分栏：左侧预览原始邮件/附件，右侧编辑结构化表单
- 表单应基于元数据驱动，不同 Segmentation 的必填字段可能不同
- 技术栈：Next.js (App Router)

---

## Scope — Files Allowed to Modify

| File Path                                                | Action  |
|----------------------------------------------------------|---------|
| `packages/web/src/app/layout.tsx`                        | Create  |
| `packages/web/src/app/page.tsx`                          | Create  |
| `packages/web/src/app/drafts/page.tsx`                   | Create  |
| `packages/web/src/app/drafts/[id]/page.tsx`              | Create  |
| `packages/web/src/app/drafts/[id]/review/page.tsx`       | Create  |
| `packages/web/src/app/mobile/drafts/page.tsx`            | Create  |
| `packages/web/src/app/mobile/drafts/[id]/page.tsx`       | Create  |
| `packages/web/src/components/DraftList.tsx`               | Create  |
| `packages/web/src/components/DraftForm.tsx`               | Create  |
| `packages/web/src/components/SplitViewReview.tsx`         | Create  |
| `packages/web/src/components/FilePreview.tsx`             | Create  |
| `packages/web/src/components/ConfidenceBadge.tsx`         | Create  |
| `packages/web/src/components/MissingFieldAlert.tsx`       | Create  |
| `packages/web/src/hooks/useDraft.ts`                      | Create  |
| `packages/web/src/lib/api.ts`                             | Create  |
| `packages/web/src/styles/globals.css`                     | Create  |

---

## Acceptance Criteria

- [ ] AC-1: 草稿列表页展示所有待审核草稿（按状态分组、时间排序）
- [ ] AC-2: 置信度低的字段显示 `ConfidenceBadge`（黄色/红色标记）
- [ ] AC-3: 缺失的必填字段显示红色高亮框 + `MissingFieldAlert` 提示
- [ ] AC-4: PC 端 `SplitViewReview` 组件：左侧文件预览 + 右侧表单编辑
- [ ] AC-5: 移动端 H5 页面适配 375px 宽度，可在企微内嵌浏览器正常使用
- [ ] AC-6: 表单提交前校验所有必填字段已填写，阻止空字段提交
- [ ] AC-7: "确认提交" 按钮调用后端 `PATCH /api/drafts/{id}` 更新状态
- [ ] AC-8: 页面响应式设计，PC/移动端自适应布局

---

## Verification Commands

```bash
cd packages/web
npm install
npm run build  # Next.js 编译无错误
npm run lint    # ESLint 无错误
```

---

## Notes for the Agent

- 使用 Next.js 14+ App Router
- API 调用使用 `fetch` + 环境变量 `NEXT_PUBLIC_API_URL`
- 移动端和 PC 端可共用组件库，通过 media query 区分布局
- 文件预览（PDF/Excel）可使用 `react-pdf` 或 iframe 嵌入
- 样式使用 CSS Modules 或 Vanilla CSS，不使用 Tailwind
- UI 设计要求：现代、专业，使用清晰的状态颜色编码
- 创建 branch: `jules/TASK-006/human-review-frontend`
