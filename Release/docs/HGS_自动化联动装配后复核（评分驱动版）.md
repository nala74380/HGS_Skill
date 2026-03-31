# HGS 自动化联动装配后复核（评分驱动版）

> 版本：formal-2026-03-31-audit-score1  
> 范围：基于 `Release/MANIFEST.json`、`Release/00_HGS_Master_Loader.md`、`Release/protocols/61_Automation_Orchestration_Protocol.md`、`Release/docs/HGS_自动化联动动作总表（正式版）.md` 做评分驱动版装配后复核。  
> 说明：本复核评估的是**评分驱动自动化联动的静态装配完整度、规则一致性与治理同频度**，不是生产环境真实性能压测报告。

---

# 一、复核结论摘要

## 核心结论
当前 HGS 已经从：

```text
有角色 + 有工具 + 有动作 + 有闸门
```

升级到：

```text
有角色 + 有工具 + 有动作 + 有闸门 + 有评分驱动决策
```

也就是现在系统已经具备：
- 根据 `owner_confidence` 与 `route_stability_score` 决定是否可直接派单
- 根据 `tool_coverage_score` 与 `evidence_completeness_score` 决定是否可进入 review
- 根据 `reopen_risk_score` 决定是否自动 reopen
- 根据 `closeout_readiness_score` 与 `reopen_risk_score` 决定是否可进入 done

---

# 二、复核对象与同频情况

## 1. `Release/MANIFEST.json`
### 复核结果
**已进入评分驱动版口径。**

### 已确认项
- `package_version = formal-2026-03-31-int7`
- `automation_policy.active_actions` 已包含 24 个动作
- 已纳入 6 个评分动作：
  - `compute_owner_confidence`
  - `compute_tool_coverage_score`
  - `compute_evidence_completeness_score`
  - `compute_route_stability_score`
  - `compute_closeout_readiness_score`
  - `compute_reopen_risk_score`
- 已写入 `score_decision_rules`
- 已写入分数阈值：
  - `owner_confidence >= 70`
  - `route_stability >= 65`
  - `tool_coverage >= 85`
  - `evidence_completeness >= 80`
  - `closeout_readiness >= 85`
  - `reopen_risk_high = 60`

### 结论
`MANIFEST` 已成为评分驱动决策的正式单点来源。

---

## 2. `Release/00_HGS_Master_Loader.md`
### 复核结果
**已进入评分驱动版口径。**

### 已确认项
- Loader 已把自动化动作清单扩到四批 active
- 已明确评分驱动序列：
  - 入口：`compute_owner_confidence`、`compute_route_stability_score`
  - review 前：`compute_tool_coverage_score`、`compute_evidence_completeness_score`
  - close 前：`compute_reopen_risk_score`、`compute_closeout_readiness_score`
- 已明确：
  - 低置信不 dispatch
  - 覆盖/证据不足不 review
  - reopen 风险高自动 reopen
  - readiness 不足不 done

### 结论
Loader 已从“动作编排器”升级成“评分驱动编排器”。

---

## 3. `Release/protocols/61_Automation_Orchestration_Protocol.md`
### 复核结果
**已进入评分驱动版口径。**

### 已确认项
- 协议版本已到 `formal-2026-03-31-p4`
- 已补齐 6 个评分动作的最小输入输出骨架
- 已补齐 `SCORE-DECISION-RULES`
- 已补齐 `AUTOMATION-HARD-GATES` 的评分闸门映射

### 结论
协议层已经具备“分数可记录、可传递、可驱动决策”的结构基础。

---

## 4. `Release/docs/HGS_自动化联动动作总表（正式版）.md`
### 复核结果
**当前主不同步点之一。**

### 发现的问题
- 版本仍停在 `formal-2026-03-31-r1`
- 虽然已列出评分层动作，但仍停留在“建议接入 / 分批接入”的表达
- 未反映：四批动作已经全部进入 active chain
- 未显式写出 `dispatch / review / reopen / done` 的分数驱动规则

