---
name: automation-orchestration-protocol
description: HGS 自动编排协议。定义自动化联动动作的统一记录结构、状态字段、评分字段与最小输入输出骨架，供 Loader 与自动化动作共同使用。
version: formal-2026-03-31-p5
author: OpenAI
role: Protocol
status: active
---

# HGS Automation Orchestration Protocol

## 1. 协议目标

本协议用于统一描述 HGS 自动化联动动作的：
- 触发原因
- 输入
- 输出
- 下一跳
- 闸门结果
- 状态迁移
- 评分字段

本协议只负责：

**把自动化动作从“文字描述”变成可记录、可审计、可回放的结构，并让分数可驱动编排决策。**

---

## 2. 自动化动作记录骨架

```yaml
AUTOMATION-ACTION-RECORD:
  batch_id: "<批次ID>"
  issue_id: "<问题ID>"
  action_name: "<动作名>"
  stage: "intake | deliberation | gating | execution | validation | review | closeout"
  trigger_reason:
    - "<触发原因>"
  inputs:
    - key: "<输入字段名>"
      value: "<输入值摘要>"
  outputs:
    - key: "<输出字段名>"
      value: "<输出值摘要>"
  gate_result: "pass | fail | conditional | not_applicable"
  next_hop: "<下一跳动作/角色/协议>"
  notes:
    - "<补充说明>"
```

---

## 3. 动作状态字段

```yaml
AUTOMATION-STATE:
  current_state: "todo | intake_normalized | tool_gating | owner_confirmed | dispatched | in_progress | evidence_assembled | verifying | experience_check | reviewing | docs_sink | done | blocked | rework | escalate_to_p10 | reopen | awaiting_external | owner_unclear | tool_missing | evidence_incomplete | reroute_required | reopen_required"
  previous_state: "<上一个状态>"
  state_reason: "<状态迁移原因>"
```

---

## 4. 评分字段骨架

```yaml
AUTOMATION-SCORES:
  owner_confidence: 0
  tool_coverage_score: 0
  evidence_completeness_score: 0
  route_stability_score: 0
  closeout_readiness_score: 0
  reopen_risk_score: 0
```

---

## 5. 当前 active 动作的最小输入输出

### 5.1 `create_issue_stub`
```yaml
CREATE-ISSUE-STUB:
  inputs: [batch_id, input_scope, source_of_truth, raw_problem_statement]
  outputs: [issue_id, issue_stub, initial_risk_flags, source_of_truth_scope]
```

### 5.2 `infer_owner_candidates`
```yaml
INFER-OWNER-CANDIDATES:
  inputs: [issue_stub, problem_type, risk_flags]
  outputs: [primary_owner_candidate, secondary_owner_candidates, owner_confidence_seed, owner_reasoning]
```

### 5.3 `infer_required_tools`
```yaml
INFER-REQUIRED-TOOLS:
  inputs: [primary_owner_candidate, problem_type, risk_flags]
  outputs: [must_run_tools, optional_tools, tool_reasoning]
```

### 5.4 `compute_owner_confidence`
```yaml
COMPUTE-OWNER-CONFIDENCE:
  inputs: [owner_candidates, issue_stub, tool_reasoning]
  outputs: [owner_confidence, owner_confidence_reason]
```

### 5.5 `compute_route_stability_score`
```yaml
COMPUTE-ROUTE-STABILITY-SCORE:
  inputs: [owner_candidates, must_run_tools, route_fragility_signals]
  outputs: [route_stability_score, route_stability_reason]
```

### 5.6 `route_dry_run`
```yaml
ROUTE-DRY-RUN:
  inputs: [issue_stub, owner_candidates, must_run_tools]
  outputs: [simulated_route, missing_steps, route_conflicts, must_trigger_tools]
```

### 5.7 `provisional_boundary_build`
```yaml
PROVISIONAL-BOUNDARY-BUILD:
  inputs: [issue_stub, route_dry_run_output, risk_flags]
  outputs: [provisional_boundary, allowed_actions, forbidden_actions, assumption_log]
```

### 5.8 `owner_self_resolve_attempt`
```yaml
OWNER-SELF-RESOLVE-ATTEMPT:
  inputs: [primary_owner, must_run_tool_outputs, provisional_or_final_boundary]
  outputs: [attempted_actions, blocked_points, remaining_uncertainties, self_resolve_result]
```

### 5.9 `peer_role_consult`
```yaml
PEER-ROLE-CONSULT:
  inputs: [primary_owner, secondary_owner_candidates, blocked_points, tool_outputs]
  outputs: [consulted_roles, shared_findings, alignment_result, new_owner_boundary_if_any]
```

### 5.10 `split_subissues`
```yaml
SPLIT-SUBISSUES:
  inputs: [issue_ledger, consulted_roles, tool_outputs]
  outputs: [subissue_list, subissue_owner_map, subissue_tool_map, merge_back_rule]
```

