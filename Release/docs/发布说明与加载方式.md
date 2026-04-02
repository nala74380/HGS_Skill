# HGS 自动化联动动作总表（正式版）

> 版本：formal-2026-03-31-r4  
> 定位：HGS 正式发布版的自动化联动治理文档。用于把“内部闭环优先、工具前置、角色协同、收口再审、评分驱动决策、持续回流直到清零”从原则层升级为**动作层 + 闸门层 + 评分层 + 清零治理层**。  
> 说明：本文件定义的是**当前 active 自动化动作、分数阈值、决策规则、清零规则与编排边界**。

---

# 一、当前正式状态

当前 HGS 自动化联动已正式形成：

- 第一批动作：已接入 active chain
- 第二批动作：已接入 active chain
- 第三批动作：已接入 active chain
- 第四批评分动作：已接入 active chain
- Wave 3 接入动作：已接入 active chain
- 清零循环动作：已接入 active chain
- 清零治理协议：已接入 active chain

当前 active 动作总数：**36 个**。  
当前关键治理协议：
- `61_Automation_Orchestration_Protocol.md`
- `62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md`

---

# 二、总原则

## 1. 内部闭环优先
```text
当前 owner 自救
→ 平级协商 / 拆子问题
→ 工具压实证据
→ P9 重构与再派单
→ 体验复演 / 回流
→ Docs 沉淀
→ 仅在内部方案穷尽后才升级问用户
```

## 2. 工具前置于拍板与执行
```text
先跑工具
→ 再落协议字段
→ 再进入执行 / 复审 / closeout
```

## 3. 分数前置于关键决策
- 派单前看 `owner_confidence` 与 `route_stability_score`
- review 前看 `tool_coverage_score` 与 `evidence_completeness_score`
- reopen 前看 `reopen_risk_score`
- done 前看 `closeout_readiness_score` 与 `reopen_risk_score`

## 4. 清零优先于提前收口
```text
全部登记
→ 全部归属 owner
→ 全部派单
→ 全部进入测试 / 体验 / 复审
→ 再发现再继续回流
→ 直到 open_issue_count = 0
→ 才允许收口
```

---

# 三、当前 active 动作分层

## 1. 入口标准化层
- `create_issue_stub`
- `infer_owner_candidates`
- `infer_required_tools`
- `compute_owner_confidence`
- `compute_route_stability_score`
- `route_dry_run`
- `provisional_boundary_build`

## 2. 内部协商与重派单层
- `owner_self_resolve_attempt`
- `peer_role_consult`
- `split_subissues`
- `fallback_to_p8_enhanced`
- `p9_reframe_and_redispatch`
- `auto_reroute_on_new_truth`

## 3. 风险 / 安全 / 运行门禁层
- `high_risk_guard_gate`
- `auth_bypass_guard_gate`
- `runtime_stability_gate`
- `must_run_tool_gate`

## 4. 执行层
- `generate_exec_plan`
- `execute_by_owner`
- `autofill_exec_report`

## 5. 验证与体验层
- `generate_validation_bundle`
- `validate_and_experience_by_issue`
- `experience_replay`
- `compute_tool_coverage_score`
- `compute_evidence_completeness_score`
- `tool_result_landing_check`

## 6. 回流与收口层
- `compute_reopen_risk_score`
- `auto_reopen_on_drift`
- `auto_docs_sink`
- `compute_closeout_readiness_score`
- `closeout_candidate_check`

## 7. 清零循环层
- `register_all_findings`
- `dispatch_all_registered_issues`
- `rereview_all_open_issues`
- `register_new_findings_if_any`
- `continue_loop_until_open_issue_zero`

---

# 四、当前 active 动作清单（按执行顺序）

```text
create_issue_stub
→ infer_owner_candidates
→ compute_owner_confidence
→ infer_required_tools
→ compute_route_stability_score
→ route_dry_run
→ provisional_boundary_build
→ owner_self_resolve_attempt
→ peer_role_consult
→ split_subissues
→ fallback_to_p8_enhanced
→ p9_reframe_and_redispatch
→ auto_reroute_on_new_truth
→ high_risk_guard_gate
→ auth_bypass_guard_gate
→ runtime_stability_gate
→ must_run_tool_gate
→ register_all_findings
→ dispatch_all_registered_issues
→ generate_exec_plan
→ execute_by_owner
→ autofill_exec_report
→ generate_validation_bundle
→ validate_and_experience_by_issue
→ experience_replay
→ compute_tool_coverage_score
→ compute_evidence_completeness_score
→ tool_result_landing_check
→ rereview_all_open_issues
→ compute_reopen_risk_score
→ auto_reopen_on_drift
→ register_new_findings_if_any
→ continue_loop_until_open_issue_zero
→ auto_docs_sink
→ compute_closeout_readiness_score
→ closeout_candidate_check
```

