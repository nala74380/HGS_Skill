# HGS 自动化联动动作总表（正式版）

> 版本：formal-2026-03-31-r1  
> 定位：HGS 正式发布版的自动化联动治理文档。用于把“内部闭环优先、工具前置、角色协同、收口再审”从原则层升级为**动作层**。  
> 说明：本文件不是运行入口，不替代 `MANIFEST.json` / `00_HGS_Master_Loader.md`；本文件定义的是**自动化联动动作清单与编排规则**，供后续接入 Loader 与 automation policy 使用。

---

# 一、文档目标

HGS 当前已经具备：

- Manifest 驱动装配
- Master Loader 总入口
- Roles / Tools / Protocols / Docs
- 内部闭环优先
- 工具前置规则
- P10 / Owner / P9 / P8 / QA / SRE / Docs 主链

但要继续提升自动化联动，不能只停留在“原则正确”，必须升级到：

```text
动作名
→ 触发条件
→ 输入
→ 输出
→ 下一跳
→ 禁止跳过条件
```

一句话：

**把“应该这样协同”升级成“系统必须这样动作”。**

---

# 二、自动化联动总原则

## 1. 内部闭环优先

固定顺序：

```text
当前 owner 自救
→ 平级协商 / 拆子问题
→ 工具压实证据
→ P9 重构与再派单
→ P10 路线重裁
→ 仅在内部方案穷尽后才升级问用户
```

## 2. 工具前置于拍板与执行

任何命中工具前置场景的问题，必须：

```text
先跑工具
→ 再落协议字段
→ 再进入执行 / 复审 / closeout
```

## 3. 闭环优先于停机

只要还存在：
- 可局部验证路径
- 可非破坏性推进路径
- 可拆子问题路径
- 可低置信复演路径

就不得直接停下来问用户。

## 4. 结果必须落点

任何动作都不能只停留在口头描述，必须至少落入：
- `ISSUE-LEDGER`
- 对应 Owner verdict
- `P8-EXEC-REPORT`
- `QA-VALIDATION-PLAN`
- `QA-VERIFICATION-RESULT`
- `DOCS-KNOWLEDGE-UPDATE`
- `HGS-CLOSEOUT`

---

# 三、动作分层总览

HGS 自动化联动动作分为 6 层：

## 1. 入口标准化层
- `create_issue_stub`
- `infer_owner_candidates`
- `infer_required_tools`
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
- `high_risk_guard_gate`
- `auth_bypass_guard_gate`
- `runtime_stability_gate`

## 4. 执行与验证层
- `generate_exec_plan`
- `autofill_exec_report`
- `generate_validation_bundle`
- `experience_replay`
- `closeout_candidate_check`

## 5. 回流与重开环层
- `auto_reopen_on_drift`
- `auto_reroute_on_new_truth`
- `auto_docs_sink`

## 6. 评分与闸门层
- `compute_owner_confidence`
- `compute_tool_coverage_score`
- `compute_evidence_completeness_score`
- `compute_route_stability_score`
- `compute_closeout_readiness_score`
- `compute_reopen_risk_score`

---

# 四、正式动作总表

## A. 入口标准化层

---

### 01. `create_issue_stub`

#### 作用
自动创建最小可追踪 issue 外壳，避免“还没立账就开始执行”。

#### 触发条件
- 用户提交新批次输入
- 当前会话首次识别到新 issue
- 旧 issue 不适用于当前输入范围

#### 输入
- `batch_id`
- `input_scope`
- `source_of_truth`
- `raw_problem_statement`

#### 输出
- `ISSUE-LEDGER.stub`
- `issue_id`
- `source_of_truth_scope`
- `initial_risk_flags`

#### 下一跳
- `infer_owner_candidates`

#### 禁止跳过条件
- 未创建 `ISSUE-LEDGER` 不得派单给 P8
- 未创建 `ISSUE-LEDGER` 不得宣称“开始执行”

---

### 02. `infer_owner_candidates`

#### 作用
自动给出主 owner 候选、次 owner 候选与置信度。

#### 触发条件
- `create_issue_stub` 完成后
- issue reopen 后重新判 owner
- 工具发现当前 owner 可能错误时

#### 输入
- `ISSUE-LEDGER.stub`
- `problem_type`
- `risk_flags`
- `source_of_truth_scope`