### 5.11 `fallback_to_p8_enhanced`
```yaml
FALLBACK-TO-P8-ENHANCED:
  inputs: [issue_ledger, failure_history, tool_outputs]
  outputs: [fallback_reason, enhanced_takeover_scope]
```

### 5.12 `p9_reframe_and_redispatch`
```yaml
P9-REFRAME-AND-REDISPATCH:
  inputs: [issue_ledger, subissue_list, tool_outputs, fallback_reason]
  outputs: [redispatch_plan, new_owner, new_tool_order, acceptance_boundary]
```

### 5.13 `generate_exec_plan`
```yaml
GENERATE-EXEC-PLAN:
  inputs: [owner, tool_outputs, boundary, acceptance_boundary]
  outputs: [exec_plan, risk_notes, required_evidence, regression_scope]
```

### 5.14 `auto_reroute_on_new_truth`
```yaml
AUTO-REROUTE-ON-NEW-TRUTH:
  inputs: [new_truth_signal, current_owner, tool_outputs]
  outputs: [new_owner, reroute_reason, next_dispatch_path]
```

### 5.15 `high_risk_guard_gate`
```yaml
HIGH-RISK-GUARD-GATE:
  inputs: [action_name, action_scope, current_guards]
  outputs: [guard_result, missing_guards, required_actions]
```

### 5.16 `auth_bypass_guard_gate`
```yaml
AUTH-BYPASS-GUARD-GATE:
  inputs: [protected_resource, actor_profile, suspected_bypass_vectors]
  outputs: [bypass_review_result, missing_checks, risky_vectors]
```

### 5.17 `runtime_stability_gate`
```yaml
RUNTIME-STABILITY-GATE:
  inputs: [runtime_issue_profile, runtime_identifiers, runtime_events]
  outputs: [runtime_gate_result, required_runtime_tools, runtime_findings]
```

### 5.18 `register_all_findings`
```yaml
REGISTER-ALL-FINDINGS:
  inputs: [new_findings, issue_inventory, source_cycle]
  outputs: [registered_issue_ids, updated_issue_inventory]
```

### 5.19 `dispatch_all_registered_issues`
```yaml
DISPATCH-ALL-REGISTERED-ISSUES:
  inputs: [issue_inventory, owner_assignment_map, score_snapshot]
  outputs: [dispatch_result_map, undispatchable_items, dispatch_wave_plan]
```

### 5.20 `execute_by_owner`
```yaml
EXECUTE-BY-OWNER:
  inputs: [dispatch_result_map, exec_plans]
  outputs: [execution_result_map, execution_blockers]
```

### 5.21 `validate_and_experience_by_issue`
```yaml
VALIDATE-AND-EXPERIENCE-BY-ISSUE:
  inputs: [execution_result_map, validation_bundle_map, experience_requirements]
  outputs: [validation_result_map, experience_result_map]
```

### 5.22 `rereview_all_open_issues`
```yaml
REREVIEW-ALL-OPEN-ISSUES:
  inputs: [issue_inventory, validation_result_map, experience_result_map]
  outputs: [rereview_verdict_map, newly_found_findings]
```

### 5.23 `register_new_findings_if_any`
```yaml
REGISTER-NEW-FINDINGS-IF-ANY:
  inputs: [rereview_verdict_map, issue_inventory]
  outputs: [new_issue_registrations, updated_issue_inventory]
```

### 5.24 `continue_loop_until_open_issue_zero`
```yaml
CONTINUE-LOOP-UNTIL-OPEN-ISSUE-ZERO:
  inputs: [full_issue_inventory, clearance_gate]
  outputs: [loop_decision, next_required_action, remaining_open_issue_count]
```

### 5.25 `must_run_tool_gate`
```yaml
MUST-RUN-TOOL-GATE:
  inputs: [must_run_tools, executed_tools]
  outputs: [tool_gate_result, missing_tools]
```

### 5.26 `autofill_exec_report`
```yaml
AUTOFILL-EXEC-REPORT:
  inputs: [exec_plan, executed_changes, tool_outputs]
  outputs: [exec_report]
```

### 5.27 `generate_validation_bundle`
```yaml
GENERATE-VALIDATION-BUNDLE:
  inputs: [exec_report, changed_scope, risk_notes]
  outputs: [qa_validation_plan, qa_verification_result_draft, validation_bundle]
```

### 5.28 `experience_replay`
```yaml
EXPERIENCE-REPLAY:
  inputs: [exec_plan, validation_bundle, expected_user_path]
  outputs: [experience_check, confidence_level, experience_risks]
```

### 5.29 `compute_tool_coverage_score`
```yaml
COMPUTE-TOOL-COVERAGE-SCORE:
  inputs: [must_run_tools, executed_tools]
  outputs: [tool_coverage_score, tool_coverage_reason]
```

