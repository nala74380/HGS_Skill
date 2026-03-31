---
name: automation-orchestration-protocol
description: HGS 自动编排协议。定义自动化联动动作的统一记录结构、状态字段、评分字段与最小输入输出骨架，供 Loader 与自动化动作共同使用。
version: formal-2026-03-31-p2
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

本协议不替代：
- `60_HGS_IO_Protocol.md`
- 各角色 verdict / exec / review 协议

本协议只负责：

**把自动化动作从“文字描述”变成可记录、可审计、可回放的结构。**

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
  inputs:
    - batch_id
    - input_scope
    - source_of_truth
    - raw_problem_statement
  outputs:
    - issue_id
    - issue_stub
    - initial_risk_flags
    - source_of_truth_scope
```

### 5.2 `infer_owner_candidates`

```yaml
INFER-OWNER-CANDIDATES:
  inputs:
    - issue_stub
    - problem_type
    - risk_flags
  outputs:
    - primary_owner_candidate
    - secondary_owner_candidates
    - owner_confidence
    - owner_reasoning
```

### 5.3 `infer_required_tools`

```yaml
INFER-REQUIRED-TOOLS:
  inputs:
    - primary_owner_candidate
    - problem_type
    - risk_flags
  outputs:
    - must_run_tools
    - optional_tools
    - tool_reasoning
```

### 5.4 `route_dry_run`

```yaml
ROUTE-DRY-RUN:
  inputs:
    - issue_stub
    - owner_candidates
    - must_run_tools
  outputs:
    - simulated_route
    - missing_steps
    - route_conflicts
    - must_trigger_tools
```

### 5.5 `provisional_boundary_build`

```yaml
PROVISIONAL-BOUNDARY-BUILD:
  inputs:
    - issue_stub
    - route_dry_run_output
    - risk_flags
  outputs:
    - provisional_boundary
    - allowed_actions
    - forbidden_actions
    - assumption_log
```

### 5.6 `owner_self_resolve_attempt`

```yaml
OWNER-SELF-RESOLVE-ATTEMPT:
  inputs:
    - primary_owner
    - must_run_tool_outputs
    - provisional_or_final_boundary
  outputs:
    - attempted_actions
    - blocked_points
    - remaining_uncertainties
    - self_resolve_result
```

### 5.7 `peer_role_consult`

```yaml
PEER-ROLE-CONSULT:
  inputs:
    - primary_owner
    - secondary_owner_candidates
    - blocked_points
    - tool_outputs
  outputs:
    - consulted_roles
    - shared_findings
    - alignment_result
    - new_owner_boundary_if_any
```

### 5.8 `split_subissues`

```yaml
SPLIT-SUBISSUES:
  inputs:
    - issue_ledger
    - consulted_roles
    - tool_outputs
  outputs:
    - subissue_list
    - subissue_owner_map
    - subissue_tool_map
    - merge_back_rule
```

### 5.9 `fallback_to_p8_enhanced`

```yaml
FALLBACK-TO-P8-ENHANCED:
  inputs:
    - issue_ledger
    - failure_history
    - tool_outputs
  outputs:
    - fallback_reason
    - enhanced_takeover_scope
```

### 5.10 `p9_reframe_and_redispatch`

```yaml
P9-REFRAME-AND-REDISPATCH:
  inputs:
    - issue_ledger
    - subissue_list
    - tool_outputs
    - fallback_reason
  outputs:
    - redispatch_plan
    - new_owner
    - new_tool_order
    - acceptance_boundary
```

### 5.11 `must_run_tool_gate`

```yaml
MUST-RUN-TOOL-GATE:
  inputs:
    - must_run_tools
    - executed_tools
  outputs:
    - tool_gate_result
    - missing_tools
```

### 5.12 `autofill_exec_report`

```yaml
AUTOFILL-EXEC-REPORT:
  inputs:
    - exec_plan
    - executed_changes
    - tool_outputs
  outputs:
    - exec_report
```

### 5.13 `generate_validation_bundle`

```yaml
GENERATE-VALIDATION-BUNDLE:
  inputs:
    - exec_report
    - changed_scope
    - risk_notes
  outputs:
    - qa_validation_plan
    - qa_verification_result_draft
    - validation_bundle
```

### 5.14 `tool_result_landing_check`

```yaml
TOOL-RESULT-LANDING-CHECK:
  inputs:
    - tool_outputs
    - current_protocol_payloads
  outputs:
    - landing_result
    - missing_fields
    - orphan_results
```

### 5.15 `closeout_candidate_check`

```yaml
CLOSEOUT-CANDIDATE-CHECK:
  inputs:
    - exec_report
    - validation_bundle
    - experience_check
    - protocol_landing_result
  outputs:
    - closeout_readiness_score
    - reopen_risk_score
    - closeout_candidate_result
```

---

## 6. 硬闸门映射

```yaml
AUTOMATION-HARD-GATES:
  - name: "require_issue_stub_before_dispatch"
    fail_state: "owner_unclear"
  - name: "require_route_dry_run_when_owner_confidence_below_threshold"
    fail_state: "reroute_required"
  - name: "require_tool_gate_before_dispatch"
    fail_state: "tool_missing"
  - name: "require_exec_report_before_review"
    fail_state: "evidence_incomplete"
  - name: "require_validation_bundle_before_review"
    fail_state: "evidence_incomplete"
  - name: "require_protocol_landing_before_review"
    fail_state: "evidence_incomplete"
  - name: "require_closeout_candidate_check_before_done"
    fail_state: "reopen_required"
  - name: "require_fallback_to_p8_enhanced_on_repeated_failure"
    fail_state: "reroute_required"
```

---

## 7. 协议使用说明

- 任一自动化动作执行时，建议生成一份 `AUTOMATION-ACTION-RECORD`
- 若动作失败，应同步更新 `AUTOMATION-STATE`
- 若动作影响 closeout，应更新 `AUTOMATION-SCORES`
- 本协议与 `60_HGS_IO_Protocol.md` 应并行使用，而不是替代关系

---

## 8. 结论

本协议的使命只有一个：

**让 HGS 的自动化联动动作不仅“存在”，而且“有结构、能落点、能回放、能审计”。**