---

# 五、分数阈值（当前正式值）

## dispatch 阈值
- `owner_confidence_min_for_direct_dispatch = 70`
- `route_stability_min_for_direct_dispatch = 65`

## review 阈值
- `tool_coverage_min_before_review = 85`
- `evidence_completeness_min_before_review = 80`

## done / reopen 阈值
- `closeout_readiness_min_before_done = 85`
- `reopen_risk_high = 60`

---

# 六、评分驱动决策规则（当前正式规则）

## dispatch
只有同时满足：
- `owner_confidence >= 70`
- `route_stability_score >= 65`

才允许直接 dispatch。否则先 `route_dry_run`，必要时 `p9_reframe_and_redispatch`。

## review
只有同时满足：
- `tool_coverage_score >= 85`
- `evidence_completeness_score >= 80`
- `P8-EXEC-REPORT` 已存在
- `validation bundle` 已存在

才允许进入 review。

## reopen
只要满足任一：
- `reopen_risk_score >= 60`
- QA / review / experience / tools 发现 drift

则自动执行：
- `auto_reopen_on_drift`
- 必要时 `auto_reroute_on_new_truth` 或 `p9_reframe_and_redispatch`

## done
只有同时满足：
- `closeout_readiness_score >= 85`
- `reopen_risk_score < 60`
- `closeout_candidate_check = pass`
- `auto_docs_sink` 已完成
- `open_issue_count = 0`

才允许进入 `done`。

---

# 七、清零治理规则（当前正式规则）

1. 所有发现必须登记  
2. 所有已登记问题必须派单  
3. 谁的问题谁处理  
4. 处理后必须测试 / 体验 / 复审  
5. 再发现问题必须继续回流  
6. `open_issue_count = 0` 才允许收口  

关键结构：
- `FULL-ISSUE-INVENTORY`
- `CLEARANCE-CYCLE-REPORT`
- `CLEARANCE-GATE`

---

# 八、正式硬闸门

当前正式生效的关键硬闸门包括：

1. 未创建 `ISSUE-LEDGER stub` 不得派单  
2. 未通过分数闸门不得派单  
3. 未通过工具闸门不得派单  
4. 高风险动作必须过 `high_risk_guard_gate`  
5. 越权/绕过风险必须过 `auth_bypass_guard_gate`  
6. 运行面身份/心跳/trace 风险必须过 `runtime_stability_gate`  
7. 无 `exec_plan` 不得执行  
8. 无 `P8-EXEC-REPORT` 不得 review  
9. 无 `validation bundle` 不得 review  
10. 无真实体验反馈时必须先 `experience_replay`  
11. 无协议落点不得 review / done  
12. `reopen_risk >= 60` 时不得 close  
13. 未完成 `auto_docs_sink` 不得 done  
14. 未通过 `closeout_candidate_check` 不得 done  
15. review 前必须完成所有发现问题登记  
16. done 前必须存在 `FULL-ISSUE-INVENTORY`  
17. `open_issue_count > 0` 时不得 done  

---

# 九、关键新增工具（本轮接入）

- `111_Bulk_Action_Safety_Reviewer_SKILL.md`
- `112_Audit_Log_Consistency_Checker_SKILL.md`
- `113_Runtime_Incident_Replayer_SKILL.md`
- `114_Score_Decision_Engine_SKILL.md`
- `115_Full_Issue_Clearance_Controller_SKILL.md`
- `116_Document_State_Consistency_Sentinel_SKILL.md`

---

# 十、结论

本总表当前阶段的使命只有一个：

**明确告诉整个 HGS：哪些动作已经正式生效、哪些分数会影响派单/复审/重开/收口、以及“未清零不得收口”已经是正式硬规则。**
