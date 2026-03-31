---
name: p8-frontend-legacy
description: 旧版前台综合执行角色。已被 32A_UI_Surface_Engineer 与 32B_Frontend_Logic_Engineer 拆分取代，仅保留历史追溯用途，不纳入正式装配。
version: formal-2026-03-31-legacy1
author: OpenAI
role: LegacyP8
status: legacy
---

# 32_P8_Frontend_PUA_SKILL（Legacy Stub）

## 当前状态

本文件**已降权为历史存根文件**，不再是正式发布版装配集的一部分。

- 不在 `Release/MANIFEST.json` 的 `load_order` 中
- 不在 `Release/MANIFEST.json` 的 `roles` 列表中
- 不应作为当前会话中的前台执行角色被加载

---

## 替代关系

旧的“前台综合执行角色”已经拆分为两个正式角色：

1. `roles/32A_P8_UI_Surface_Engineer_SKILL.md`
   - 负责：界面表面质量、信息层级、状态反馈、组件一致性、响应式体验

2. `roles/32B_P8_Frontend_Logic_Engineer_SKILL.md`
   - 负责：状态管理、路由上下文、请求编排、权限表达、竞态与 contract 消费

---

## 保留原因

保留本文件仅用于：

- 历史追溯
- 对照旧版本前台职责拆分路径
- 帮助维护者理解为什么 Frontend 被拆成 `UI Surface + Logic`

---

## 禁止事项

- 禁止把本文件重新加入正式装配链
- 禁止把本文件与 `32A/32B` 并行当作 active role 使用
- 禁止基于本文件继续扩写新规则或新执行约束

---

## 迁移结论

当前正式前台执行链以以下两个文件为准：

```text
32A_P8_UI_Surface_Engineer_SKILL.md
32B_P8_Frontend_Logic_Engineer_SKILL.md
```

本文件到此停止演进。
