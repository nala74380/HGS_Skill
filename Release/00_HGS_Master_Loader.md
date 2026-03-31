---
name: hgs-master-loader
description: HGS 正式发布版主装配器。负责装配 Manifest、角色 Skill、工具 Skill、治理文档、自动编排协议与其他协议 Skill，并按统一状态机驱动全链路。
version: formal-2026-03-31-int4
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
- 自动化动作驱动 owner 置信与 route dry-run
- 自动化动作驱动工具闸门与字段落点检查
- 自动化动作驱动 closeout 候选检查

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

## 角色装配清单

### 战略层
- `roles/10_P10_CTO_SKILL.md`

### 真相 / Owner 层
- `roles/11_Product_Business_Rules_Owner_SKILL.md`
- `roles/12_Auth_Identity_Owner_SKILL.md`
- `roles/13_Billing_Entitlement_Owner_SKILL.md`
- `roles/14_Release_Config_Owner_SKILL.md`
- `roles/15_Security_Risk_Owner_SKILL.md`
- `roles/16_Agent_Operations_Owner_SKILL.md`
- `roles/17_EndUser_Support_Owner_SKILL.md`
- `roles/18_Control_Plane_Owner_SKILL.md`
- `roles/19_Execution_Plane_Owner_SKILL.md`

### 审查 / 派单 / 复审层
- `roles/20_P9_Principal_SKILL.md`

### 执行层
- `roles/30_P8_PUA_Enhanced_SKILL.md`
- `roles/31_P8_Backend_PUA_SKILL.md`
- `roles/32A_P8_UI_Surface_Engineer_SKILL.md`
- `roles/32B_P8_Frontend_Logic_Engineer_SKILL.md`
- `roles/33A_P8_Console_Runtime_Engineer_SKILL.md`
- `roles/33B_P8_Console_Management_Experience_Engineer_SKILL.md`
- `roles/34_P8_LanrenJingling_PUA_SKILL.md`
- `roles/35_P8_Agent_PUA_SKILL.md`
- `roles/36_P8_EndUser_PUA_SKILL.md`

### 验证 / 运行 / 沉淀层
- `roles/37_QA_Validation_Owner_SKILL.md`
- `roles/38_SRE_Observability_Owner_SKILL.md`
- `roles/39_Knowledge_Documentation_Owner_SKILL.md`

---

## 工具装配清单

### 真相判定工具
- `tools/70_Business_Rule_Matrix_SKILL.md`
- `tools/72_JWT_Inspector_SKILL.md`
- `tools/73_Device_Identity_Diff_SKILL.md`
- `tools/74_Session_Refresh_Trace_SKILL.md`
- `tools/77_Quota_Usage_Analyzer_SKILL.md`
- `tools/78_Freeze_Reversal_Diagnoser_SKILL.md`
- `tools/88_Console_Auth_Flow_Trace_SKILL.md`
- `tools/89_Project_Context_Drift_SKILL.md`
- `tools/90_StepUp_Resume_Checker_SKILL.md`
- `tools/101_Compatibility_Matrix_SKILL.md`

### 差异 / 漂移工具
- `tools/71_State_Machine_Consistency_SKILL.md`
- `tools/79_API_Contract_Diff_SKILL.md`
- `tools/82_Network_Trace_Reviewer_SKILL.md`

### 运行面工具
- `tools/91_Worker_Identity_Stability_SKILL.md`
- `tools/92_Heartbeat_Gap_Analyzer_SKILL.md`
- `tools/98_Trace_Correlation_SKILL.md`

### 体验 / 表面审查工具
- `tools/85_UI_Surface_Audit_SKILL.md`

### 验证工具
- `tools/95_Test_Matrix_Builder_SKILL.md`
- `tools/96_Regression_Checklist_SKILL.md`
- `tools/107_Protocol_Field_Completeness_Checker_SKILL.md`
- `tools/108_Chain_Route_Simulator_SKILL.md`

### 安全 / 门禁工具
- `tools/109_High_Risk_Action_Guard_Checker_SKILL.md`
- `tools/110_Authorization_Bypass_Path_Reviewer_SKILL.md`

### 沉淀工具
- `tools/106_SOP_Generator_SKILL.md`

---

## 协议与治理文档装配清单

### 自动编排协议层
- `protocols/61_Automation_Orchestration_Protocol.md`

### 体验 / 再审协议层
- `protocols/40_P8_Agent_Experience_Protocol.md`
- `protocols/41_P8_EndUser_Experience_Protocol.md`
- `protocols/50_RE_REVIEW_PROTOCOL.md`
- `protocols/60_HGS_IO_Protocol.md`

### 治理文档
- `docs/正式发布版全局审查报告.md`
- `docs/发布说明与加载方式.md`
- `docs/角色调用关系总表.md`
- `docs/工具调用关系总表.md`
- `docs/HGS_自动化联动动作总表（正式版）.md`

---

## 主状态机

所有 issue 必须遵守：

```text
todo
→ intake_normalized
→ tool_gating
→ owner_confirmed
→ dispatched
→ in_progress
→ evidence_assembled
→ verifying
→ experience_check
→ reviewing
→ docs_sink
→ done
```

