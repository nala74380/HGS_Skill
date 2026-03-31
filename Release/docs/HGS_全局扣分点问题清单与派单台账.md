# HGS 全局扣分点问题清单与派单台账

> 版本：formal-2026-03-31-ledger1  
> 来源：基于 `Release/docs/HGS_全局检查与清理评分报告.md`、`Release/docs/HGS_自动化联动装配后复核（评分驱动版）.md`、`Release/docs/HGS_全量问题发现—全量派单—持续回流直到清零协议_装配后复核.md` 以及当前 `main` 分支最新全局审查结果。  
> 说明：本台账用于把本轮全局审查发现的**所有扣分点**逐条登记、逐条归属 owner、逐条派单，并纳入清零循环。  
> 原则：**不是挑重点处理，而是全部立账、全部派单、持续回流直到清零。**

---

# 一、总览

## FULL-ISSUE-INVENTORY

```yaml
FULL-ISSUE-INVENTORY:
  batch_id: "hgs-global-audit-deduction-ledger-2026-03-31"
  review_cycle_no: 1
  total_found_issue_count: 16
  open_issue_count: 16
  dispatched_issue_count: 16
  in_progress_issue_count: 0
  verifying_issue_count: 0
  experience_pending_count: 0
  review_pending_count: 16
  docs_sink_pending_count: 0
  done_issue_count: 0
  blocked_issue_count: 0
```

说明：
- 本轮不允许只处理一部分问题
- 所有问题默认已进入 `dispatched` 或待执行状态
- 后续每轮复审后必须更新本表

---

# 二、逐条问题清单与派单结果

| issue_id | 扣分点 | 扣分原因 | primary_owner | execution_role | support_roles | required_tools | required_validation | required_experience | dispatch_wave | status |
|---|---|---|---|---|---|---|---|---|---:|---|
| DED-001 | `MANIFEST.documentation_load_order` 未纳入最新审查文档 | 文档装配名单未完整覆盖 `audit5`、`audit-clear1`、当前台账 | `20_P9_Principal` | `31_P8_Backend_PUA` | `39_Knowledge_Documentation_Owner` | `107_Protocol_Field_Completeness_Checker` | manifest / docs list consistency review | no | 1 | dispatched |
| DED-002 | `MANIFEST.governance_docs` 未纳入最新治理文档 | 治理文档注册不完整，导致装配主链与治理文档名单不同步 | `20_P9_Principal` | `31_P8_Backend_PUA` | `39_Knowledge_Documentation_Owner` | `107_Protocol_Field_Completeness_Checker` | governance docs registration review | no | 1 | dispatched |
| DED-003 | `Master Loader` 激活文档清单未覆盖最新治理文档 | Loader 的“必须同时读取”清单尚未完整覆盖最新复核/台账文档 | `20_P9_Principal` | `31_P8_Backend_PUA` | `39_Knowledge_Documentation_Owner` | `107_Protocol_Field_Completeness_Checker` | loader / manifest / docs consistency review | no | 1 | dispatched |
| DED-004 | `audit-score2` 正文存在时序性陈旧表述 | 文档版本已升，但正文仍保留“r2→r3 / audit4→audit5 待升级”的旧描述 | `39_Knowledge_Documentation_Owner` | `39_Knowledge_Documentation_Owner` | `20_P9_Principal` | `107_Protocol_Field_Completeness_Checker` | doc internal stale-state cleanup review | no | 1 | dispatched |
| DED-005 | 评分引擎仍未独立 Tool Skill 化 | 当前评分动作主要依赖协议 / 编排表达，非独立评分工具 | `37_QA_Validation_Owner` | `31_P8_Backend_PUA` | `20_P9_Principal` | `95_Test_Matrix_Builder`, `107_Protocol_Field_Completeness_Checker` | tool spec review + integration review | no | 2 | dispatched |
| DED-006 | 清零循环仍未独立 Tool Skill 化 | `register_all_findings / continue_loop_until_open_issue_zero` 仍主要由协议 / Loader 约束 | `20_P9_Principal` | `31_P8_Backend_PUA` | `39_Knowledge_Documentation_Owner`, `37_QA_Validation_Owner` | `107_Protocol_Field_Completeness_Checker`, `108_Chain_Route_Simulator` | loop governance review + integration review | no | 2 | dispatched |
| DED-007 | `generate_exec_plan` 已定义但未进入 active chain | 执行前计划生成仍未被提升为自动编排硬动作 | `20_P9_Principal` | `31_P8_Backend_PUA` | `37_QA_Validation_Owner` | `108_Chain_Route_Simulator`, `107_Protocol_Field_Completeness_Checker` | manifest / loader / protocol sync review | no | 3 | dispatched |
| DED-008 | `auto_reroute_on_new_truth` 已定义但未进入 active chain | 新真相改派能力仍未正式 active | `20_P9_Principal` | `31_P8_Backend_PUA` | `11_Product_Business_Rules_Owner`, `12_Auth_Identity_Owner` | `108_Chain_Route_Simulator` | reroute route-stability review | no | 3 | dispatched |
| DED-009 | `high_risk_guard_gate` 已定义但未进入 active chain | 高风险动作门禁仍未被提升为自动编排硬动作 | `15_Security_Risk_Owner` | `31_P8_Backend_PUA` | `20_P9_Principal` | `109_High_Risk_Action_Guard_Checker` | security gate integration review | no | 3 | dispatched |
| DED-010 | `auth_bypass_guard_gate` 已定义但未进入 active chain | 越权 / 绕过门禁仍未被提升为自动编排硬动作 | `12_Auth_Identity_Owner` | `31_P8_Backend_PUA` | `15_Security_Risk_Owner`, `20_P9_Principal` | `110_Authorization_Bypass_Path_Reviewer` | auth gate integration review | no | 3 | dispatched |
| DED-011 | `runtime_stability_gate` 已定义但未进入 active chain | 运行面门禁仍未被提升为自动编排硬动作 | `19_Execution_Plane_Owner` | `31_P8_Backend_PUA` | `38_SRE_Observability_Owner`, `20_P9_Principal` | `91_Worker_Identity_Stability`, `92_Heartbeat_Gap_Analyzer`, `98_Trace_Correlation` | runtime gate integration review | no | 3 | dispatched |
| DED-012 | 缺 `111_Bulk_Action_Safety_Reviewer_SKILL.md` | 批量高风险动作仍缺专属工具 | `15_Security_Risk_Owner` | `31_P8_Backend_PUA` | `20_P9_Principal` | `109_High_Risk_Action_Guard_Checker` | tool build review + integration review | no | 4 | dispatched |
| DED-013 | 缺 `112_Audit_Log_Consistency_Checker_SKILL.md` | 审计一致性仍缺专属工具 | `38_SRE_Observability_Owner` | `31_P8_Backend_PUA` | `39_Knowledge_Documentation_Owner`, `20_P9_Principal` | `107_Protocol_Field_Completeness_Checker` | audit consistency review | no | 4 | dispatched |
| DED-014 | 缺 `113_Runtime_Incident_Replayer_SKILL.md` | 运行事故重建仍缺专属工具 | `38_SRE_Observability_Owner` | `31_P8_Backend_PUA` | `19_Execution_Plane_Owner` | `98_Trace_Correlation`, `92_Heartbeat_Gap_Analyzer` | runtime replay review | no | 4 | dispatched |
| DED-015 | 清零循环尚未拆成独立 active 动作集 | 目前只有协议 / Loader 约束，未成为正式 active action family | `20_P9_Principal` | `31_P8_Backend_PUA` | `39_Knowledge_Documentation_Owner` | `108_Chain_Route_Simulator`, `107_Protocol_Field_Completeness_Checker` | active action decomposition review | no | 2 | dispatched |
| DED-016 | 文档时序残留缺少自动巡检机制 | 当前仍需人工发现“正文版本已旧”的问题 | `39_Knowledge_Documentation_Owner` | `31_P8_Backend_PUA` | `20_P9_Principal` | `107_Protocol_Field_Completeness_Checker` | doc stale-state detection review | no | 1 | dispatched |

