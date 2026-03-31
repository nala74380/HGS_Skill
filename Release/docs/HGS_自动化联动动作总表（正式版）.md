# HGS 自动化联动动作总表（正式版）

> 版本：formal-2026-03-31-r2  
> 定位：HGS 正式发布版的自动化联动治理文档。用于把“内部闭环优先、工具前置、角色协同、收口再审、评分驱动决策”从原则层升级为**动作层 + 闸门层 + 评分层**。  
> 说明：本文件不是运行入口，不替代 `MANIFEST.json` / `00_HGS_Master_Loader.md`；本文件定义的是**当前 active 自动化动作、分数阈值、决策规则与编排边界**。

---

# 一、当前正式状态

当前 HGS 自动化联动已经不是“准备接入”，而是：

- 第一批动作：**已接入 active chain**
- 第二批动作：**已接入 active chain**
- 第三批动作：**已接入 active chain**
- 第四批评分动作：**已接入 active chain**

当前 active 动作总数：**24 个**。

一句话：

**HGS 现在已经从“有动作建议”升级成“动作 + 闸门 + 分数共同驱动编排”。**

---

# 二、自动化联动总原则

## 1. 内部闭环优先
固定顺序：

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
任何命中工具前置场景的问题，必须：

```text
先跑工具
→ 再落协议字段
→ 再进入执行 / 复审 / closeout
```

## 3. 分数前置于关键决策
关键决策现在必须看分数：
- 派单前看 `owner_confidence` 与 `route_stability_score`
- review 前看 `tool_coverage_score` 与 `evidence_completeness_score`
- reopen 前看 `reopen_risk_score`
- done 前看 `closeout_readiness_score` 与 `reopen_risk_score`

## 4. 结果必须落点
任何动作都不能只停留在口头描述，必须至少落入：
- `ISSUE-LEDGER`
- 对应 Owner verdict
- `P8-EXEC-REPORT`
- `QA-VALIDATION-PLAN`
- `QA-VERIFICATION-RESULT`
- `HGS-EXPERIENCE-CHECK`
- `DOCS-KNOWLEDGE-UPDATE`
- `HGS-CLOSEOUT`

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

## 2. 内部协商层
- `owner_self_resolve_attempt`
- `peer_role_consult`
- `split_subissues`
- `fallback_to_p8_enhanced`
- `p9_reframe_and_redispatch`

## 3. 工具闸门层
- `must_run_tool_gate`
- `tool_result_landing_check`
- `high_risk_guard_gate`（已定义，尚未进入 active_actions）
- `auth_bypass_guard_gate`（已定义，尚未进入 active_actions）
- `runtime_stability_gate`（已定义，尚未进入 active_actions）

## 4. 执行与验证层
- `autofill_exec_report`
- `generate_validation_bundle`
- `experience_replay`

## 5. 回流与收口层
- `compute_reopen_risk_score`
- `auto_reopen_on_drift`
- `auto_docs_sink`
- `compute_closeout_readiness_score`
- `closeout_candidate_check`

## 6. review / close 评分层
- `compute_tool_coverage_score`
- `compute_evidence_completeness_score`

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
→ must_run_tool_gate
→ autofill_exec_report
→ generate_validation_bundle
→ experience_replay
→ compute_tool_coverage_score
→ compute_evidence_completeness_score
→ tool_result_landing_check
→ compute_reopen_risk_score
→ auto_reopen_on_drift
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

## 1. dispatch 规则
只有同时满足：
- `owner_confidence >= 70`
- `route_stability_score >= 65`

才允许直接 dispatch。否则：
- `route_dry_run`
- 必要时 `p9_reframe_and_redispatch`

## 2. review 规则
只有同时满足：
- `tool_coverage_score >= 85`
- `evidence_completeness_score >= 80`
- `P8-EXEC-REPORT` 已存在
- `validation bundle` 已存在

才允许进入 review。否则：
- `tool_missing`
- 或 `evidence_incomplete`

## 3. reopen 规则
只要满足任一：
- `reopen_risk_score >= 60`
- QA / review / experience / tools 发现 drift

则自动执行：
- `auto_reopen_on_drift`
- 必要时 `p9_reframe_and_redispatch`

## 4. done 规则
只有同时满足：
- `closeout_readiness_score >= 85`
- `reopen_risk_score < 60`
- `closeout_candidate_check = pass`
- `auto_docs_sink` 已完成

才允许进入 `done`。

---

# 七、正式硬闸门

当前已正式生效的关键硬闸门：

1. 未创建 `ISSUE-LEDGER stub` 不得派单
2. 未通过分数闸门不得派单
3. 未通过工具闸门不得派单
4. 无 `P8-EXEC-REPORT` 不得 review
5. 无 `validation bundle` 不得 review
6. 无真实体验反馈时必须先 `experience_replay`
7. 无协议落点不得 review / done
8. `reopen_risk >= 60` 时不得 close
9. 未完成 `auto_docs_sink` 不得 done
10. 未通过 `closeout_candidate_check` 不得 done
11. 重复失败时必须 `fallback_to_p8_enhanced`

---

# 八、当前未进入 active chain 但已定义的动作

以下动作已在治理文档中定义，但当前仍未进入 `MANIFEST.active_actions`：

- `generate_exec_plan`
- `auto_reroute_on_new_truth`
- `high_risk_guard_gate`
- `auth_bypass_guard_gate`
- `runtime_stability_gate`

说明：
- 这不代表它们无效
- 只代表它们尚未被提升为“自动编排硬动作”

---

# 九、当前最重要的治理结论

1. HGS 自动化联动已从“建议动作”升级为“正式 active 动作集”。
2. 评分动作已成为编排决策的正式依据，而非辅助参考。 
3. 关键入口、review、reopen、done 已形成分数驱动闸门。 
4. 当前剩余问题主要不在动作缺失，而在于：
   - 个别治理文档仍需继续同频
   - 部分已定义动作尚未进入 active chain

---

# 十、结论

本总表当前阶段的使命只有一个：

**明确告诉整个 HGS：哪些动作已经正式生效、哪些分数会影响派单/复审/重开/收口、哪些规则已经不再只是建议。**
