---
name: state-machine-consistency
description: 状态机一致性工具。用于对比业务规则、接口状态、前后端实现与文档中的状态定义，识别缺失跳转、非法状态、命名漂移与逻辑断裂。
version: formal-2026-03-31-t2
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# State Machine Consistency Tool

## 核心定位

这个工具专门解决：
- 同一个概念在不同模块里状态名不一样
- 状态跳转不完整
- 业务上不该存在的状态在工程里出现了
- 文档、接口、前端、后端各自维护了一套状态机

一句话：**把“状态混乱”拆成可检查、可定位、可复审的状态机一致性问题。**

---

## 适用场景

适用于：
- account_status / entitlement_status / activation_status / task_status 等状态定义不清
- 前端、后端、文档、运营口径不一致
- 某个状态能到但不该到，或该跳转却跳不过去
- P9 复审发现命名漂移或状态闭环断裂

不适用于：
- 纯视觉问题
- 纯账务流水核对
- 没有任何状态样本时的空泛讨论

---

## 输入模板

```yaml
STATE-MACHINE-CONSISTENCY-INPUT:
  state_domain: "account | activation | entitlement | billing | task | custom"
  expected_state_machine:
    states:
      - "<状态1>"
      - "<状态2>"
    transitions:
      - from: "<状态A>"
        to: "<状态B>"
        condition: "<条件>"
  observed_state_machine:
    states:
      - "<实际状态1>"
      - "<实际状态2>"
    transitions:
      - from: "<实际状态A>"
        to: "<实际状态B>"
        condition: "<实际条件>"
  sources:
    - "<文档/接口/代码/页面来源>"
```

---

## 输出模板

```yaml
STATE-MACHINE-CONSISTENCY-OUTPUT:
  state_domain: "<领域>"
  consistency_result: "consistent | partial_drift | drift | unclear"
  findings:
    missing_states:
      - "<缺失状态>"
    unexpected_states:
      - "<异常状态>"
    missing_transitions:
      - "<缺失跳转>"
    illegal_transitions:
      - "<非法跳转>"
    naming_drift:
      - "<命名漂移>"
  likely_owner_of_truth: "Product / Business Rules Owner"
  downstream_owners:
    - "P9"
    - "Backend"
    - "Frontend Logic"
```

---

## 长处

1. **特别擅长抓“名字差不多但语义不一样”的问题**
2. **非常适合 Product / P9 / Backend / Frontend Logic 共用**
3. **能把状态争议从感觉层拉回结构层**
4. **适合进入复审和模式固化**

---

## 调用规则

- Product / Business Rules Owner 在定义状态真相时可前置调用
- P9 在审查、复审、再审阶段高频可用
- Backend / Frontend Logic 在发现状态不一致时可先调用
- 输出不得直接替代最终规则拍板，应进入 `BUSINESS-RULE-DECISION` 或 `P9-REVIEW-VERDICT`

---

## 禁止行为

- 禁止把工程里已有状态直接视为业务真相
- 禁止只比状态名，不比状态跳转条件
- 禁止无来源对比，只凭记忆构造状态机

---

## 激活确认

```text
[State Machine Consistency Tool 已激活]
定位：状态定义一致性检查器 · 跳转闭环审查器 · 命名漂移发现器
默认输出：STATE-MACHINE-CONSISTENCY-OUTPUT
```