---

# 三、执行波次（不是可选方案，全部都要做）

## Wave 1：治理文档与装配名单同频
- DED-001
- DED-002
- DED-003
- DED-004
- DED-016

## Wave 2：评分 / 清零循环工具化与动作化
- DED-005
- DED-006
- DED-015

## Wave 3：已定义未 active 的关键动作接入
- DED-007
- DED-008
- DED-009
- DED-010
- DED-011

## Wave 4：缺失工具补齐
- DED-012
- DED-013
- DED-014

说明：
- 这不是方案 A / B / C
- 这只是为了并行执行而做的执行波次划分
- **所有波次都必须做，不允许跳过**

---

# 四、CLEARANCE-CYCLE-REPORT

```yaml
CLEARANCE-CYCLE-REPORT:
  batch_id: "hgs-global-audit-deduction-ledger-2026-03-31"
  review_cycle_no: 1
  newly_found_issue_count: 16
  newly_dispatched_issue_count: 16
  newly_closed_issue_count: 0
  reopened_issue_count: 0
  remaining_open_issue_count: 16
  major_blockers:
    - "评分引擎尚未独立 Tool Skill 化"
    - "清零循环尚未独立 Tool Skill 化"
    - "5 个已定义关键动作尚未进入 active chain"
    - "111/112/113 三个工具尚未补齐"
    - "治理文档装配名单与正文仍有残留不同步"
  next_required_action: "continue_execution"
```

---

# 五、CLEARANCE-GATE

```yaml
CLEARANCE-GATE:
  batch_id: "hgs-global-audit-deduction-ledger-2026-03-31"
  open_issue_count: 16
  review_pending_count: 16
  verification_pending_count: 16
  experience_pending_count: 0
  docs_sink_pending_count: 0
  can_closeout: "no"
  closeout_blockers:
    - "16 个扣分点问题已立账但尚未清零"
    - "active chain 仍有关键动作未接入"
    - "评分 / 清零循环仍未完成工具化"
    - "缺失的 111/112/113 工具仍未补齐"
```

---

# 六、结论

本台账的作用只有一个：

**把本轮全局审查发现的所有扣分点全部立账、全部派单、全部纳入清零循环，不再让任何问题继续以“以后再说”的方式悬空。**
