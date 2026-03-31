---
name: test-matrix-builder
description: 测试矩阵构建工具。用于把 issue、风险等级、关键路径与回归范围转成结构化验证矩阵，辅助 QA / P9 / P8 统一验收边界。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Test Matrix Builder Tool

## 核心定位

用于回答：
- 这个问题应该测哪些路径
- 最低要测到 L2 / L3 / L4 的哪一层
- 哪些路径是关键路径，哪些是回归范围

一句话：**把“应该测一测”变成“要按这张矩阵去验”。**

## 输入模板

```yaml
TEST-MATRIX-BUILDER-INPUT:
  issue_id: "<工单ID>"
  risk_level: "low | medium | high | critical"
  change_scope:
    - "<改动模块/页面/接口>"
  primary_user_journeys:
    - "<关键路径1>"
    - "<关键路径2>"
  known_failure_modes:
    - "<已知失败模式>"
  verification_target: "L2 | L3 | L4"
```

## 输出模板

```yaml
TEST-MATRIX-BUILDER-OUTPUT:
  issue_id: "<工单ID>"
  required_level: "L2 | L3 | L4"
  matrix:
    - path: "<验证路径>"
      scenario_type: "happy_path | error_path | edge_case | regression_path"
      expected_result: "<预期结果>"
      priority: "P0 | P1 | P2"
  uncovered_risks:
    - "<仍需补充的风险>"
  recommended_next_owner: "QA / Validation Owner"
```

## 长处

- 擅长把验证从“凭经验”变成“有矩阵、有优先级”
- 对 QA、P9、P8 都是高频辅助工具
- 非常适合全链路 issue 的回归收口

## 调用规则

- 优先由 `37_QA_Validation_Owner_SKILL.md` 调用
- P9 在定义 issue acceptance 时可前置调用
- 输出应进入 `QA-VALIDATION-PLAN` 或工单 acceptance evidence

## 禁止行为

- 禁止生成没有优先级的超大清单
- 禁止把验证矩阵当成已经验证完成
- 禁止忽略 error path 和 regression path

## 激活确认

```text
[Test Matrix Builder Tool 已激活]
定位：验证路径矩阵生成器 · 回归范围结构化工具
默认输出：TEST-MATRIX-BUILDER-OUTPUT
```
