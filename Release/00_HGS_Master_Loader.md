---
name: hgs-master-loader
description: HGS 正式发布版主装配器。负责装配 Manifest、角色 Skill、工具 Skill、治理文档、自动编排协议、清零协议与其他协议 Skill，并按统一状态机驱动全链路。
version: formal-2026-03-31-int8
author: OpenAI
role: MasterLoader
status: active
entrypoint: true
---

# HGS Master Loader / 主装配器

本文件的职责只有一件事：**把多角色、多工具、自动化动作、统一协议、清零治理规则正式装配成一条可自动推进、可审计、可持续回流直到清零的标准链路。**

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
9. `protocols/62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md`

---

## 装配目标

默认路线固定为：

```text
全局审查
→ 全量发现问题
→ 全量登记 issue
→ 全量派单
→ 按 owner 执行
→ 测试 / 回归 / 体验
→ 全量复审
→ 新问题继续登记并继续派单
→ 持续回流直到 open_issue_count = 0
→ Docs 沉淀
→ Closeout
```

本版新增的核心治理能力：

- **禁止只挑重点处理、剩余问题尾大不掉**
- **禁止在 open issue 尚未清零时改成让用户选 A/B 方案**
- **要求所有新发现问题全部进入 inventory 并全部派单**
- **要求每个问题在执行后进入测试 / 体验 / 复审**
- **要求只有 open issue 清零后才允许收口**

---

## 协议装配清单

当前必须装配的协议包括：

- `protocols/40_P8_Agent_Experience_Protocol.md`
- `protocols/41_P8_EndUser_Experience_Protocol.md`
- `protocols/50_RE_REVIEW_PROTOCOL.md`
- `protocols/60_HGS_IO_Protocol.md`
- `protocols/61_Automation_Orchestration_Protocol.md`
- `protocols/62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md`

其中：

- `61` 负责动作骨架、评分与自动化决策
- `62` 负责“全量发现—全量派单—持续回流直到清零”的治理硬规则

---

## 自动化动作装配清单（当前 active）

当前正式激活的动作包括四批共 24 个。统一以：

- `MANIFEST.automation_policy.active_actions`
- `docs/HGS_自动化联动动作总表（正式版）`

为准。

本 Loader 额外新增一条**全局治理循环**：

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

## 全量问题发现—全量派单—持续回流直到清零规则

### 1. 所有发现的问题必须全部登记
任何全局审查、QA、体验、复审、工具输出中新增的问题，必须全部登记进入：

- `ISSUE-LEDGER`
- 子 issue 清单
- `FULL-ISSUE-INVENTORY`

禁止只登记最重要的一部分。

### 2. 所有已登记问题必须全部派单
只要：
- owner 可以判定
- 不触发硬停机条件

就必须全部派单。

允许分批执行，但不允许分批遗忘。

### 3. 谁的问题谁处理
每个 issue 必须有：
- `issue_id`
- `owner`
- `status`
- `required_tools`
- `required_validation`
- `required_experience_if_any`

禁止长期挂成“待以后处理”且没有 owner。

### 4. 每个问题处理后必须验证
处理完成后必须进入：
- 测试 / 回归
- 必要时体验复演或真实体验
- 复审

禁止“修完就算完”。

### 5. 复审发现新问题必须继续回流
每轮复审、QA、体验、工具发现的新问题必须：
- 立即登记
- 立即归属 owner
- 立即进入下一轮派单

### 6. 只有清零才允许收口
只有同时满足：
- `open_issue_count = 0`
- `review_pending_count = 0`
- `verification_pending_count = 0`
- `experience_pending_count = 0`
- `docs_sink_pending_count = 0`

才允许进入 `done`。

---

## 全局清零循环（强制）

固定循环如下：

```text
全量发现问题
→ 全量登记
→ 全量派单
→ 逐项执行
→ 逐项验证 / 体验
→ 全量复审
→ 再发现问题继续登记
→ 继续派单
→ 继续执行
→ 直到 open_issue_count = 0
```

硬要求：

- 禁止“这轮先只修重点，剩下下次再说”作为默认策略
- 禁止“问题太多”为理由不立账、不派单
- 禁止在 open issue 未清零时让用户承担编排决策压力
- 允许多轮循环，但不允许未清零就 closeout

---

## 分数驱动与清零协议的关系

当前评分驱动规则继续生效：

### dispatch
只有：
- `owner_confidence >= 70`
- `route_stability_score >= 65`

才允许直接派单。

### review
只有：
- `tool_coverage_score >= 85`
- `evidence_completeness_score >= 80`

才允许进入 review。

### reopen
只要：
- `reopen_risk_score >= 60`
- 或 review / QA / experience / tools 发现 drift

就必须回流。

### done
只有：
- `closeout_readiness_score >= 85`
- `reopen_risk_score < 60`
- `closeout_candidate_check = pass`
- `auto_docs_sink` 已完成
- `open_issue_count = 0`

才允许进入 `done`。

---

## 新增硬规则

当前新增并正式生效的硬规则：

- `require_register_all_findings_before_review`
- `require_full_issue_inventory_before_done`
- `require_open_issue_zero_before_done`

并保留原有：
- score gates
- tool gates
- exec report / validation bundle / experience replay / docs sink / closeout gates

---

## 默认自动行为

当系统执行全局审查时，默认自动行为不是：

- 推荐先搞几个重点
- 让用户选择方案 A / 方案 B
- 把剩余问题留到以后

而是：

```text
发现多少问题
→ 登记多少问题
→ 派多少问题
→ 谁的问题谁干
→ 干完测试 / 体验 / 复审
→ 再发现再登记再派
→ 直到 open_issue_count = 0
→ 再做 docs sink 和 closeout
```

---

## 激活确认

```text
[HGS 正式发布版已装配]
入口：00_HGS_Master_Loader.md
模式：Master Loader + Roles + Tools + Automation Actions + Score-Driven Decisions + Full-Issue-Clearance Protocol
新增治理：全量问题发现—全量派单—持续回流直到清零
强制条件：所有发现必须登记、所有问题必须派单、所有问题处理后必须测试/体验/复审、open_issue_count = 0 才允许收口
```
