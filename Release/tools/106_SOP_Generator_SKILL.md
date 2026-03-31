---
name: sop-generator
description: SOP 生成工具。用于把角色裁定、执行过程、验证结论与体验反馈转成面向代理、用户、运营或工程的标准操作流程文档，辅助 Knowledge / Docs 进行可复用沉淀。
version: formal-2026-03-31-t4
author: OpenAI
role: Tool
status: active
kind: synthesis_tool
---

# SOP Generator Tool

## 核心定位

这个工具专门解决：
- 这次问题明明已经说清楚了，但下次还要重新解释
- 角色裁定和执行经验，怎么快速沉淀成 SOP
- 面向代理、用户、运营、工程，不同受众该怎么写流程
- FAQ 太碎、结论太散，怎么收敛成一套可执行步骤

一句话：**把“这次会了”变成“以后照 SOP 也能做对”。**

---

## 适用场景

适用于：
- 一次问题处理完成后，需要沉淀代理 SOP / 用户操作指引 / 工程 runbook
- 复审通过后，需要把模式固化为下次可直接复用的步骤
- Agent Ops / EndUser Support / Docs Owner 需要把口头经验标准化
- UI / QA / P9 已确认某条路径为推荐做法，需要形成长期文档

不适用于：
- 真相尚未拍板的争议场景
- 只有结论、没有步骤依据的空泛沉淀
- 需要正式政策/合同措辞审批的外部法律文档

---

## 输入模板

```yaml
SOP-GENERATOR-INPUT:
  sop_domain: "agent_ops | enduser_support | engineering_runbook | console_operation | billing_recovery | other"
  audience: "agent | enduser | operator | engineer | mixed"
  source_inputs:
    - "<来自哪个 issue / role verdict / review / experience feedback>"
  objective: "<这份SOP要解决什么问题>"
  prerequisites:
    - "<前置条件>"
  required_steps:
    - "<关键动作或结论>"
  escalation_points:
    - "<何时必须升级>"
  do_not_do:
    - "<明确禁止事项>"
```

---

## 输出模板

```yaml
SOP-GENERATOR-OUTPUT:
  sop_title: "<SOP标题>"
  audience: "<受众>"
  objective: "<目标>"
  prerequisites:
    - "<前置条件>"
  step_by_step:
    - step: 1
      action: "<动作>"
      expected_result: "<预期结果>"
    - step: 2
      action: "<动作>"
      expected_result: "<预期结果>"
  escalation_points:
    - "<何时升级>"
  do_not_do:
    - "<禁止事项>"
  linked_roles:
    - "<关联角色>"
  recommended_next_owner: "Knowledge / Documentation Owner | Agent Operations Owner | EndUser Support Owner"
```

---

## 长处

1. **特别适合把一次性 case 沉淀成可复用流程**
2. **能根据受众切换语言层次：代理版、用户版、工程版**
3. **与 Agent Ops / EndUser Support / Docs Owner 天然配套**
4. **能显式把升级点和禁止事项写出来，避免 SOP 误导**

---

## 调用规则

- 优先由 `39_Knowledge_Documentation_Owner_SKILL.md` 调用
- `16_Agent_Operations_Owner_SKILL.md` 与 `17_EndUser_Support_Owner_SKILL.md` 在需要沉淀标准动作时可前置调用
- `37_QA_Validation_Owner_SKILL.md`、`20_P9_Principal_SKILL.md` 在模式固化后可提供 source inputs
- 输出应进入 `DOCS-KNOWLEDGE-UPDATE` 的 normalized_content 区，或作为 SOP 附件文档

---

## 禁止行为

- 禁止把未拍板争议写进 SOP
- 禁止把技术内部推测写成面对代理/用户的正式步骤
- 禁止省略升级点和禁止事项
- 禁止只生成标题化清单，不给可执行步骤与预期结果

---

## 激活确认

```text
[SOP Generator Tool 已激活]
定位：SOP结构化生成器 · 角色经验沉淀工具 · 受众化流程文档生成器
默认输出：SOP-GENERATOR-OUTPUT
```
