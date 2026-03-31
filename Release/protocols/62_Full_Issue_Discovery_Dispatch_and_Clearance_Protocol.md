---
name: full-issue-discovery-dispatch-and-clearance-protocol
description: HGS 全量问题发现—全量派单—持续回流直到清零协议。定义全量问题登记、全量派单、执行验证体验、复审回流与清零收口的强制治理规则。
version: formal-2026-03-31-p1
author: OpenAI
role: Protocol
status: active
---

# HGS 全量问题发现—全量派单—持续回流直到清零协议

## 1. 协议目标

本协议用于把下面这件事正式写死：

```text
每次全局审查发现的所有问题
→ 必须全部登记
→ 必须全部派单
→ 谁的问题谁处理
→ 处理后必须测试 / 体验 / 复审
→ 复审再发现问题继续登记并继续派单
→ 直到 open_issue_count = 0 才允许收口
```

一句话：

**禁止只挑重点处理、剩余问题长期尾大不掉；HGS 必须持续回流直到清零。**

---

## 2. 适用范围

本协议适用于：

- 全局审查
- 批次复核
- 角色复审
- QA 回归
- 体验检查
- 安全审查
- 运行面审查
- 任何会新增问题发现的 rerreview 场景

本协议不适用于：

- 用户明确只要求做一次纯观察性评估，且不要求进入执行链
- 法律 / 安全 / 金融边界已触发停机条件，且内部解法已经穷尽

---

## 3. 强制总原则

### 原则 1：所有发现必须登记
任何审查、复审、测试、体验、工具输出新发现的问题，**必须全部登记进 `ISSUE-LEDGER` 或其子问题清单**。

禁止：
- 只登记最重要的几个
- 其余问题只口头提及不立账
- 因为问题多就只保留摘要不逐项落 issue

### 原则 2：禁止“方案 A / 方案 B”替代全量派单
在仍存在未清零问题时，默认行为不是让用户在多个方案之间选，而是：

```text
全部登记
→ 全部归属 owner
→ 全部派单
→ 持续处理
```

只有命中硬停机条件时，才允许升级问用户。

### 原则 3：谁的问题谁处理
每个问题都必须有：
- `issue_id`
- `owner`
- `status`
- `required_tools`
- `required_validation`
- `required_experience_if_any`

禁止“所有问题最后都落到一个兜底角色长期背锅不清”。

### 原则 4：处理后必须验证
问题处理完成后，必须按问题类型进入：
- 测试
- 回归
- 体验复演或真实体验
- 复审

禁止“改完就算完”。

### 原则 5：再发现问题必须继续回流
复审、QA、体验、工具再次发现问题时，必须：

```text
新增 issue
→ 归属 owner
→ 继续派单
→ 继续处理
```

禁止“这轮先不管，留到下次再说”。

### 原则 6：只有清零才允许收口
只有同时满足：
- `open_issue_count = 0`
- `review_pending_count = 0`
- `verification_pending_count = 0`
- `experience_pending_count = 0`
- `docs_sink_pending_count = 0`

才允许进入 `HGS-CLOSEOUT` / `done`。

---

## 4. 核心循环

HGS 在全局审查场景下必须遵守下面的固定循环：

```text
全量发现问题
→ 全量登记 issue
→ 按 owner 全量派单
→ 按 issue 执行
→ 逐项测试 / 回归 / 体验
→ 全量复审
→ 新发现问题继续登记
→ 再次派单
→ 直到 open_issue_count = 0
→ Docs 沉淀
→ Closeout
```

本协议要求：

**循环可以很多轮，但不能在未清零时提前收口。**

---

## 5. 必须输出的协议字段

## 5.1 `FULL-ISSUE-INVENTORY`

```yaml
FULL-ISSUE-INVENTORY:
  batch_id: "<批次ID>"
  review_cycle_no: 1
  total_found_issue_count: 0
  open_issue_count: 0
  dispatched_issue_count: 0
  in_progress_issue_count: 0
  verifying_issue_count: 0
  experience_pending_count: 0
  review_pending_count: 0
  docs_sink_pending_count: 0
  done_issue_count: 0
  blocked_issue_count: 0
  issue_list:
    - issue_id: "<问题ID>"
      title: "<问题标题>"
      owner: "<角色>"
      status: "todo | dispatched | in_progress | verifying | experience_check | reviewing | done | blocked | reopen"
      required_tools:
        - "<工具>"
      required_validation:
        - "<验证动作>"
      required_experience: "yes | no"
```

