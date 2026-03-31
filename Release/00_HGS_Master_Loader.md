---
name: hgs-master-loader
description: HGS 正式发布版主装配器。负责装配 Manifest、角色 Skill、工具 Skill、治理文档、自动编排协议与其他协议 Skill，并按统一状态机驱动全链路。
version: formal-2026-03-31-int7
author: OpenAI
role: MasterLoader
status: active
entrypoint: true
---

# HGS Master Loader / 主装配器

本文件不是“替代所有角色”的超级单体 Skill。  
本文件的职责只有一件事：**把多角色、多工具、自动化动作、统一协议、治理文档正式装配成一条可自动推进、可审计、可重开环的标准链路。**

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

---

## 装配目标

默认路线固定为：

```text
P10 战略初判（仅必要时）
  ↓
真相 Owner 识别
  ↓
P9 审查与派单
  ↓
P8 按 owner 执行
  ↓
体验验证（代理 / 终端用户 / 路径复演）
  ↓
QA / SRE / 体验证据收口
  ↓
P9 复审
  ↓
Knowledge / Docs 沉淀
  ↓
收口 / 再开环
```

本版新增的核心能力：

- 自动化动作驱动入口标准化、内部协商、执行、验证、体验、回流、收口
- **自动化评分驱动派单、review、reopen 与 done 决策**

---

## 自动化动作装配清单（全 active）

当前正式激活的动作包括：

### 第一批
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

### 第二批
11. `owner_self_resolve_attempt`
12. `fallback_to_p8_enhanced`
13. `p9_reframe_and_redispatch`
14. `autofill_exec_report`
15. `generate_validation_bundle`

### 第三批
16. `experience_replay`
17. `auto_reopen_on_drift`
18. `auto_docs_sink`

### 第四批（评分驱动）
19. `compute_owner_confidence`
20. `compute_tool_coverage_score`
21. `compute_evidence_completeness_score`
22. `compute_route_stability_score`
23. `compute_closeout_readiness_score`
24. `compute_reopen_risk_score`

---

## 自动化动作执行顺序（当前 active）

### 入口标准化与评分路由序列
```text
create_issue_stub
→ infer_owner_candidates
→ compute_owner_confidence
→ infer_required_tools
→ compute_route_stability_score
→ route_dry_run（当 owner_confidence < 70 或 route_stability < 65）
→ provisional_boundary_build（当边界暂不精确）
```

### 内部协商与重派单序列
```text
owner_self_resolve_attempt
→ peer_role_consult
→ split_subissues
→ fallback_to_p8_enhanced
→ p9_reframe_and_redispatch
```

### 工具闸门与 review 评分序列
```text
must_run_tool_gate
→ autofill_exec_report
→ generate_validation_bundle
→ compute_tool_coverage_score
→ compute_evidence_completeness_score
→ tool_result_landing_check
→ 若 tool_coverage < 85 或 evidence_completeness < 80，则不得进入 review
```

### 体验 / 回流 / 收口评分序列
```text
experience_replay（当真实反馈缺失）
→ compute_reopen_risk_score
→ auto_reopen_on_drift（当 reopen_risk >= 60 或 review/QA/experience/tools 发现漂移）
→ auto_docs_sink（当复审通过且具备复用价值）
→ compute_closeout_readiness_score
→ closeout_candidate_check
→ 若 closeout_readiness >= 85 且 reopen_risk < 60，则进入 done
```

---

## 分数驱动决策规则（正式版）

### 1. 派单决策
只有同时满足：
- `owner_confidence >= 70`
- `route_stability_score >= 65`

才允许直接 dispatch。否则：
- 先 `route_dry_run`
- 必要时 `p9_reframe_and_redispatch`

### 2. Review 决策
只有同时满足：
- `tool_coverage_score >= 85`
- `evidence_completeness_score >= 80`
- `P8-EXEC-REPORT` 已存在
- `validation bundle` 已存在

才允许进入 review。否则：
- `tool_missing` 或 `evidence_incomplete`
- 继续补 exec / validation / protocol landing

### 3. Reopen 决策
只要满足任一：
- `reopen_risk_score >= 60`
- QA / review / experience / tools 发现 drift

则自动执行：
- `auto_reopen_on_drift`
- 必要时 `p9_reframe_and_redispatch`

### 4. Done 决策
只有同时满足：
- `closeout_readiness_score >= 85`
- `reopen_risk_score < 60`
- `closeout_candidate_check = pass`
- `auto_docs_sink` 已完成

才允许进入 `done`。

---

## 硬规则

- 未创建 `ISSUE-LEDGER stub` 不得派单
- 未通过分数闸门不得派单
- 未通过 tool/evidence 闸门不得 review
- `reopen_risk >= 60` 时不得 close
- 未完成 docs sink 不得 done
- 未通过 closeout 候选检查不得 done

---

## 激活确认

```text
[HGS 正式发布版已装配]
入口：00_HGS_Master_Loader.md
模式：Master Loader + Roles + Tools + Automation Actions + Score-Driven Decisions + Governance Docs + Manifest
加载策略：Manifest 驱动，全角色 + 全工具 + 四批自动化动作装配
分数驱动：owner_confidence / route_stability / tool_coverage / evidence_completeness / reopen_risk / closeout_readiness
自动决策：会根据分数自动决定是否派单、是否 review、是否 reopen、是否 close
```
