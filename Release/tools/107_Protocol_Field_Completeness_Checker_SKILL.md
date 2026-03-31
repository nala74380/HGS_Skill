---
name: protocol-field-completeness-checker
description: 协议字段完整性检查工具。用于检查 ISSUE、VERDICT、EXEC、QA、DOCS 等协议产物字段是否缺失、错位、悬空或未落点，辅助 P9 / QA / Docs 保证链路产物可复审、可追踪、可收口。
version: formal-2026-03-31-t5
author: OpenAI
role: Tool
status: active
kind: governance_tool
---

# Protocol Field Completeness Checker Tool

## 核心定位

这个工具专门解决：
- 为什么 issue 看起来做了很多，但没有完整协议产物
- 为什么工具结果分析完了，却没有落到协议字段
- 为什么 P8 说修完了，但 `P8-EXEC-REPORT` 缺关键字段
- 为什么 QA / Docs / P9 在收口时发现 evidence、verdict、closeout 对不上

一句话：**把“格式像有了”变成“协议字段真的齐了、能复审、能闭环”。**

---

## 适用场景

适用于：
- `ISSUE-LEDGER` 完整性检查
- `P8-EXEC-REPORT` 字段缺失检查
- `QA-VALIDATION-PLAN` / `QA-VERIFICATION-RESULT` 字段完整性检查
- `BUSINESS-RULE-DECISION` / `IDENTITY-DECISION` / `BILLING-VERDICT` 等 owner 输出完整性检查
- `DOCS-KNOWLEDGE-UPDATE` / `HGS-CLOSEOUT` 收口字段检查

不适用于：
- 业务规则真相拍板
- 身份真相拍板
- 单纯的文档润色

---

## 输入模板

```yaml
PROTOCOL-FIELD-CHECKER-INPUT:
  protocol_type: "ISSUE-LEDGER | P8-EXEC-REPORT | QA-VALIDATION-PLAN | QA-VERIFICATION-RESULT | BUSINESS-RULE-DECISION | IDENTITY-DECISION | BILLING-VERDICT | RELEASE-CONFIG-VERDICT | SECURITY-RISK-VERDICT | CONTROL-PLANE-VERDICT | EXECUTION-PLANE-VERDICT | AGENT-OPS-VERDICT | ENDUSER-SUPPORT-VERDICT | DOCS-KNOWLEDGE-UPDATE | HGS-CLOSEOUT"
  current_payload: "<当前协议内容，可为文本或结构化对象>"
  expected_required_fields:
    - "<必须字段1>"
    - "<必须字段2>"
  downstream_expectations:
    - "<后续角色/协议依赖什么字段>"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
PROTOCOL-FIELD-CHECKER-OUTPUT:
  protocol_type: "<协议类型>"
  completeness_result: "complete | partial | incomplete | misaligned"
  missing_fields:
    - "<缺失字段>"
  weak_fields:
    - field: "<字段名>"
      issue: "empty | vague | not_actionable | not_traceable"
  orphan_results:
    - "<有结果但没落点的内容>"
  downstream_risks:
    - "<会导致复审/验证/沉淀失败的风险>"
  recommended_next_owner: "P9 | QA / Validation Owner | Knowledge / Documentation Owner"
```

---

## 长处

1. **特别适合在 closeout 前做协议质量总审**
2. **能显式抓出“分析有了，但没落到字段”这类隐性断链**
3. **对 P9、QA、Docs 都非常高频**
4. **是把静态治理真正变成可检查治理的关键工具**

---

## 调用规则

- 优先由 `20_P9_Principal_SKILL.md` 调用
- `37_QA_Validation_Owner_SKILL.md` 在验证收口时可调用
- `39_Knowledge_Documentation_Owner_SKILL.md` 在 SOP / Closeout 沉淀前可调用
- 输出应进入 `P9-REVIEW-VERDICT`、`QA-VERIFICATION-RESULT` 或 `DOCS-KNOWLEDGE-UPDATE`

---

## 禁止行为

- 禁止把字段齐全误当成问题已解决
- 禁止只检查字段名，不检查字段是否可执行、可追踪
- 禁止跳过 downstream expectation，导致“当前完整、下游不可用”

---

## 激活确认

```text
[Protocol Field Completeness Checker Tool 已激活]
定位：协议字段完整性审计器 · 结果落点检查器 · closeout前质量闸门
默认输出：PROTOCOL-FIELD-CHECKER-OUTPUT
```