说明：
- 每轮复审后都必须更新一次
- 这是判断“是否还能 close”的主真相表之一

---

## 5.2 `CLEARANCE-CYCLE-REPORT`

```yaml
CLEARANCE-CYCLE-REPORT:
  batch_id: "<批次ID>"
  review_cycle_no: 1
  newly_found_issue_count: 0
  newly_dispatched_issue_count: 0
  newly_closed_issue_count: 0
  reopened_issue_count: 0
  remaining_open_issue_count: 0
  major_blockers:
    - "<主要阻塞>"
  next_required_action: "dispatch_remaining | continue_execution | continue_validation | continue_experience | rereview | docs_sink | closeout"
```

说明：
- 每轮循环结束都必须生成
- 用于告诉系统下一轮必须做什么，而不是让用户替系统决策

---

## 5.3 `CLEARANCE-GATE`

```yaml
CLEARANCE-GATE:
  batch_id: "<批次ID>"
  open_issue_count: 0
  review_pending_count: 0
  verification_pending_count: 0
  experience_pending_count: 0
  docs_sink_pending_count: 0
  can_closeout: "yes | no"
  closeout_blockers:
    - "<阻塞项>"
```

说明：
- 只有 `can_closeout = yes` 才允许进入 `done`

---

## 6. 派单规则

### 6.1 全量派单
每轮发现的问题只要：
- 已能识别 owner
- 不触发硬停机条件

就必须全部派单，不得只挑高优先问题执行。

### 6.2 允许分批执行，不允许分批遗忘
可以为了工程可控性：
- 分子 issue
- 分 owner
- 分执行波次

但不允许：
- 未派单问题脱离 inventory
- 未分配 owner 的问题长期滞留
- 只留“以后再看”而没有 issue 状态

### 6.3 多 owner 问题
多 owner 问题必须：
- 拆子问题
- 各自派单
- 保持 merge back rule

不得用“问题太复杂”作为不拆单、不派单的理由。

---

## 7. 测试 / 体验 / 复审规则

### 7.1 测试规则
每个完成执行的问题必须进入：
- QA 验证
- 回归清单
- 必要时工具落点检查

### 7.2 体验规则
涉及用户路径、代理路径、管理台路径的问题：
- 有真实体验反馈则用真实体验
- 无真实反馈则必须 `experience_replay`

### 7.3 复审规则
每轮完成后的问题必须送回：
- P9 复审
- 必要时 P10 / Owner 再裁定

复审发现问题时不得硬收口，必须重新进入 inventory。

---

## 8. 禁止行为

以下行为在本协议下全部禁止：

1. **只挑重点处理，其他问题不立账**
2. **把问题太多当成不派单的理由**
3. **处理完不测试、不体验、不复审**
4. **复审发现新问题却不回流**
5. **在 open issue 还大于 0 时问用户选 A/B 方案**
6. **在还有 pending review / pending validation / pending experience 时 closeout**
7. **把“下次再改”当作正式收口条件**

---

## 9. 与现有编排体系的关系

本协议与现有体系的关系是：

- `61_Automation_Orchestration_Protocol.md` 负责动作骨架
- **本协议负责清零循环治理规则**
- `MANIFEST.json` 负责把它接入正式装配链
- `00_HGS_Master_Loader.md` 负责让这条规则在运行中生效

一句话：

**61 管动作结构，62 管“问题必须一直处理到清零”为止。**

---

## 10. 默认自动行为

当系统执行全局审查时，默认自动行为应为：

```text
发现多少问题
→ 登记多少问题
→ 派多少问题
→ 谁的问题谁处理
→ 处理后测试 / 体验 / 复审
→ 再发现再登记再派
→ 直到 open_issue_count = 0
→ 再进入 Docs sink 与 Closeout
```

这条规则默认优先于：
- “先选一个方案”
- “先搞最重要的几个”
- “剩余问题以后再说”

---

## 11. 结论

本协议的使命只有一个：

**把 HGS 从“总是只处理重点、剩余问题尾大不掉”改造成“全量发现、全量派单、持续回流、直到清零再收口”的系统。**
