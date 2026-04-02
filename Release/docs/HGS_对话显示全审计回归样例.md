# HGS 对话显示全审计回归样例

> 版本：formal-2026-04-02-r1  
> 定位：用于验证“自动化链路：已开启 / 显示：全审计”在对话中是否默认稳定渲染，并检查预立单、已立单、复审、收口四类阶段模板是否符合显示契约。

---

## 一、回归目标

本样例只验证一件事：

**只要 HGS 在对话中完成装配并进入可见回复阶段，默认必须显示：**

- `自动化链路：已开启`
- `显示：全审计`

且在 `forensic` 模式下，必须附带对应阶段的最小审计字段。

---

## 二、统一验收规则

### 1. 抬头规则
- 必须显示 `自动化链路：已开启`
- 必须显示 `显示：全审计`
- 禁止显示 `全自动化链路Skill：已开启`

### 2. 最小字段规则
#### pre_ticket
- `ticket_id`
- `problem_statement`
- `blocking_reasons`
- `dispatch_target_skill`

#### ticketed
- `ticket_id`
- `priority_rank`
- `problem_statement`
- `blocking_reasons`
- `linked_files_to_modify`
- `linked_records_to_update`
- `dispatch_target_skill`

### 3. 缺字段规则
- 允许显示安全占位值
- 不允许静默丢字段
- 关键字段缺失时必须标记“审计信息不完整”

---

## 三、样例 1：新对话首次装配（预立单阶段）

### 输入条件
- Skill 已完成装配
- 尚未生成正式 issue
- `display_mode=forensic`

### 期望输出骨架

```text
自动化链路：已开启
显示：全审计
阶段：pre_ticket
ticket_id: provisional
problem_statement: <当前问题摘要>
blocking_reasons:
  - <若无则显示 none 或 pending>
dispatch_target_skill: pending_owner_inference
```

### 通过条件
- 两行抬头齐全
- `ticket_id=provisional`
- 未使用旧抬头
- 未立单阶段字段没有静默缺失

---

## 四、样例 2：已立单并派单执行中

### 输入条件
- 已存在 issue
- owner 已识别
- `display_mode=forensic`

### 期望输出骨架

```text
自动化链路：已开启
显示：全审计
阶段：in_progress
ticket_id: ISSUE-001
priority_rank: P1
problem_statement: <问题描述>
blocking_reasons:
  - none
linked_files_to_modify:
  - <文件A>
linked_records_to_update:
  - <记录A>
dispatch_target_skill: P8前端工程师
```

### 通过条件
- 两行抬头齐全
- `priority_rank` 已显示
- 文件 / 记录 / 派单目标已显示
- 无旧抬头

---

## 五、样例 3：复审阶段

### 输入条件
- P8 已回包
- P9 进入复审
- `display_mode=forensic`

### 期望输出骨架

```text
自动化链路：已开启
显示：全审计
阶段：reviewing
ticket_id: ISSUE-001
problem_statement: <问题描述>
blocking_reasons:
  - none
dispatch_target_skill: P9派单官
```

### 通过条件
- 两行抬头齐全
- 阶段已变为 `reviewing`
- 票据绑定仍然存在
- 无旧抬头

---

## 六、样例 4：closeout 前

### 输入条件
- issue 已复审通过
- docs sink 已完成或即将完成
- `display_mode=forensic`

### 期望输出骨架

```text
自动化链路：已开启
显示：全审计
阶段：closeout
ticket_id: ISSUE-001
problem_statement: <问题描述>
blocking_reasons:
  - none
dispatch_target_skill: 文档负责人
```

### 通过条件
- 两行抬头齐全
- 阶段为 `closeout`
- 票据未丢
- 无旧抬头

---

## 七、失败判定

出现任一情况，判定回归失败：

1. 缺少 `自动化链路：已开启`
2. 缺少 `显示：全审计`
3. 出现 `全自动化链路Skill：已开启`
4. `forensic` 模式下没有最小字段
5. 把缺关键字段的回复包装成完整全审计

---

## 八、结论

本样例的使命只有一个：

**确保 HGS 在对话中一旦装配生效，就把“自动化链路：已开启 / 显示：全审计”稳定、统一、无旧抬头漂移地渲染出来。**
