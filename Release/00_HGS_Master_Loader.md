---
name: hgs-master-loader
description: HGS 正式发布版主装配器。负责装配 Manifest、角色 Skill、工具 Skill、治理文档、自动编排协议与其他协议 Skill，并按统一状态机驱动全链路。
version: formal-2026-03-31-int5
author: OpenAI
role: MasterLoader
status: active
entrypoint: true
---

# HGS Master Loader / 主装配器

本文件不是“替代所有角色”的超级单体 Skill。  
本文件的职责只有一件事：**把多角色、多工具、自动化动作、统一协议、治理文档正式装配成一条可自动推进、可审计、可重开环的标准链路。**

---

## 激活方式

正式发布版激活时，必须同时读取：

1. `MANIFEST.json`
2. `00_HGS_Master_Loader.md`
3. `roles/` 下已纳入 manifest 的全部角色 Skill
4. `tools/` 下已纳入 manifest 的全部工具 Skill
5. `protocols/` 下全部协议文件
6. `docs/角色调用关系总表.md`
7. `docs/工具调用关系总表.md`
8. `docs/HGS_自动化联动动作总表（正式版）.md`

说明：

- `docs/正式发布版全局审查报告.md` 与 `docs/发布说明与加载方式.md` 属于基线与操作文档，应在装配阶段被视为背景约束
- `protocols/61_Automation_Orchestration_Protocol.md` 定义自动化动作的输入输出骨架
- 治理文档不是“执行角色”，但对角色调用顺序、工具优先级、动作闸门具有约束力

---

## 装配目标

默认路线固定为：

```text
P10 战略初判（仅必要时）
  ↓
真相 Owner 识别
  ↓
P9 审查与派单
  ↓
P8 按 owner 执行
  ↓
体验验证（代理 / 终端用户 / 路径复演）
  ↓
QA / SRE / 体验证据收口
  ↓
P9 复审
  ↓
P10 终审（仅必要时）
  ↓
Knowledge / Docs 沉淀
  ↓
收口 / 再开环
```

本版新增的核心能力：

- 自动化动作驱动入口标准化
- 自动化动作驱动 owner 自救 / 平级协商 / 重派单
- 自动化动作驱动工具闸门与字段落点检查
- 自动化动作驱动执行报告、验证包与 closeout 候选检查

---

## 装配顺序

```text
MANIFEST
→ Master Loader
→ 战略 / 真相 / Owner 层
→ P9 审查层
→ P8 Enhanced（兜底约束先就位）
→ P8 专项执行层
→ Tool Skills
→ Automation Orchestration Protocol
→ Experience Protocols
→ Re-Review Protocol
→ I/O Protocol
→ Governance Docs
```

说明：
- `P8_PUA_Enhanced` 提前装配，是为了让升级接管规则从一开始生效
- `tools/` 在执行前装配，是为了保证先结构化分析、再拍板、再执行
- `protocols/61_Automation_Orchestration_Protocol.md` 在协议层中前置，是为了让自动化动作记录与字段落点先有统一骨架

---

## 自动化动作装配清单（第一批 + 第二批 active）

当前正式激活的动作包括：

### 第一批
1. `create_issue_stub`
2. `infer_owner_candidates`
3. `infer_required_tools`
4. `route_dry_run`
5. `provisional_boundary_build`
6. `peer_role_consult`
7. `split_subissues`
8. `must_run_tool_gate`
9. `tool_result_landing_check`
10. `closeout_candidate_check`

### 第二批
11. `owner_self_resolve_attempt`
12. `fallback_to_p8_enhanced`
13. `p9_reframe_and_redispatch`
14. `autofill_exec_report`
15. `generate_validation_bundle`

这些动作的详细输入输出以：
- `docs/HGS_自动化联动动作总表（正式版）.md`
- `protocols/61_Automation_Orchestration_Protocol.md`

为准。

---

## 自动化动作执行顺序（当前 active）

### 入口标准化序列
```text
create_issue_stub
→ infer_owner_candidates
→ infer_required_tools
→ route_dry_run（当 owner_confidence 低 / mixed issue / route 不稳）
→ provisional_boundary_build（当边界暂不精确）
```

### 内部协商与重派单序列
```text
owner_self_resolve_attempt
→ peer_role_consult（当当前 owner 自救不足）
→ split_subissues（当 mixed issue / 多 owner 交叉依赖）
→ fallback_to_p8_enhanced（当失败次数过多 / owner 不稳 / 路由碎裂）
→ p9_reframe_and_redispatch（当需要重构 issue / 改派 / 重排工具顺序）
```

### 工具闸门序列
```text
must_run_tool_gate
→ tool_result_landing_check
```

### 执行与验证序列
```text
P8 执行
→ autofill_exec_report
→ generate_validation_bundle
→ tool_result_landing_check
```