### 结论
动作总表需要升版，改成“评分驱动已接入”的口径。

---

## 5. `Release/docs/HGS_全局检查与清理评分报告.md`
### 复核结果
**当前主不同步点之二。**

### 发现的问题
- 当前仍为 `audit3`
- 仍停留在“运行面版复核”结论
- 未反映自动化动作四批 active
- 未反映评分驱动 dispatch/review/reopen/done 已进入 active chain

### 结论
评分报告需要升版，改成“评分驱动版复核”口径。

---

# 三、评分驱动规则一致性检查

## 1. 派单规则一致性
### 检查结果
**一致。**

### 当前规则
- `owner_confidence >= 70`
- `route_stability_score >= 65`
- 否则：`route_dry_run` 或 `p9_reframe_and_redispatch`

### 结论
评分驱动 dispatch 规则已在 `MANIFEST / Loader / Protocol` 三处同频。

---

## 2. Review 规则一致性
### 检查结果
**一致。**

### 当前规则
- `tool_coverage_score >= 85`
- `evidence_completeness_score >= 80`
- 且 exec report / validation bundle 必须存在

### 结论
评分驱动 review 规则已在三处同频。

---

## 3. Reopen 规则一致性
### 检查结果
**一致。**

### 当前规则
- `reopen_risk_score >= 60`
- 自动执行 `auto_reopen_on_drift`

### 结论
评分驱动 reopen 规则已在三处同频。

---

## 4. Done 规则一致性
### 检查结果
**一致。**

### 当前规则
- `closeout_readiness_score >= 85`
- `reopen_risk_score < 60`
- `closeout_candidate_check = pass`
- `auto_docs_sink` 已完成

### 结论
评分驱动 done 规则已在三处同频。

---

# 四、当前能力边界

## 已具备的能力
1. 低置信 owner 不直接派单
2. route 不稳先 dry-run，不盲派
3. 工具覆盖率不足不进入 review
4. 证据完整度不足不进入 review
5. reopen 风险高自动 reopen
6. closeout readiness 不足不进入 done
7. 没有 docs sink 不允许 done

## 仍未具备的能力
1. 真实运行时的自动分数计算器尚未工具化为独立 Tool Skill
2. 评分结果仍主要依赖协议/动作结构，而非独立评分引擎
3. “全量问题发现后自动派单直到 open issue 清零”的治理循环还未单独固化为正式动作

---

# 五、评分驱动版总评分

| 维度 | 评分 | 结论 |
|---|---:|---|
| 动作装配完整度 | **9.7 / 10** | 四批动作已进入 active chain，骨架完整 |
| 评分决策一致性 | **9.8 / 10** | dispatch / review / reopen / done 规则在三处同频 |
| 自动化闭环程度 | **9.5 / 10** | 已覆盖入口、协商、执行、验证、体验、回流、收口 |
| 文档治理同频度 | **8.8 / 10** | 关键入口已同频，但动作总表与评分报告仍落后 |
| 综合评分 | **9.5 / 10** | 已具备正式评分驱动编排能力，但治理文档仍需同步升版 |

---

# 六、本轮复核后的直接动作

本轮复核后，建议立即执行且无需再做 A/B 选择的动作只有两项：

1. 升级 `Release/docs/HGS_自动化联动动作总表（正式版）.md`
2. 升级 `Release/docs/HGS_全局检查与清理评分报告.md`

这是把评分驱动版从“装配链已完成”推进到“治理文档也完全同频”的最后两步。

---

# 七、结论

本轮《自动化联动装配后复核（评分驱动版）》的核心结论是：

**HGS 现在已经不只是“有自动化动作”，而是“自动化动作开始由分数驱动真实编排决策”；当前剩余的主要问题不是装配链本身，而是治理文档口径还需要同步到评分驱动版。**
