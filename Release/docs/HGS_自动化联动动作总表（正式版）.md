# HGS 自动化联动动作总表（正式版）

> 版本：formal-2026-03-31-r3  
> 定位：HGS 正式发布版的自动化联动治理文档。用于把“内部闭环优先、工具前置、角色协同、收口再审、评分驱动决策、持续回流直到清零”从原则层升级为**动作层 + 闸门层 + 评分层 + 清零治理层**。  
> 说明：本文件不是运行入口，不替代 `MANIFEST.json` / `00_HGS_Master_Loader.md`；本文件定义的是**当前 active 自动化动作、分数阈值、决策规则、清零规则与编排边界**。

---

# 一、当前正式状态

当前 HGS 自动化联动已经不是“准备接入”，而是：

- 第一批动作：**已接入 active chain**
- 第二批动作：**已接入 active chain**
- 第三批动作：**已接入 active chain**
- 第四批评分动作：**已接入 active chain**
- 清零治理协议：**已接入 active chain**

当前 active 动作总数：**24 个**。  
当前新增硬治理协议：**`62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md`**。

一句话：

**HGS 现在已经从“有动作建议”升级成“动作 + 闸门 + 分数 + 清零协议共同驱动编排”。**

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

## 4. 清零优先于提前收口
每次全局审查、QA、体验、复审的新发现都必须：

```text
全部登记
→ 全部归属 owner
→ 全部派单
→ 全部进入测试 / 体验 / 复审
→ 再发现再继续回流
→ 直到 open_issue_count = 0
→ 才允许收口
```

## 5. 结果必须落点
任何动作都不能只停留在口头描述，必须至少落入：
- `ISSUE-LEDGER`
- `FULL-ISSUE-INVENTORY`
- `CLEARANCE-CYCLE-REPORT`
- `CLEARANCE-GATE`
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

## 7. 清零治理层
- `62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md`（协议驱动）
- `FULL-ISSUE-INVENTORY`
- `CLEARANCE-CYCLE-REPORT`
- `CLEARANCE-GATE`

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

全局审查场景下，还必须叠加：

```text
register_all_findings
→ dispatch_all_registered_issues
→ execute_by_owner
→ validate_and_experience_by_issue
→ rereview_all_open_issues
→ register_new_findings_if_any
→ continue_loop_until_open_issue_zero
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
- `open_issue_count = 0`

才允许进入 `done`。

---

# 七、清零治理规则（当前正式规则）

## 1. 所有发现必须登记
任何审查、复审、测试、体验、工具输出新发现的问题，必须全部登记进：
- `ISSUE-LEDGER`
- 子 issue 清单
- `FULL-ISSUE-INVENTORY`

## 2. 所有已登记问题必须派单
只要 owner 可判定且不触发硬停机条件，就必须全部派单。允许分波次执行，但不允许分波次遗忘。

## 3. 谁的问题谁处理
每个问题必须有：
- `issue_id`
- `owner`
- `status`
- `required_tools`
- `required_validation`
- `required_experience_if_any`

## 4. 处理后必须测试 / 体验 / 复审
禁止“修完就算完”。

## 5. 再发现问题必须继续回流
新问题必须立即登记、立即归属、立即派单。

## 6. 只有清零才允许收口
只有同时满足：
- `open_issue_count = 0`
- `review_pending_count = 0`
- `verification_pending_count = 0`
- `experience_pending_count = 0`
- `docs_sink_pending_count = 0`

才允许 `done`。

---

# 八、正式硬闸门

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
12. review 前必须完成所有发现问题登记
13. done 前必须存在 `FULL-ISSUE-INVENTORY`
14. `open_issue_count > 0` 时不得 done

---

# 九、当前未进入 active chain 但已定义的动作

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

# 十、当前最重要的治理结论

1. HGS 自动化联动已从“建议动作”升级为“正式 active 动作集”。
2. 评分动作已成为编排决策的正式依据，而非辅助参考。 
3. 关键入口、review、reopen、done 已形成分数驱动闸门。 
4. 清零协议已正式进入装配链，`open_issue_count = 0` 已成为 closeout 的必要条件。 
5. 当前剩余问题主要不在主规则缺失，而在于：
   - 个别治理文档仍需继续同频
   - 部分已定义动作尚未进入 active chain

---

# 十一、结论

本总表当前阶段的使命只有一个：

**明确告诉整个 HGS：哪些动作已经正式生效、哪些分数会影响派单/复审/重开/收口、以及“未清零不得收口”已经是正式硬规则。**
