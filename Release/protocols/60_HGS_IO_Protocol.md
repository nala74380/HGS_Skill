---
name: hgs-io-protocol
description: HGS 正式发布版统一 I/O 协议。定义批次、问题台账、执行回包、体验验证、复审裁决与收口数据结构。
version: formal-2026-03-31-ie1
author: OpenAI
role: Protocol
status: active
---

# HGS I/O Protocol

本文件是正式发布版唯一的产物协议源。  
任何角色文件都可以定义“如何思考、如何审查、如何执行”，但**不能私自发明另一套回包格式**。

---

## 统一原则

1. 一个批次只有一个 `batch_id`
2. 一个 issue 只有一个 `issue_id`
3. 一个 issue 同时只能有一个 owner
4. 执行、体验、复审都必须引用同一个 `issue_id`
5. 未进入 `ISSUE-LEDGER` 的问题，不得直接执行
6. 未产生 `P8-EXEC-REPORT` 的 issue，不得进入 P9 复审
7. 未产生体验证据，不得把 `review_result=pass` 伪装成用户体验闭环
8. 在升级问用户之前，必须先完成内部协商与上级裁决记录
9. 所有状态流转必须落在主装配器定义的状态机之内

---

## 1. HGS-BATCH-HEADER

```yaml
HGS-BATCH-HEADER:
  batch_id: "BATCH-20260331-001"
  route_mode: "full_loop"
  input_scope:
    - "<uploaded_file_or_source_1>"
    - "<uploaded_file_or_source_2>"
  source_of_truth:
    - "<primary_source_1>"
  objective: "<本批次想达成什么>"
  stop_conditions:
    - "需要用户业务取舍"
    - "涉及不可逆删除/覆盖"
    - "需要真实外发给用户/代理"
  close_rule: "P9复审通过 + 体验证据达标 + 无P10阻断"
```

字段要求：

- `batch_id`：全批次唯一
- `route_mode`：固定为 `full_loop`
- `input_scope`：本轮实际处理对象
- `source_of_truth`：可回查的唯一真相来源
- `stop_conditions`：明确何时必须停下
- `close_rule`：收口条件

---

## 2. ISSUE-LEDGER

```yaml
ISSUE-LEDGER:
  - issue_id: "ISSUE-001"
    title: "<简明问题名>"
    owner: "p8-backend | p8-frontend | p8-pc-console | p8-lanren-jingling | p8-agent | p8-enduser | p8-pua-enhanced"
    severity: "P0 | P1 | P2 | P3"
    evidence:
      - "<证据1>"
      - "<证据2>"
    source_of_truth:
      - "<具体文件/接口/路径>"
    acceptance_criteria:
      - "<通过标准1>"
      - "<通过标准2>"
    max_change_boundary:
      - "<允许改动范围>"
    upgrade_rule:
      - "failure_count >= 2 -> p8-pua-enhanced"
      - "路线冲突 -> p10"
    status: "todo"
```

约束：

- `owner` 必须唯一
- `acceptance_criteria` 必须可验证
- `max_change_boundary` 必须写清楚，不能使用“视情况而定”
- `status` 只能使用主状态机允许值

---

## 2.5 INTERNAL-DELIBERATION

```yaml
INTERNAL-DELIBERATION:
  issue_id: "ISSUE-001"
  current_owner: "p8-backend"
  attempted_internal_options:
    - option: "<已尝试的内部解法>"
      owner: "<谁尝试>"
      result: "failed | partial | blocked"
      why_not_enough: "<为什么还不够>"
  peer_consultation:
    - consulted_role: "p9-principal | p8-pua-enhanced | p10-cto | other-owner"
      advice: "<给出的解法或裁决>"
      outcome: "adopted | rejected | insufficient"
  exhausted: false
  next_internal_step: "<下一步内部动作>"
```

约束：

- 只要 `exhausted=false`，不得升级问用户
- 任何用户升级请求前，必须先有至少一份 `INTERNAL-DELIBERATION`

## 2.6 ASSUMPTION-LOG

```yaml
ASSUMPTION-LOG:
  issue_id: "ISSUE-001"
  assumptions:
    - assumption: "<当前采用的假设>"
      reason: "<为什么当前可暂采纳>"
      impact_if_wrong: "<若假设错误会影响什么>"
      mitigation: "<如何控制风险>"
```

## 3. P8-EXEC-REPORT

