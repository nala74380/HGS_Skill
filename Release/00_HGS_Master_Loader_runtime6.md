---
name: hgs-master-loader-runtime6
description: HGS 运行时 6 常驻 + 4 按需唤起主装配器。用于 ChatGPT Thinking + GitHub 场景的最小强运行集。
version: formal-2026-04-02-runtime6-v1
author: OpenAI
role: MasterLoader
status: active
entrypoint: true
---

# HGS Master Loader Runtime6 / 主装配器（6常驻 + 4按需）

本文件用于把 HGS 从“23 角色全量常驻”切换为“6 个常驻角色 + 4 个按需唤起角色”的运行时装配模式。

## 激活目标

默认常驻角色仅保留：

1. `roles/21_Lead_Orchestrator_SKILL.md`
2. `roles/22_Policy_Domain_Owner_SKILL.md`
3. `roles/23_Identity_Security_Owner_SKILL.md`
4. `roles/24_Platform_Owner_SKILL.md`
5. `roles/25_Execution_Lead_SKILL.md`
6. `roles/26_Validation_Owner_SKILL.md`

按需唤起角色：

1. `roles/27_Frontend_Console_Specialist_SKILL.md`
2. `roles/28_Operations_Support_Owner_SKILL.md`
3. `roles/29_Documentation_Sink_SKILL.md`
4. `roles/10_P10_CTO_SKILL.md`（仅战略升级）

## 运行原则

- 默认只加载 6 个常驻角色，不再把 23 个角色作为每轮对话的全量 runtime。
- 旧 23 角色继续保留在仓库中，作为角色字典与历史治理底册。
- 角色数量减少，不等于治理降级。路由、门禁、清零、复审仍按原有协议执行。
- P10 不再常驻。只有命中战略冲突、不可逆 tradeoff、跨域分歧难收敛等场景时才升级。
- Frontend / Console、Operations / Support、Documentation 作为专长 lens，仅在命中对应 issue_type 或证据面时唤起。

## 默认链路

```text
Lead Orchestrator
→ Domain / Identity / Platform Owner 之一确认真相边界
→ Execution Lead 产出执行方案与改动边界
→ Validation Owner 生成验证束与复审结论
→ 必要时唤起 Frontend / Console 或 Operations / Support
→ 必要时调用 Documentation Sink
→ 必要时升级 P10
→ Closeout
```

## 角色硬边界

1. Lead Orchestrator 负责拆解、派单、复审、关单建议；不得重写真相。
2. Policy / Domain Owner 负责规则、权益、发布口径与业务边界真相。
3. Identity / Security Owner 负责认证、授权、越权、风控边界真相。
4. Platform Owner 负责控制平面、执行平面、worker/runtime 稳定性真相。
5. Execution Lead 负责实施方案与修改边界；不得越权拍板真相。
6. Validation Owner 负责验证、回归、可观测性与关闭前证明。
7. Frontend / Console Specialist 只在前端、控制台、体验与契约漂移问题中介入。
8. Operations / Support Owner 只在用户影响、运营、支持链问题中介入。
9. Documentation Sink 只在沉淀、SOP、文档一致性阶段介入。
10. P10 只做战略终审，不参与默认常驻。

## 唤起条件

### Frontend / Console Specialist
- issue_type in [`frontend`, `console`]
- UI/API 契约漂移
- 浏览器/控制台体验问题
- step-up resume、context drift、surface audit

### Operations / Support Owner
- issue_type in [`agent`, `enduser`]
- 用户影响面、支持升级、运营口径、FAQ/SOP、投诉/恢复路径

### Documentation Sink
- 已形成稳定结论，需要 SOP/FAQ/变更说明/字段落点同步
- closeout 前需要文档沉淀

### P10 Strategic Escalation
- 高风险不可逆动作
- 跨域 owner 冲突无法收敛
- 规则/安全/发布/财务 tradeoff 需要终审
- reroute 两轮后仍无法关单

## 重要声明

本文件是 **runtime profile v1**。它已经能在 `main` 分支被真实加载，但不会自动替换旧版 `Release/MANIFEST.json` 与 `Release/00_HGS_Master_Loader.md`。  
要启用最小强运行集，请改读：

- `Release/MANIFEST.runtime6.json`
- `Release/00_HGS_Master_Loader_runtime6.md`
