# OpenSpec 集成与 Agent 协同工作指南

**OpenSpec** 是 `jules-team` 多智能体协同框架的声明式接口层。它通过在项目仓库中维护一组结构化的 Markdown 文档，实现**人机协同（Human-in-the-loop）**与**多智能体并发协同**。

本文档旨在指导开发者与 AI Agent 理解如何正确编写和使用 OpenSpec（包括任务清单 `tasks.md` 和任务描述 `specs/TASK-XXX.md`），以实现 Worker Agent 的自动触发、上下文隔离与安全执行。

---

## 1. 核心设计理念

1. **声明式状态机 (Declarative State)**
   所有的任务调度、依赖关系、执行状态和 PR 关联，都以文本形式记录在 `openspec/tasks.md` 中。框架（Master Orchestrator）通过解析该文件来驱动整个工作流。
2. **上下文隔离 (Context Isolation)**
   Worker Agent 在被触发执行某个任务时，不需要（也不应该）阅读整个项目的全部代码。它只需加载项目全局规则 `AGENTS.md` 以及该任务专属的 `openspec/specs/TASK-XXX.md` 描述文件。这极大地节省了 Token，并避免了无关上下文的干扰。
3. **Git-Ops 与审计可追踪 (Git-Ops & Auditability)**
   任务状态的每一次变更（如从 `backlog` 到 `in_progress` 再到 `done`）都会被 Master 自动提交并推送至 Git 仓库。所有协同过程公开、透明且随时可回滚。

---

## 2. 核心文件结构

在需要接入 `jules-team` 协同开发的目标项目中，必须在根目录及 `openspec` 目录下维护以下结构：

```text
目标项目/
├── AGENTS.md                    # 1. 全局 Agent 行为规范与技术栈定义 (SSOT)
└── openspec/
    ├── README.md                # 本指南
    ├── tasks.md                 # 2. 声明式任务清单（Kanban 看板）
    └── specs/                   # 3. 任务描述目录
        ├── _template.md         # 新任务 Spec 模板
        ├── TASK-001.md          # 任务 001 描述文件
        └── ...
```

---

## 3. 任务清单 `tasks.md` 规范

`tasks.md` 是协同框架的“指挥中心”，它由 **YAML Frontmatter** 和 **Markdown 任务看板** 两部分组成。

### 3.1 YAML Frontmatter (配置信息)
文件顶部必须包含 YAML 属性，用于定义项目基本信息：
```yaml
---
project: target-project-name     # 目标项目名称
repo: https://github.com/org/repo # 目标项目 GitHub 仓库地址
sprint: "2026-W27"               # 当前迭代周期/双周标识
---
```
> [!IMPORTANT]
> `repo` 必须是一个合法的 GitHub 仓库 URL，因为 Master Orchestrator 会据此向对应的 API 发送请求来触发 Agent 或查询 PR 状态。

### 3.2 任务列表语法与状态转换
任务列表通过 Markdown 的无序列表 `*` 或 `-` 配合复选框进行声明。每个任务必须严格遵循以下格式：

```markdown
- [ ] `TASK-001`: 修复 utils/validator.js 中的邮箱校验逻辑
  - assignee: unassigned
  - priority: high
  - depends_on: []
  - spec: specs/TASK-001.md
```

#### 语法要求：
1. **任务 ID 声明**：必须匹配 `^TASK-\d{3,}$` 正则表达式（例如：`TASK-001`, `TASK-002`），并用反引号 `` ` `` 包裹。
2. **任务标题**：紧跟在冒号 `:` 后面，简述任务内容。
3. **属性缩进**：任务行下方缩进 2 个空格，并以 `- 属性名: 属性值` 的形式声明。
   - `assignee`: 分配的 Agent 标识或 `unassigned`（未分配时填 `unassigned`，Master 派发后会更新为具体 Worker ID）。
   - `priority`: 优先级，可选值：`low`, `medium`, `high`, `critical`。
   - `depends_on`: 依赖的任务 ID 列表，格式为 `[TASK-001, TASK-002]`。无依赖则填 `[]`。
   - `spec`: 任务详情文件的相对路径，通常在 `specs/` 目录下。

#### 状态与复选框对应关系：
Master Orchestrator 会自动识别复选框中的字符，并将其映射为任务生命周期状态：
- `- [ ]` (未勾选)：代表 `backlog`（待办）、`failed`（失败）或 `needs_human`（需人工介入）。
- `- [/]` (斜杠)：代表 `in_progress`（开发中）或 `pr_submitted`（已提交 PR）。
- `- [x]` (已勾选)：代表 `done`（已完成）。

---

## 4. 任务描述 `specs/TASK-XXX.md` 规范

每个任务必须有且仅有一个对应的描述文件。该文件是 Worker Agent 的**唯一行动指南**，包含了任务执行的上下文和边界。

你可以从 [_template.md](file:///d:/workspace/jules-team/openspec/specs/_template.md) 复制并填写。一个标准的 Spec 文件包含以下部分：

### 4.1 任务元数据 (Metadata)
以 Markdown 表格形式重复声明基本状态，以便 Worker 校验：
```markdown
## Metadata

