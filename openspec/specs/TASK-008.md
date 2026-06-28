# TASK-008: 修复配置项缺失与环境依赖问题

## Metadata

| Field       | Value                |
|-------------|----------------------|
| ID          | TASK-008             |
| Priority    | critical             |
| Depends On  | (none)               |
| Assigned To | unassigned           |
| Status      | backlog              |

---

## Objective

> 修复因 `src/config.py` 配置项缺失导致的 `AttributeError`，并在 `pyproject.toml` 中补全所有在实际代码中已导入但未声明的依赖项；同时解决 `PYTHONPATH` 导入路径引起的 `ModuleNotFoundError` 报错，确保测试用例和环境能顺利通过编译及运行。

---

## Background & Context

- 邮件监听服务（[listener.py](file:///d:/workspace/ai-quotation/packages/api/src/services/mail/listener.py)）和文件存储等模块在加载或运行时需要访问 `Settings` 的各项参数（如 `settings.mail_poll_interval`、`settings.imap_host`、`settings.s3_endpoint` 等）。
- 现有的 `src/config.py` 中遗漏了这些字段的声明，这导致在执行 `python -m pytest` 时连导入阶段都会直接崩溃。
- 项目中多处跨包导入使用 `from packages.shared...` 或 `from mq...`。如果不调整导入路径或者补充配置，Worker 无法在标准测试命令下成功验证。

---

## Scope — Files Allowed to Modify

| File Path                                       | Action |
|-------------------------------------------------|--------|
| `packages/api/src/config.py`                    | Modify |
| `packages/api/pyproject.toml`                   | Modify |
| `packages/api/src/services/mail/listener.py`    | Modify |
| `.env.example`                                  | Modify |

---

## Acceptance Criteria

- [ ] AC-1: 在 [config.py](file:///d:/workspace/ai-quotation/packages/api/src/config.py) 中增加所有缺失的业务字段配置默认值（含 `mail_poll_interval`, `mq_dead_letter_topic`, `mail_max_attachment_size`, `mq_quotation_parse_topic` 以及所有 `imap_*` 和 `s3_*` 配置属性）
- [ ] AC-2: 在 [pyproject.toml](file:///d:/workspace/ai-quotation/packages/api/pyproject.toml) 的依赖中补全 `xmltodict`、`pypdf`、`openpyxl`、`python-docx`、`boto3` 以及 `structlog`，确保执行 `pip install -e ".[dev]"` 后无需手动安装其他包
- [ ] AC-3: 修复 [listener.py](file:///d:/workspace/ai-quotation/packages/api/src/services/mail/listener.py) 中 `from mq.adapter` 的导入错误，改为 `from packages.shared.mq.adapter` 形式
- [ ] AC-4: 更新根目录的 `.env.example`，提供对应的业务配置占位说明（如 `IMAP_HOST`、`S3_ENDPOINT` 等项）
- [ ] AC-5: 在 `PYTHONPATH` 包含根目录时，API 模块所有的测试用例在测试收集阶段不再有任何 `ImportError` 或 `AttributeError`，且除 AI 转换外的其他单元测试全部通过

---

## Verification Commands

在提交 PR 之前运行以下命令：

```bash
# 后端依赖安装
cd packages/api
pip install -e ".[dev]"

# 环境变量设置与测试运行 (Windows CMD/Powershell 适配)
# Powershell:
$env:PYTHONPATH="d:\workspace\ai-quotation;d:\workspace\ai-quotation\packages\shared"
python -m pytest tests/ --ignore=tests/test_ai_parser.py -v

# 类型检查与 Lint
mypy src/ --strict
```

---

## Notes for the Agent

- `Settings` 的新增属性应考虑合理的默认值（例如 `mail_poll_interval` 默认为 30 秒，`mail_max_attachment_size` 默认为 10MB 等）。
- mypy 类型检查需要全绿通过。
