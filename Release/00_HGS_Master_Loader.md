---
name: hgs-master-loader
description: HGS 运行时 6 常驻 + 4 按需唤起主装配器。用于 ChatGPT Thinking + GitHub 场景的最小强运行集正式入口。
version: formal-2026-04-02-runtime6-main-v1
author: OpenAI
role: MasterLoader
status: active
entrypoint: true
---

# HGS Master Loader / 主装配器（Runtime6 默认）

本文件的职责只有一件事：**把 HGS 从“23 角色全量常驻”切换为“6 个常驻角色 + 4 个按需唤起角色”的正式运行链路，并继续保留门禁、工具、协议、复审、清零与文档沉淀能力。**

---

## 激活方式

正式发布版激活时，必须同时读取：

1. `MANIFEST.json`
2. `00_HGS_Master_Loader.md`
3. `roles/21_Lead_Orchestrator_SKILL.md`
4. `roles/22_Policy_Domain_Owner_SKILL.md`
5. `roles/23_Identity_Security_Owner_SKILL.md`
6. `roles/24_Platform_Owner_SKILL.md`
7. `roles/25_Execution_Lead_SKILL.md`
8. `roles/26_Validation_Owner_SKILL.md`
9. `tools/` 下已纳入 manifest 的全部工具 Skill
10. `protocols/40_P8_Agent_Experience_Protocol.md`
11. `protocols/41_P8_EndUser_Experience_Protocol.md`
12. `protocols/50_RE_REVIEW_PROTOCOL.md`
13. `protocols/60_HGS_IO_Protocol.md`
14. `protocols/61_Automation_Orchestration_Protocol.md`
15. `protocols/62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md`
16. `docs/角色调用关系总表.md`
17. `docs/角色-工具矩阵总表.md`
18. `docs/角色边界验证台账.md`
19. `docs/工具调用关系总表.md`
20. `docs/HGS_自动化联动动作总表（正式版）.md`
21. `docs/HGS_自动化联动装配后复核（评分驱动版）.md`
22. `docs/HGS_全量问题发现—全量派单—持续回流直到清零协议_装配后复核.md`
23. `docs/HGS_全局检查与清理评分报告.md`
24. `docs/HGS_全局扣分点问题清单与派单台账.md`
25. `docs/HGS_角色整合与最小强运行集方案.md`

### 按需唤起角色（不是默认常驻）

以下角色**不进入默认每轮全量常驻装配**，但在命中对应 issue_type、证据面或升级条件时必须按需读取：

- `roles/27_Frontend_Console_Specialist_SKILL.md`
- `roles/28_Operations_Support_Owner_SKILL.md`
- `roles/29_Documentation_Sink_SKILL.md`
- `roles/10_P10_CTO_SKILL.md`

说明：

- 第 16~18 项属于角色治理底册，不得遗漏
- 第 20~24 项属于自动化、清零、审计与台账底册，不得遗漏
- 第 25 项属于 Runtime6 角色整合底册，不得遗漏

---

## 装配目标

默认路线固定为：

```text
全局审查
→ 全量发现问题
→ 全量登记 issue
→ 全量派单
→ 由 Lead Orchestrator 组织真相 Owner / 执行 / 验证
→ 必要时唤起 Frontend / Console 或 Operations / Support
→ 测试 / 回归 / 体验 / 可观测
→ 全量复审
→ 新问题继续登记并继续派单
→ 持续回流直到 open_issue_count = 0
→ Docs 沉淀
→ Closeout