```yaml
P8-EXEC-REPORT:
  issue_id: "ISSUE-001"
  changed_scope:
    - "<改动文件/模块/配置>"
  hypothesis_log:
    - hypothesis: "<假设>"
      verification_method: "<验证方法>"
      result: "<已否定/已确认/部分成立>"
  verification_level: "L1 | L2 | L3 | L4"
  acceptance_check:
    - criterion: "<验收项>"
      result: "pass | fail | partial"
  residual_risks:
    - "<剩余风险>"
  need_p9_review: true
  need_p10_escalation: false
```

约束：

- 必须显式包含假设追踪
- `verification_level` 不得空缺
- 不能只写“已修复，请复测”

---

## 4. HGS-EXPERIENCE-CHECK

```yaml
HGS-EXPERIENCE-CHECK:
  issue_id: "ISSUE-001"
  actor: "agent | enduser | admin | operator"
  evidence_type: "real_feedback | path_replay"
  journey: "<触发路径/操作旅程>"
  before: "<修复前摩擦>"
  after: "<修复后表现>"
  friction_removed: true
  remaining_friction:
    - "<仍残留的摩擦>"
  confidence: "low | medium | high"
  evidence:
    - "<真实反馈/路径复演证据>"
```

约束：

- `actor` 必须真实对应体验来源
- `confidence=high` 时必须有足够证据
- 没有真实反馈时可用路径复演，但必须明示不是外部真人确认

---

## 5. P9-REVIEW-VERDICT

```yaml
P9-REVIEW-VERDICT:
  issue_id: "ISSUE-001"
  review_result: "pass | rework | escalate"
  cross_module_impacts:
    - "<跨模块影响>"
  drift_check:
    naming_consistency: "pass | drift"
    enum_consistency: "pass | drift"
    interface_boundary: "pass | drift"
    error_handling: "pass | drift"
  pattern_freeze:
    required: true
    pattern_name: "<如需固化的模式名>"
  next_action: "<close | reopen | escalate_to_p10>"
```

---

## 6. P10-FINAL-DECISION

```yaml
P10-FINAL-DECISION:
  batch_id: "BATCH-20260331-001"
  issue_id: "ISSUE-001"
  decision: "approve | defer | reject | reroute"
  reason: "<战略/边界/优先级说明>"
  strategic_risk:
    - "<战略风险>"
  next_batch_advice:
    - "<下批次建议>"
```

使用时机：

- 路线冲突
- 优先级变化
- 批次边界需要重定义
- 当前修复会锁死未来方向

---

## 7. HGS-CLOSEOUT

```yaml
HGS-CLOSEOUT:
  batch_id: "BATCH-20260331-001"
  closure_type: "full_closed | engineering_closed_experience_pending | reopened | escalated"
  closed_issue_ids:
    - "ISSUE-001"
  reopened_issue_ids:
    - "ISSUE-002"
  escalated_issue_ids:
    - "ISSUE-003"
  unresolved_risks:
    - "<未解决风险>"
  next_batch_advice:
    - "<下一批建议>"
```

---

## 状态机

```text
todo
→ in_review
→ dispatched
→ in_progress
→ verifying
→ experience_check
→ reviewing
→ done
```

允许的异常分支：

```text
in_progress → blocked
reviewing → rework
reviewing → escalate_to_p10
experience_check → reopen
```

---

## 禁止事项

- 禁止新增第二套 issue 台账格式
- 禁止把体验反馈写进执行回包里冒充体验证据
- 禁止绕过 `ISSUE-LEDGER` 直接派 P8
- 禁止在复审阶段偷偷扩大改动边界
- 禁止 `review_result=pass` 但 `next_action=reopen` 这类互相打架的字段组合


## 8. USER-ESCALATION-REQUEST

```yaml
USER-ESCALATION-REQUEST:
  issue_id: "ISSUE-001"
  why_internal_resolution_failed: "<为什么内部链路已穷尽>"
  options_considered:
    - "<已考虑方案1>"
    - "<已考虑方案2>"
  p9_position: "<P9 结论>"
  p10_position: "<P10 结论，如已介入>"
  exact_decision_needed_from_user: "<到底要用户决定什么>"
  safe_default_if_no_answer: "<若用户暂未回复，最安全默认动作是什么>"
```

约束：

- 没有 `USER-ESCALATION-REQUEST`，不得把普通不确定性包装成“需要用户拍板”
- `exact_decision_needed_from_user` 必须精确，禁止问泛化问题