### 5.30 `compute_evidence_completeness_score`
```yaml
COMPUTE-EVIDENCE-COMPLETENESS-SCORE:
  inputs: [exec_report, validation_bundle, protocol_payloads, tool_outputs]
  outputs: [evidence_completeness_score, evidence_completeness_reason]
```

### 5.31 `tool_result_landing_check`
```yaml
TOOL-RESULT-LANDING-CHECK:
  inputs: [tool_outputs, current_protocol_payloads]
  outputs: [landing_result, missing_fields, orphan_results]
```

### 5.32 `compute_reopen_risk_score`
```yaml
COMPUTE-REOPEN-RISK-SCORE:
  inputs: [review_findings, validation_failures, experience_failures, tool_warnings]
  outputs: [reopen_risk_score, reopen_risk_reason]
```

### 5.33 `auto_reopen_on_drift`
```yaml
AUTO-REOPEN-ON-DRIFT:
  inputs: [review_findings, validation_failures, tool_warnings, experience_failures, reopen_risk_score]
  outputs: [reopen_reason, reopen_target_scope]
```

### 5.34 `auto_docs_sink`
```yaml
AUTO-DOCS-SINK:
  inputs: [p9_review_verdict, validation_results, experience_check]
  outputs: [docs_knowledge_update, sop_draft, hgs_closeout]
```

### 5.35 `compute_closeout_readiness_score`
```yaml
COMPUTE-CLOSEOUT-READINESS-SCORE:
  inputs: [exec_report, validation_bundle, experience_check, docs_sink_result, protocol_landing_result]
  outputs: [closeout_readiness_score, closeout_readiness_reason]
```

### 5.36 `closeout_candidate_check`
```yaml
CLOSEOUT-CANDIDATE-CHECK:
  inputs: [exec_report, validation_bundle, experience_check, protocol_landing_result, closeout_readiness_score, reopen_risk_score]
  outputs: [closeout_candidate_result, final_closeout_blockers]
```

---

## 6. 分数驱动决策映射

```yaml
SCORE-DECISION-RULES:
  dispatch:
    require_owner_confidence_gte: 70
    require_route_stability_gte: 65
    else: "route_dry_run_or_p9_reframe_and_redispatch"
  review:
    require_tool_coverage_gte: 85
    require_evidence_completeness_gte: 80
    else: "tool_missing_or_evidence_incomplete"
  reopen:
    when_reopen_risk_gte: 60
    action: "auto_reopen_on_drift"
  done:
    require_closeout_readiness_gte: 85
    require_reopen_risk_lt: 60
    else: "auto_reopen_on_drift_or_auto_docs_sink_then_recheck"
```

---

## 7. 硬闸门映射

```yaml
AUTOMATION-HARD-GATES:
  - name: "require_issue_stub_before_dispatch"
    fail_state: "owner_unclear"
  - name: "require_score_gates_before_dispatch"
    fail_state: "reroute_required"
  - name: "require_route_dry_run_when_owner_confidence_below_threshold"
    fail_state: "reroute_required"
  - name: "require_tool_gate_before_dispatch"
    fail_state: "tool_missing"
  - name: "require_high_risk_guard_before_sensitive_execution"
    fail_state: "blocked"
  - name: "require_auth_bypass_guard_when_auth_scope_or_object_risk_present"
    fail_state: "blocked"
  - name: "require_runtime_stability_gate_when_runtime_identity_heartbeat_or_trace_risk_present"
    fail_state: "blocked"
  - name: "require_exec_plan_before_execution"
    fail_state: "evidence_incomplete"
  - name: "require_exec_report_before_review"
    fail_state: "evidence_incomplete"
  - name: "require_validation_bundle_before_review"
    fail_state: "evidence_incomplete"
  - name: "require_experience_replay_when_real_feedback_missing"
    fail_state: "evidence_incomplete"
  - name: "require_score_gates_before_review"
    fail_state: "evidence_incomplete"
  - name: "require_protocol_landing_before_review"
    fail_state: "evidence_incomplete"
  - name: "require_auto_reroute_on_new_truth"
    fail_state: "reroute_required"
  - name: "require_auto_reopen_on_drift"
    fail_state: "reopen_required"
  - name: "require_auto_docs_sink_before_done"
    fail_state: "docs_sink"
  - name: "require_score_gates_before_done"
    fail_state: "reopen_required"
  - name: "require_closeout_candidate_check_before_done"
    fail_state: "reopen_required"
  - name: "require_fallback_to_p8_enhanced_on_repeated_failure"
    fail_state: "reroute_required"
```

---

## 8. 结论

本协议的使命只有一个：

**让 HGS 的自动化联动不仅“有动作”，还“能按分数自动决定是否派单、是否 reopen、是否 close”，并把关键门禁与清零动作提升为正式 active 动作集。**