#### 输出
- `primary_owner_candidate`
- `secondary_owner_candidates`
- `owner_confidence`
- `owner_reasoning`

#### 下一跳
- `infer_required_tools`
- 若 `owner_confidence` 低，则进入 `route_dry_run`

#### 禁止跳过条件
- owner 未判定前不得直接进入正式派单

---

### 03. `infer_required_tools`

#### 作用
自动推断本 issue 必须先跑的工具与可选工具。

#### 触发条件
- 已有 owner 候选
- issue 类型已初步确定

#### 输入
- `primary_owner_candidate`
- `problem_type`
- `risk_flags`
- `governance_docs`

#### 输出
- `must_run_tools`
- `optional_tools`
- `tool_reasoning`

#### 下一跳
- `route_dry_run` 或 `must_run_tool_gate`

#### 禁止跳过条件
- 命中工具前置场景时，不得在没有 `must_run_tools` 的情况下进入执行

---

### 04. `route_dry_run`

#### 作用
先做 dry-run 路由预演，发现错派、漏工具、漏验证、漏沉淀。

#### 触发条件
- `owner_confidence < 阈值`
- mixed issue
- 多 owner 依赖
- 新角色 / 新工具刚接入
- 怀疑自动链路会走歪

#### 输入
- `ISSUE-LEDGER.stub`
- `owner_candidates`
- `must_run_tools`

#### 工具绑定
- `108_Chain_Route_Simulator_SKILL.md`

#### 输出
- `simulated_route`
- `missing_steps`
- `route_conflicts`
- `must_trigger_tools`

#### 下一跳
- `provisional_boundary_build` 或 `p9_reframe_and_redispatch`

#### 禁止跳过条件
- owner 低置信 / route 不稳定时不得直接派单

---

### 05. `provisional_boundary_build`

#### 作用
边界尚不够精确时，先生成临时边界，允许非破坏性推进。

#### 触发条件
- `source_of_truth` 部分不清晰
- `max_change_boundary` 暂不够精确
- 但仍存在可安全推进路径

#### 输入
- `ISSUE-LEDGER.stub`
- `route_dry_run.output`
- `risk_flags`

#### 输出
- `provisional_boundary`
- `allowed_actions`
- `forbidden_actions`
- `assumption_log`

#### 下一跳
- `owner_self_resolve_attempt`

#### 禁止跳过条件
- 边界不稳时不得直接进入破坏性执行

---

## B. 内部协商层

---

### 06. `owner_self_resolve_attempt`

#### 作用
让当前 owner 先完成第一轮自救，而不是马上抛给用户。

#### 触发条件
- 已有主 owner
- 已有 provisional 或正式边界

#### 输入
- `primary_owner`
- `must_run_tools.output`
- `provisional_boundary`

#### 输出
- `attempted_actions`
- `blocked_points`
- `remaining_uncertainties`
- `self_resolve_result`

#### 下一跳
- 成功则 `generate_exec_plan`
- 失败则 `peer_role_consult`

#### 禁止跳过条件
- 未进行 self-resolve，不得直接升级问用户

---

### 07. `peer_role_consult`

#### 作用
自动拉相邻角色协商，而不是把不确定性直接丢给用户。

#### 触发条件
- 当前 owner 自救失败
- 问题天然跨角色
- 工具显示多 owner 交叉依赖

#### 输入
- `primary_owner`
- `secondary_owner_candidates`
- `blocked_points`
- `tool_outputs`

#### 输出
- `consulted_roles`
- `shared_findings`
- `alignment_result`
- `new_owner_boundary_if_any`

#### 下一跳
- `split_subissues` 或 `p9_reframe_and_redispatch`

#### 禁止跳过条件
- 平级角色可协商时，不得直接升级给用户

---

### 08. `split_subissues`

#### 作用
把 mixed issue 自动拆成多个子问题，每个子问题对应一个 owner / 工具组。

#### 触发条件
- mixed issue
- 多 owner 交叉依赖
- 一个 issue 内包含规则、执行、体验、验证多种问题

#### 输入
- `ISSUE-LEDGER`
- `consulted_roles`
- `tool_outputs`

#### 输出
- `subissue_list`
- `subissue_owner_map`
- `subissue_tool_map`
- `merge_back_rule`

#### 下一跳
- `fallback_to_p8_enhanced` 或 `p9_reframe_and_redispatch`

#### 禁止跳过条件
- mixed issue 不得以“一个 P8 通吃”方式强行执行

