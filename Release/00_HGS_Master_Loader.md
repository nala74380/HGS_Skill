---
name: hgs-master-loader
description: HGS 正式发布版主装配器。负责装配 Manifest、角色 Skill、工具 Skill、治理文档、自动编排协议、清零协议与其他协议 Skill，并按统一状态机驱动全链路。
version: formal-2026-03-31-int10
author: OpenAI
role: MasterLoader
status: active
entrypoint: true
---

# HGS Master Loader / 主装配器

本文件的职责只有一件事：**把多角色、多工具、自动化动作、统一协议、清零治理规则正式装配成一条可自动推进、可审计、可持续回流直到清零的标准链路。**

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
9. `docs/HGS_自动化联动装配后复核（评分驱动版）.md`
10. `docs/HGS_全量问题发现—全量派单—持续回流直到清零协议_装配后复核.md`
11. `docs/HGS_全局检查与清理评分报告.md`
12. `docs/HGS_全局扣分点问题清单与派单台账.md`
13. `protocols/62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md`

---

## 装配目标

默认路线固定为：

```text
全局审查
→ 全量发现问题
→ 全量登记 issue
→ 全量派单
→ 按 owner 执行
→ 测试 / 回归 / 体验
→ 全量复审
→ 新问题继续登记并继续派单
→ 持续回流直到 open_issue_count = 0
→ Docs 沉淀
→ Closeout
```

本版新增并已正式接入的核心能力：

- **评分驱动 dispatch / review / reopen / done**
- **清零循环的协议化与工具化**
- **高风险 / 越权 / 运行面门禁动作已进入 active chain**
- **本轮扣分点全部进入派单台账并纳入清零循环**

---

## 工具装配清单（新增重点）

### 新增安全 / 治理 / 运行工具
- `tools/111_Bulk_Action_Safety_Reviewer_SKILL.md`
- `tools/112_Audit_Log_Consistency_Checker_SKILL.md`
- `tools/113_Runtime_Incident_Replayer_SKILL.md`
- `tools/114_Score_Decision_Engine_SKILL.md`
- `tools/115_Full_Issue_Clearance_Controller_SKILL.md`
- `tools/116_Document_State_Consistency_Sentinel_SKILL.md`

---

## 自动化动作装配清单（当前 active）

当前正式激活的动作包括：

### 核心编排
- `create_issue_stub`
- `infer_owner_candidates`
- `infer_required_tools`
- `compute_owner_confidence`
- `compute_route_stability_score`
- `route_dry_run`
- `provisional_boundary_build`
- `owner_self_resolve_attempt`
- `peer_role_consult`
- `split_subissues`
- `fallback_to_p8_enhanced`
- `p9_reframe_and_redispatch`

### 新接入 active 的执行 / 改派 / 门禁动作
- `generate_exec_plan`
- `auto_reroute_on_new_truth`
- `high_risk_guard_gate`
- `auth_bypass_guard_gate`
- `runtime_stability_gate`

### 清零循环动作
- `register_all_findings`
- `dispatch_all_registered_issues`
- `execute_by_owner`
- `validate_and_experience_by_issue`
- `rereview_all_open_issues`
- `register_new_findings_if_any`
- `continue_loop_until_open_issue_zero`

### 既有验证 / 收口动作
- `must_run_tool_gate`
- `autofill_exec_report`
- `generate_validation_bundle`
- `experience_replay`
- `compute_tool_coverage_score`
- `compute_evidence_completeness_score`
- `tool_result_landing_check`
- `compute_reopen_risk_score`
- `auto_reopen_on_drift`
- `auto_docs_sink`
- `compute_closeout_readiness_score`
- `closeout_candidate_check`

---

## 自动化动作执行顺序（当前 active）

### 入口与路由
```text
create_issue_stub
→ infer_owner_candidates
→ compute_owner_confidence
→ infer_required_tools
→ compute_route_stability_score
→ route_dry_run
→ provisional_boundary_build
```

### 自救、协商与重派
```text
owner_self_resolve_attempt
→ peer_role_consult
→ split_subissues
→ fallback_to_p8_enhanced
→ p9_reframe_and_redispatch
→ auto_reroute_on_new_truth
```

### 门禁与执行
```text
high_risk_guard_gate
→ auth_bypass_guard_gate
→ runtime_stability_gate
→ must_run_tool_gate
→ generate_exec_plan
→ execute_by_owner
→ autofill_exec_report
```

### 验证与体验
```text
generate_validation_bundle
→ validate_and_experience_by_issue
→ experience_replay
→ compute_tool_coverage_score
→ compute_evidence_completeness_score
→ tool_result_landing_check
```

### 回流与清零
```text
compute_reopen_risk_score
→ auto_reopen_on_drift
→ register_new_findings_if_any
→ continue_loop_until_open_issue_zero
→ auto_docs_sink
→ compute_closeout_readiness_score
→ closeout_candidate_check
```

---

## 清零循环（强制）

固定循环如下：

```text
register_all_findings
→ dispatch_all_registered_issues
→ execute_by_owner
→ validate_and_experience_by_issue
→ rereview_all_open_issues
→ register_new_findings_if_any
→ continue_loop_until_open_issue_zero
```

硬要求：
- 禁止“这轮先只修重点，剩下下次再说”作为默认策略
- 禁止“问题太多”为理由不立账、不派单
- 禁止在 open issue 未清零时让用户承担编排决策压力
- 允许多轮循环，但不允许未清零就 closeout

---

## 分数驱动与 done 条件

### dispatch
只有：
- `owner_confidence >= 70`
- `route_stability_score >= 65`

才允许直接派单。

### review
只有：
- `tool_coverage_score >= 85`
- `evidence_completeness_score >= 80`

才允许进入 review。

### done
只有：
- `closeout_readiness_score >= 85`
- `reopen_risk_score < 60`
- `closeout_candidate_check = pass`
- `auto_docs_sink` 已完成
- `open_issue_count = 0`

才允许进入 `done`。

---

## 当前执行底册

当前轮次必须参考：
- `docs/HGS_全局扣分点问题清单与派单台账.md`

作为 open issue 的基线，并按 wave 顺序推进，但**所有 wave 都必须执行，不允许跳过**。

---

## 激活确认

```text
[HGS 正式发布版已装配]
入口：00_HGS_Master_Loader.md
模式：Master Loader + Roles + Tools + Automation Actions + Score-Driven Decisions + Full-Issue-Clearance Protocol
当前执行底册：HGS_全局扣分点问题清单与派单台账.md
强制条件：所有发现必须登记、所有问题必须派单、所有问题处理后必须测试/体验/复审、open_issue_count = 0 才允许收口
```