允许的异常分支：

```text
blocked
rework
escalate_to_p10
reopen
awaiting_external
owner_unclear
tool_missing
evidence_incomplete
reroute_required
reopen_required
```

---

## 自动化动作装配清单（第一批 active）

当前正式激活的第一批动作为：

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

这些动作的详细输入输出以：
- `docs/HGS_自动化联动动作总表（正式版）.md`
- `protocols/61_Automation_Orchestration_Protocol.md`

为准。

---

## 自动化动作执行顺序（第一批）

### 入口标准化序列
```text
create_issue_stub
→ infer_owner_candidates
→ infer_required_tools
→ route_dry_run（当 owner_confidence 低 / mixed issue / route 不稳）
→ provisional_boundary_build（当边界暂不精确）
```

### 内部协商序列
```text
peer_role_consult（当当前 owner 自救不足）
→ split_subissues（当 mixed issue / 多 owner 交叉依赖）
```

### 工具闸门序列
```text
must_run_tool_gate
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
- 工具结果未落字段不得进入 review / done
- 未通过 `closeout_candidate_check` 不得进入 `done`

---

## 路由矩阵

### 按真相归属路由
- 业务规则、状态语义、自助边界、平台/代理/用户权责 → `roles/11_Product_Business_Rules_Owner_SKILL.md`
- token、session、设备身份、project scope、recent-auth、step-up 真相 → `roles/12_Auth_Identity_Owner_SKILL.md`
- 点数、冻结、冲正、配额、授权权益 → `roles/13_Billing_Entitlement_Owner_SKILL.md`
- 版本组合、配置边界、灰度、回滚 → `roles/14_Release_Config_Owner_SKILL.md`
- 越权、暴露、高风险动作门禁、安全债 → `roles/15_Security_Risk_Owner_SKILL.md`
- 代理 owner 层动作、升级边界、经营闭环标准 → `roles/16_Agent_Operations_Owner_SKILL.md`
- 用户自助边界、支持路径、升级条件、闭环标准 → `roles/17_EndUser_Support_Owner_SKILL.md`
- 后台真相、管理归属、控制平面 / 执行平面分层 → `roles/18_Control_Plane_Owner_SKILL.md`
- 运行时门禁、心跳、任务状态、热更新执行链 → `roles/19_Execution_Plane_Owner_SKILL.md`

### 按动作驱动路由
- owner 低置信 / mixed issue / route 不稳 → `route_dry_run`
- 边界不清但可非破坏性推进 → `provisional_boundary_build`
- 多 owner 交叉依赖 → `peer_role_consult` → `split_subissues`
- 命中工具前置场景 → `must_run_tool_gate`
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
6. 多 owner 交叉依赖时，先执行 `peer_role_consult`，必要时再执行 `split_subissues`
7. 正式派单前，必须通过 `must_run_tool_gate`
8. review / done 前，必须通过 `tool_result_landing_check`
9. closeout 前，必须通过 `closeout_candidate_check`
10. 任一关口不通过时，自动转入 `tool_missing / evidence_incomplete / reroute_required / reopen_required`

---

## 内部解法穷尽链（强制）

默认不是“直接问用户”，而是先在编排体系内部穷尽解法。

固定顺序：

```text
当前 owner 自救
→ 必要时 peer_role_consult
→ 必要时 split_subissues
→ 调用对应 Tool Skill 压实证据与边界
→ P9 协调、重构工单、重定边界
→ P10 做路线重裁 / 优先级重排
→ 仅当内部方案穷尽仍无法继续时，才升级问用户
```

---

## 停机条件

只有命中以下硬条件，且内部解法穷尽后，才允许升级问用户：
- 需要真实外发给用户 / 代理 / 客户执行
- 涉及不可逆删除、覆盖、批量清理、生产数据破坏性操作
- 需要用户做业务取舍，且 P9 / P10 已确认内部不存在可接受默认路径
- 涉及法律 / 安全 / 金融边界，已超出当前批次授权范围
- 暴露路线级 / 战略级冲突，且 P10 重裁后仍需你拍板

---

## 激活确认

```text
[HGS 正式发布版已装配]
入口：00_HGS_Master_Loader.md
模式：Master Loader + Roles + Tools + Automation Actions + Governance Docs + Manifest
加载策略：Manifest 驱动，全角色 + 全工具 + 第一批自动化动作装配
默认路线：P10(按需) → 真相Owner → P9 → P8 → 体验 / QA / SRE → P9 → P10(按需) → Docs → Closeout
自动化动作：create_issue_stub / infer_owner_candidates / infer_required_tools / route_dry_run / provisional_boundary_build / peer_role_consult / split_subissues / must_run_tool_gate / tool_result_landing_check / closeout_candidate_check
统一协议：HGS-BATCH-HEADER / ISSUE-LEDGER / P8-EXEC-REPORT / HGS-EXPERIENCE-CHECK / P9-REVIEW-VERDICT / P10-FINAL-DECISION / HGS-CLOSEOUT / AUTOMATION-ACTION-RECORD
```