---

### 09. `fallback_to_p8_enhanced`

#### 作用
owner 不清、失败次数过多、证据碎片化时自动兜底。

#### 触发条件
- `failure_count >= 2`
- owner 不稳
- `route_stability_score` 低
- 需要更强约束式诊断

#### 输入
- `ISSUE-LEDGER`
- `failure_history`
- `tool_outputs`

#### 输出
- `fallback_reason`
- `enhanced_takeover_scope`

#### 下一跳
- `p9_reframe_and_redispatch`

#### 禁止跳过条件
- 明显需要兜底时不得继续原 owner 盲试

---

### 10. `p9_reframe_and_redispatch`

#### 作用
由 P9 重构 issue、重定边界、重排 owner 与工具顺序。

#### 触发条件
- peer consult 未收敛
- fallback 后仍需正式派单
- route dry-run 显示错派 / 漏环节
- 工具发现新真相改变 owner

#### 输入
- `ISSUE-LEDGER`
- `subissue_list`
- `tool_outputs`
- `fallback_reason`

#### 输出
- `redispatch_plan`
- `new_owner`
- `new_tool_order`
- `acceptance_boundary`

#### 下一跳
- `must_run_tool_gate` 或 `generate_exec_plan`

#### 禁止跳过条件
- 需要重构 issue 时不得让各角色各修各的

---

## C. 工具闸门层

---

### 11. `must_run_tool_gate`

#### 作用
检查本 issue 命中的前置工具是否已全部执行。

#### 触发条件
- 进入正式派单前
- 进入复审前
- 进入 closeout 前

#### 输入
- `must_run_tools`
- `executed_tools`

#### 输出
- `tool_gate_result`
- `missing_tools`

#### 下一跳
- 通过则 `generate_exec_plan`
- 不通过则补跑缺失工具

#### 禁止跳过条件
- 未满足工具前置要求，不得进入 P8 执行

---

### 12. `tool_result_landing_check`

#### 作用
检查工具结果是否已正确落入协议字段，而不是悬空在聊天过程里。

#### 触发条件
- 工具执行后
- 复审前
- closeout 前

#### 输入
- `tool_outputs`
- `current_protocol_payloads`

#### 工具绑定
- `107_Protocol_Field_Completeness_Checker_SKILL.md`

#### 输出
- `landing_result`
- `missing_fields`
- `orphan_results`

#### 下一跳
- 通过则进入验证/复审
- 不通过则补字段

#### 禁止跳过条件
- 工具结果未落字段不得 close

---

### 13. `high_risk_guard_gate`

#### 作用
凡涉及高风险动作，先做门禁充分性审查。

#### 触发条件
- 删除
- 冻结
- 解绑
- 扣点
- 授权
- 回滚
- 批量高风险动作

#### 输入
- `action_name`
- `action_scope`
- `current_guards`

#### 工具绑定
- `109_High_Risk_Action_Guard_Checker_SKILL.md`

#### 输出
- `guard_result`
- `missing_guards`
- `required_actions`

#### 下一跳
- 通过则执行
- 不通过则转 Security / Backend / Console UX 补门禁

#### 禁止跳过条件
- 高风险动作不得无 `109` 直接执行

---

### 14. `auth_bypass_guard_gate`

#### 作用
凡涉及对象级授权、scope、project 边界、前端显隐代替授权等场景，先做绕过路径审查。

#### 触发条件
- project scope 争议
- object auth 争议
- 前端显隐不等于服务端权限
- 疑似越权访问

#### 输入
- `protected_resource`
- `actor_profile`
- `suspected_bypass_vectors`

#### 工具绑定
- `110_Authorization_Bypass_Path_Reviewer_SKILL.md`

#### 输出
- `bypass_review_result`
- `missing_checks`
- `risky_vectors`

#### 下一跳
- 通过则继续执行
- 不通过则转 Security / Auth / Backend / Control Plane

#### 禁止跳过条件
- 越权/绕过争议不得不跑 `110`

---

### 15. `runtime_stability_gate`

#### 作用
凡涉及运行主体、心跳、trace 链的争议，强制进入运行面工具链。

#### 触发条件
- Worker 主体漂移 / 重装迁移 / 重复注册
- 在线/离线争议 / 心跳缺口 / 恢复抖动
- 多系统 trace 割裂 / 运行链断点

