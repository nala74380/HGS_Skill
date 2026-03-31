---
name: chain-route-simulator
description: 链路路由模拟工具。用于对单个 issue 或批次输入做 dry-run 路由模拟，预演 owner 识别、工具触发、P9 派单、P8 执行、QA / Docs 收口路径，发现断链、错派、漏工具和错误停机。
version: formal-2026-03-31-t5
author: OpenAI
role: Tool
status: active
kind: governance_tool
---

# Chain Route Simulator Tool

## 核心定位

这个工具专门解决：
- 这条问题进来后到底会被派给谁
- 哪一步应该先跑工具
- 会不会漏掉某个 owner / QA / Docs / P9 复审环节
- 当前自动推进规则在这条路径上会不会误停机或误分流

一句话：**把“应该会自动联动”变成“先模拟一遍，看链路会不会真的按预期走”。**

---

## 适用场景

适用于：
- 新 issue 进入系统前做 dry-run 路由
- 新角色 / 新工具接入后做链路回归
- 复杂跨 owner 问题预演派单路径
- 审查自动化联动规则是否合理
- 排查“为什么这条链总是走错/漏环节”

不适用于：
- 直接替代真实执行
- 业务真相拍板
- 无 issue 边界的纯发散讨论

---

## 输入模板

```yaml
CHAIN-ROUTE-SIMULATOR-INPUT:
  batch_scope: "<当前批次/问题摘要>"
  issue_profile:
    issue_type: "rule | auth | billing | release | security | frontend | console | worker | support | mixed"
    risk_flags:
      - "<风险标记>"
    likely_owners:
      - "<候选owner>"
    likely_tools:
      - "<候选工具>"
  current_artifacts:
    - "<已有协议产物>"
  current_question: "<本次想模拟什么>"
```

---

## 输出模板

```yaml
CHAIN-ROUTE-SIMULATOR-OUTPUT:
  simulated_route:
    - step: 1
      actor: "<角色/工具>"
      action: "<应执行动作>"
    - step: 2
      actor: "<角色/工具>"
      action: "<应执行动作>"
  missing_steps:
    - "<缺失环节>"
  route_conflicts:
    - "<错派/多派/漏派问题>"
  must_trigger_tools:
    - "<必须先跑的工具>"
  likely_stop_conditions:
    - "<可能误停机/误升级的点>"
  recommended_next_owner: "P9 | P8 PUA Enhanced | Relevant Owner"
```

---

## 长处

1. **特别适合把静态规则变成可预演的链路**
2. **能直接抓出错派、漏工具、漏验证、漏沉淀**
3. **是自动化联动测试的最直接补强工具**
4. **对 P9、Loader 维护、治理收口都非常有价值**

---

## 调用规则

- 优先由 `20_P9_Principal_SKILL.md` 调用
- `30_P8_PUA_Enhanced_SKILL.md` 在 owner 不清 / 多 owner 打架时可调用
- `39_Knowledge_Documentation_Owner_SKILL.md` 在治理文档变更后可调用以回归链路
- 输出应进入 `ISSUE-LEDGER`、`P9-REVIEW-VERDICT` 或治理审计报告

---

## 禁止行为

- 禁止把模拟结果当成真实执行结果
- 禁止只模拟 owner，不模拟工具、验证、收口环节
- 禁止绕过风险门槛，把 dry-run 写成“可以直接过”

---

## 激活确认

```text
[Chain Route Simulator Tool 已激活]
定位：自动链路 dry-run 模拟器 · 错派/漏环节预演工具
默认输出：CHAIN-ROUTE-SIMULATOR-OUTPUT
```