### 收口闸门序列
```text
closeout_candidate_check
→ 通过则 reviewing / docs_sink
→ 不通过则 reopen_required / reroute_required
```

---

## 评分与闸门阈值

当前采用以下默认阈值：
- `owner_confidence_min_for_direct_dispatch = 70`
- `tool_coverage_min_before_review = 85`
- `evidence_completeness_min_before_review = 80`
- `closeout_readiness_min_before_done = 85`
- `reopen_risk_high = 60`

硬规则：
- 未创建 `ISSUE-LEDGER stub` 不得派单
- `owner_confidence < 70` 时必须先跑 `108`
- 工具前置场景中 `must_run_tools` 未完成不得派单
- 重复失败时必须升级 `fallback_to_p8_enhanced`
- 无 `P8-EXEC-REPORT` 不得进入 review
- 无 `validation bundle` 不得进入 review
- 工具结果未落字段不得进入 review / done
- 未通过 `closeout_candidate_check` 不得进入 `done`

---

## 按动作驱动路由

- owner 低置信 / mixed issue / route 不稳 → `route_dry_run`
- 边界不清但可非破坏性推进 → `provisional_boundary_build`
- 当前 owner 应先内部自救 → `owner_self_resolve_attempt`
- 多 owner 交叉依赖 → `peer_role_consult` → `split_subissues`
- 重复失败 / 路由碎裂 / 需要兜底 → `fallback_to_p8_enhanced`
- 新真相出现 / 需改派 / 需重排执行顺序 → `p9_reframe_and_redispatch`
- 命中工具前置场景 → `must_run_tool_gate`
- 执行完成后 → `autofill_exec_report`
- exec report 完成后 → `generate_validation_bundle`
- 工具已跑但字段未落点 → `tool_result_landing_check`
- 复审前/close 前 → `closeout_candidate_check`

---

## 自动推进规则

满足以下条件时，默认自动进入下一环：

1. 新批次进入时，先自动执行 `create_issue_stub`
2. stub 完成后，自动执行 `infer_owner_candidates`
3. owner 候选形成后，自动执行 `infer_required_tools`
4. `owner_confidence < 70` 或 route 不稳时，必须执行 `route_dry_run`
5. 边界不清但存在安全推进路径时，必须执行 `provisional_boundary_build`
6. owner 确认后，必须先执行 `owner_self_resolve_attempt`
7. 多 owner 交叉依赖时，先执行 `peer_role_consult`，必要时再执行 `split_subissues`
8. 重复失败 / route 碎裂 / owner 不稳时，必须执行 `fallback_to_p8_enhanced`
9. 需要改派、重构 issue、重排工具顺序时，必须执行 `p9_reframe_and_redispatch`
10. 正式派单前，必须通过 `must_run_tool_gate`
11. 执行完成后，必须执行 `autofill_exec_report`
12. exec report 完成后，必须执行 `generate_validation_bundle`
13. review / done 前，必须通过 `tool_result_landing_check`
14. closeout 前，必须通过 `closeout_candidate_check`
15. 任一关口不通过时，自动转入 `tool_missing / evidence_incomplete / reroute_required / reopen_required`

---

## 内部解法穷尽链（强制）

默认不是“直接问用户”，而是先在编排体系内部穷尽解法。

固定顺序：

```text
当前 owner 自救
→ 必要时 peer_role_consult
→ 必要时 split_subissues
→ 必要时 fallback_to_p8_enhanced
→ 调用对应 Tool Skill 压实证据与边界
→ P9 协调、重构工单、重定边界
→ 仅当内部方案穷尽仍无法继续时，才升级问用户
```

---

## 激活确认

```text
[HGS 正式发布版已装配]
入口：00_HGS_Master_Loader.md
模式：Master Loader + Roles + Tools + Automation Actions + Governance Docs + Manifest
加载策略：Manifest 驱动，全角色 + 全工具 + 第一批/第二批自动化动作装配
默认路线：P10(按需) → 真相Owner → P9 → P8 → 体验 / QA / SRE → P9 → P10(按需) → Docs → Closeout
自动化动作：create_issue_stub / infer_owner_candidates / infer_required_tools / route_dry_run / provisional_boundary_build / owner_self_resolve_attempt / peer_role_consult / split_subissues / fallback_to_p8_enhanced / p9_reframe_and_redispatch / must_run_tool_gate / autofill_exec_report / generate_validation_bundle / tool_result_landing_check / closeout_candidate_check
统一协议：HGS-BATCH-HEADER / ISSUE-LEDGER / P8-EXEC-REPORT / HGS-EXPERIENCE-CHECK / P9-REVIEW-VERDICT / P10-FINAL-DECISION / HGS-CLOSEOUT / AUTOMATION-ACTION-RECORD
```