#### 输入
- `runtime_issue_profile`
- `runtime_identifiers`
- `runtime_events`

#### 工具绑定
- `91_Worker_Identity_Stability_SKILL.md`
- `92_Heartbeat_Gap_Analyzer_SKILL.md`
- `98_Trace_Correlation_SKILL.md`

#### 输出
- `runtime_gate_result`
- `required_runtime_tools`
- `runtime_findings`

#### 下一跳
- `generate_exec_plan` 或 `p9_reframe_and_redispatch`

#### 禁止跳过条件
- 命中运行面问题，不得只靠抓包或猜测进入执行

---

## D. 执行与验证层

---

### 16. `generate_exec_plan`

#### 作用
把 owner 与工具结论压成可执行的 P8 计划。

#### 触发条件
- 工具闸门通过
- owner 已稳定
- boundary 已明确或 provisional 可接受

#### 输入
- `owner`
- `tool_outputs`
- `boundary`
- `acceptance_boundary`

#### 输出
- `exec_plan`
- `risk_notes`
- `required_evidence`
- `regression_scope`

#### 下一跳
- P8 执行

#### 禁止跳过条件
- 不得让 P8 在没有 exec plan 的情况下裸执行

---

### 17. `autofill_exec_report`

#### 作用
根据执行动作和工具结果自动回填 `P8-EXEC-REPORT`。

#### 触发条件
- P8 完成一轮执行
- 子问题完成
- 需要进入复审

#### 输入
- `exec_plan`
- `executed_changes`
- `tool_outputs`

#### 输出
- `P8-EXEC-REPORT`

#### 下一跳
- `generate_validation_bundle`

#### 禁止跳过条件
- 无 `P8-EXEC-REPORT` 不得进入复审

---

### 18. `generate_validation_bundle`

#### 作用
自动生成验证矩阵、回归清单与必要的体验/界面审查。

#### 触发条件
- 有执行报告
- 准备进入验证

#### 输入
- `P8-EXEC-REPORT`
- `changed_scope`
- `risk_notes`

#### 工具绑定
- `95_Test_Matrix_Builder_SKILL.md`
- `96_Regression_Checklist_SKILL.md`
- 必要时 `85_UI_Surface_Audit_SKILL.md`

#### 输出
- `QA-VALIDATION-PLAN`
- `QA-VERIFICATION-RESULT.draft`

#### 下一跳
- `experience_replay` 或正式 QA

#### 禁止跳过条件
- 没有 validation bundle 不得宣称“验证过了”

---

### 19. `experience_replay`

#### 作用
当真实用户/代理体验证据缺失时，做低置信体验复演，避免卡死。

#### 触发条件
- 无真实体验反馈
- 但工程与验证链基本完整

#### 输入
- `exec_plan`
- `validation_bundle`
- `expected_user_path`

#### 输出
- `HGS-EXPERIENCE-CHECK`
- `confidence_level`
- `experience_risks`

#### 下一跳
- `closeout_candidate_check`

#### 禁止跳过条件
- 缺真实体验证据时不得直接 close，至少要有 replay 结论

---

### 20. `closeout_candidate_check`

#### 作用
在 close 前做最终候选检查，防止“看起来差不多了”就关单。

#### 触发条件
- 复审前
- closeout 前

#### 输入
- `P8-EXEC-REPORT`
- `validation_bundle`
- `experience_check`
- `protocol_landing_result`

#### 输出
- `closeout_readiness_score`
- `reopen_risk_score`
- `closeout_candidate_result`

#### 下一跳
- 通过则 P9 复审 / Docs sink
- 不通过则 `auto_reopen_on_drift`

#### 禁止跳过条件
- readiness 未达标不得 close

---

## E. 回流与重开环层

---

### 21. `auto_reopen_on_drift`

#### 作用
当复审、QA、体验或工具发现 drift 时，自动 reopen。

#### 触发条件
- P9 复审失败
- QA 回归失败
- 体验复演失败
- 工具发现 owner 错派 / 协议断链 / 绕过风险

#### 输入
- `review_findings`
- `validation_failures`
- `tool_warnings`

#### 输出
- `reopen_reason`
- `reopen_target_scope`

#### 下一跳
- `infer_owner_candidates` 或 `p9_reframe_and_redispatch`

#### 禁止跳过条件
- 出现结构性 drift 时不得硬关单

---

### 22. `auto_reroute_on_new_truth`

