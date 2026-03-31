---
name: p8-pc-console-legacy
description: 旧版 PC Console 综合执行角色。已被 33A_Console_Runtime_Engineer 与 33B_Console_Management_Experience_Engineer 拆分取代，仅保留历史追溯用途，不纳入正式装配。
version: formal-2026-03-31-legacy1
author: OpenAI
role: LegacyP8
status: legacy
---

# 33_P8_PCConsole_PUA_SKILL（Legacy Stub）

## 当前状态

本文件**已降权为历史存根文件**，不再是正式发布版装配集的一部分。

- 不在 `Release/MANIFEST.json` 的 `load_order` 中
- 不在 `Release/MANIFEST.json` 的 `roles` 列表中
- 不应作为当前会话中的 PC Console 执行角色被加载

---

## 替代关系

旧的“PC Console 综合执行角色”已经拆分为两个正式角色：

1. `roles/33A_P8_Console_Runtime_Engineer_SKILL.md`
   - 负责：ConsoleToken、project context、step-up 恢复、登出清理、管理动作运行逻辑

2. `roles/33B_P8_Console_Management_Experience_Engineer_SKILL.md`
   - 负责：管理台信息层级、可发现性、高风险动作反馈、错误/空态/限制态设计

---

## 保留原因

保留本文件仅用于：

- 历史追溯
- 对照旧版 Console 职责拆分路径
- 帮助维护者理解为什么 Console 被拆成 `Runtime + Management Experience`

---

## 禁止事项

- 禁止把本文件重新加入正式装配链
- 禁止把本文件与 `33A/33B` 并行当作 active role 使用
- 禁止基于本文件继续扩写新规则或新执行约束

---

## 迁移结论

当前正式 Console 执行链以以下两个文件为准：

```text
33A_P8_Console_Runtime_Engineer_SKILL.md
33B_P8_Console_Management_Experience_Engineer_SKILL.md
```

本文件到此停止演进。
