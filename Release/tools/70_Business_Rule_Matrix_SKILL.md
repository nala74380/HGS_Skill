---
name: business-rule-matrix
description: 业务规则矩阵工具。用于把模糊业务口径转成结构化规则矩阵，辅助 Business Rules Owner、P9 与相关执行角色统一判定口径。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Business Rule Matrix Tool

## 发布版装配位置

- 运行层级：`tools/70_Business_Rule_Matrix_SKILL.md`
- 本文件是 **工具型 Skill**，不是角色 Skill
- 不替代 Product / Business Rules Owner 拍板，只负责把争议压成可裁定的规则矩阵

---

## 核心定位

这个工具专门解决：

- 业务规则说不清
- 规则口径分散在聊天、文档、代码和经验里
- 同一问题不同人有不同理解
- P9 无法把问题结构化派单

一句话：**把“大家觉得应该是这样”变成“条件-结果-动作-owner”的规则矩阵。**

---

## 适用场景

适用于：
- 账号状态含义不清
- 激活 / 名额 / 换机 / 重装规则不清
- 自助动作边界不清
- 平台 / 代理 / 用户权责不清
- 某异常到底算正常例外还是规则漏洞不清

不适用于：
- 纯代码 bug 定位
- 纯 UI 表现问题
- 纯账务流水核对

---

## 输入模板

```yaml
BUSINESS-RULE-MATRIX-INPUT:
  rule_domain: "account_status | activation | renewal | entitlement | self_service | other"
  current_question: "<当前争议问题>"
  known_facts:
    - "<已知事实1>"
    - "<已知事实2>"
  candidate_rules:
    - "<候选规则1>"
    - "<候选规则2>"
  actors:
    - "platform"
    - "agent"
    - "enduser"
  exception_cases:
    - "<已知例外>"
  source_of_truth:
    - "<相关文档/接口/历史规则>"
```

---

## 输出模板

```yaml
BUSINESS-RULE-MATRIX-OUTPUT:
  rule_domain: "<领域>"
  normalized_question: "<压缩后的核心问题>"
  rule_matrix:
    - condition: "<条件>"
      expected_result: "<判定结果>"
      owner_of_action: "platform | agent | enduser | mixed"
      allowed_action:
        - "<允许动作>"
      forbidden_action:
        - "<禁止动作>"
  unresolved_conflicts:
    - "<仍有冲突的点>"
  recommended_owner: "Product / Business Rules Owner"
  downstream_impacts:
    - "<影响的角色/模块>"
```

---

## 典型长处

1. **擅长把口水争论压成表格**
2. **擅长发现条件缺失和例外未定义**
3. **擅长把“谁来处理”同步列出来**
4. **非常适合进入 `BUSINESS-RULE-DECISION` 前置分析**

---

## 调用规则

- 优先由 `11_Product_Business_Rules_Owner_SKILL.md` 调用
- P9 在发现规则不清、无法直接拆单时可先调用
- 调用后不得直接宣布规则成立，必须交 Owner 裁定
- 若结果仍存在关键冲突，升级给 P10 或 Product Owner

---

## 禁止行为

- 禁止替代 Business Rules Owner 最终拍板
- 禁止把工程现状直接当业务规则
- 禁止输出“视情况而定”这类未矩阵化结果

---

## 激活确认

```text
[Business Rule Matrix Tool 已激活]
定位：规则争议压缩器 · 条件/结果矩阵生成器 · owner归属辅助器
默认输出：BUSINESS-RULE-MATRIX-OUTPUT
```