#### 作用
工具或复审发现当前 owner 错误时，自动改派。

#### 触发条件
- 新真相出现
- 工具结论改变 issue 归属
- 原 owner 不再适用

#### 输入
- `new_truth_signal`
- `current_owner`
- `tool_outputs`

#### 输出
- `new_owner`
- `reroute_reason`

#### 下一跳
- `must_run_tool_gate` 或 `generate_exec_plan`

#### 禁止跳过条件
- owner 已明显错误时不得继续原链路盲修

---

### 23. `auto_docs_sink`

#### 作用
在 close 前自动判断是否需要沉淀为 SOP / 知识更新。

#### 触发条件
- 复审通过
- 问题具备可复用性
- 以后大概率会重复解释

#### 输入
- `P9-REVIEW-VERDICT`
- `validation_results`
- `experience_check`

#### 工具绑定
- `106_SOP_Generator_SKILL.md`
- `107_Protocol_Field_Completeness_Checker_SKILL.md`

#### 输出
- `DOCS-KNOWLEDGE-UPDATE`
- `SOP draft`
- `HGS-CLOSEOUT`

#### 下一跳
- `done`

#### 禁止跳过条件
- 明显可复用的问题，不得只修不沉淀

---

## F. 评分与闸门层

---

### 24. `compute_owner_confidence`

#### 作用
计算当前 owner 判断可信度。

#### 输出字段
- `owner_confidence: 0-100`

#### 用途
- 低于阈值时强制跑 `108`

---

### 25. `compute_tool_coverage_score`

#### 作用
计算本 issue 应跑工具的覆盖率。

#### 输出字段
- `tool_coverage_score: 0-100`

#### 用途
- 不足阈值时禁止进入 closeout

---

### 26. `compute_evidence_completeness_score`

#### 作用
计算证据与协议落点完整度。

#### 输出字段
- `evidence_completeness_score: 0-100`

#### 用途
- 低时强制跑 `107`

---

### 27. `compute_route_stability_score`

#### 作用
计算当前路由是否稳定、是否高概率改派。

#### 输出字段
- `route_stability_score: 0-100`

#### 用途
- 低时强制跑 `108`

---

### 28. `compute_closeout_readiness_score`

#### 作用
判断是否具备 close 条件。

#### 输出字段
- `closeout_readiness_score: 0-100`

#### 用途
- 未达阈值不得 close

---

### 29. `compute_reopen_risk_score`

#### 作用
判断当前结果被 reopen 的风险。

#### 输出字段
- `reopen_risk_score: 0-100`

#### 用途
- 高风险时先回流再 close

---

# 五、最优先落地的 10 个动作

若要分批接入 Loader，建议第一批先落这 10 个：

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

原因：

- 先把入口标准化
- 再把 owner 自动判断化
- 再把工具前置强制化
- 再把内部协商动作化
- 再把 closeout 闸门化

这 10 个动作落地后，自动化联动会立刻明显提升。

---

# 六、建议接入 Loader 的第一批硬规则

## 必须写成硬规则的 8 条

1. 进入 P8 前，必须先生成 `ISSUE-LEDGER stub`
2. `owner_confidence < 阈值` 时，必须先跑 `108_Chain_Route_Simulator`
3. 命中工具前置场景时，`must_run_tools` 未完成不得派单
4. 高风险动作必须先跑 `109_High_Risk_Action_Guard_Checker`
5. 越权 / scope / object auth 争议必须先跑 `110_Authorization_Bypass_Path_Reviewer`
6. 运行面争议必须先跑 `91 / 92 / 98`
7. 没有 `P8-EXEC-REPORT + validation bundle + protocol landing check` 不得 close
8. 出现 drift / wrong owner / failed experience 时自动 reopen，不问用户

---

# 七、建议扩展状态机

当前建议升级为：

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

建议异常状态：

```text
owner_unclear
tool_missing
evidence_incomplete
reroute_required
reopen_required
```

这样能减少“从 in_review 直接跳到 in_progress”的粗糙状态流。

---

# 八、结论

当前 HGS 继续提升自动化联动，关键不在于继续加角色，而在于：

- 增加标准动作
- 增加强制闸门
- 增加自动评分
- 增加回流与重开环规则

本总表的使命只有一个：

**让 HGS 从“有角色、有工具、有规则”升级到“会自己组织角色、调用工具、完成验证、完成收口”。**