| Field       | Value        |
|-------------|--------------|
| ID          | TASK-001     |
| Priority    | high         |
| Depends On  | none         |
| Assigned To | unassigned   |
| Status      | backlog      |
```

### 4.2 任务目标与背景 (Objective & Context)
- **Objective**：用一到两句话明确阐述该任务的目标。
- **Background & Context**：提供所需的背景。例如：当前的行为是什么？预期的行为是什么？如果有相关的 Issue 链接或设计讨论，请在此贴出。

### 4.3 修改范围约束 (Scope — Files Allowed to Modify)
> [!CAUTION]
> **这是最核心的安全红线**。为了防止 AI Agent 产生幻觉或越权修改非相关文件，Worker Agent **绝对不允许**修改未列在 Scope 表格中的任何文件。

格式要求：
```markdown
## Scope — Files Allowed to Modify

| File Path                        | Action         |
|----------------------------------|----------------|
| `src/utils/validator.js`         | Modify         |
| `tests/utils/validator.test.js`  | Create / Modify|
```

### 4.4 验收标准 (Acceptance Criteria)
验收标准必须具体、可客观测试。避免使用模糊的词汇（如“优化性能”、“提高可读性”），而应使用：
- [ ] AC-1: 当邮箱格式不含 `@` 时，`validateEmail` 应当返回 `false`
- [ ] AC-2: 当邮箱包含特殊字符时，抛出特定的自定义错误 `ValidationError`
- [ ] AC-3: 确保所有修改过的代码均有对应的单元测试覆盖

### 4.5 验证命令 (Verification Commands)
在 Worker Agent 提交 Pull Request 之前，**必须**在隔离环境中运行并全部通过的本地命令：
```bash
# 运行单元测试
npm test

# 类型检查
npx tsc --noEmit

# 代码风格检查
npx eslint src/
```

---

## 5. 协同工作流与自动触发机制

当项目配置完毕并启动 `jules-team` 编排服务后，智能体之间将按照以下机制自动触发并协同工作：

```mermaid
graph TD
    Start((开始编排)) --> Parse[1. 解析 tasks.md]
    Parse --> DepCheck{2. 依赖解析 DAG}
    DepCheck -- 发现无依赖且未启动的 Backlog 任务 --> Dispatch[3. 派发任务]
    DepCheck -- 任务存在未完成依赖 --> Blocked[保持 Backlog / 等待]
    
    Dispatch --> CreateIssue[4. 在目标 Repo 创建 Issue<br>标题: '[TASK-001] ...'<br>标签: 'jules']
    CreateIssue --> AgentTriggered[5. Jules App 监听标签并启动 VM<br>拉取分支: jules/TASK-001/xxx]
    
    AgentTriggered --> AgentWork[6. Worker Agent 读取 AGENTS.md 和 Spec<br>修改 Scope 内 file 并运行验证命令]
    AgentWork --> CreatePR[7. Worker 提交代码并创建 PR]
    
    CreatePR --> Monitor[8. Master 监听到 PR 并更新 tasks.md<br>状态 -> '/'; 添加 pr 属性]
    Monitor --> Merge{9. CI 通过 & 人工/自动 Merge}
    Merge -- 已 Merge --> Complete[10. Master 更新 tasks.md 状态为 'x']
    Merge -- 失败/超时 --> Retry{11. 重试次数 < 2?}
    Retry -- Yes --> Reset[状态重置为 ' ' / 重新派发]
    Retry -- No --> NeedsHuman[12. 标记状态为 'needs_human' / 报警]
```

### 5.1 自动调度细节
1. **并发限制**：Master 默认最多同时启动 5 个并发的 Worker 任务（可在配置中调整），防止资源耗尽。
2. **熔断器 (Circuit Breaker)**：若连续 3 个任务在执行中抛出异常或失败，Master 将自动熔断（进入 `halted` 阶段）并停止派发后续任务，等待人工排查。
3. **超时控制 (Timeout)**：每个 Worker 任务的最长执行时间为 3 小时，超时将被 Master 自动销毁会话。

---

## 6. 给编写者的最佳实践 (Best Practices)

为确保 AI Agent 能 100% 成功地自主协同，任务设计者应遵循以下原则：

1. **小粒度解耦 (Atomicity)**：一个 `TASK-XXX` 只做一件事。如果一个需求既要改前端又要改后端，建议拆分为两个有依赖关系（`depends_on`）的小任务。
2. **严苛的修改范围 (Tight Scope)**：Scope 中只写必须修改的文件。尽量避免把整个文件夹（如 `src/**/*`）放入 Scope，这会大大增加 Agent 误改或引入 Bug 的概率。
3. **完善的测试守卫 (Test Guard)**：确保项目中具备基础的单元测试环境，并在 Spec 的 `Verification Commands` 中声明测试命令。Agent 会在提交 PR 前自动运行测试，不通过则不会提 PR，从而充当第一道质量关卡。
4. **避免硬编码敏感信息 (No Secrets)**：确保 Spec 中不包含任何真实的 API 密钥、数据库密码或私钥，防止泄露。

---

通过遵循本指南，你可以轻松使用 `openspec` 驱动整个智能体团队高效、安全地并发完成复杂的项目开发。
