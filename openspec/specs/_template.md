# TASK-XXX: [One-line task title]

## Metadata

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | TASK-XXX                       |
| Priority    | high / medium / low / critical |
| Depends On  | TASK-YYY, TASK-ZZZ (or none)  |
| Assigned To | unassigned                     |
| Status      | backlog                        |

---

## Objective

> A clear, one-paragraph description of what this task accomplishes and why it matters.

---

## Background & Context

Provide any relevant context the worker agent needs to understand:
- What is the current behavior?
- What is the expected behavior?
- Links to issues, discussions, or related PRs.

---

## Scope — Files Allowed to Modify

> **IMPORTANT**: The worker agent MUST NOT modify any files outside this list.

| File Path                        | Action         |
|----------------------------------|----------------|
| `src/utils/validator.js`         | Modify         |
| `tests/utils/validator.test.js`  | Create / Modify|

---

## Acceptance Criteria

- [ ] AC-1: [Specific, testable condition]
- [ ] AC-2: [Specific, testable condition]
- [ ] AC-3: All existing tests still pass

---

## Verification Commands

The worker agent **MUST** run these commands and confirm they pass before submitting a PR:

```bash
# Run unit tests
npm test

# Type check
npx tsc --noEmit

# Lint
npx eslint src/
```

---

## Notes for the Agent

- Read `AGENTS.md` at the repo root for global coding conventions.
- Follow the commit message format: `fix(validator): <description>`
- Create a branch named: `jules/TASK-XXX/<short-description>`
