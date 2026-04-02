---
name: conversation-display-compliance-checker
description: 对话显示合规检查工具。用于检查“自动化链路：已开启 / 显示：全审计”抬头、阶段标签、票据绑定与最小审计字段是否已正确渲染，防止对话显示层漂移、缺栏位或错误沿用旧抬头。
version: formal-2026-04-02-t1
author: OpenAI
role: Tool
status: active
kind: governance_tool
---

# Conversation Display Compliance Checker Tool

## 核心定位

这个工具专门解决：

- 为什么已经装配了自动化链路，但对话里没有显示 `自动化链路：已开启`
- 为什么已经切到 `显示：全审计`，却只有标题没有审计字段
- 为什么还在输出旧抬头 `全自动化链路Skill：已开启`
- 为什么未立单阶段、已立单阶段、复审阶段使用了错误模板
- 为什么字段缺失时把“部分审计”伪装成“完整全审计”

一句话：**把对话显示层从“看起来像开启了”变成“显示契约真的被执行了”。**

---

## 适用场景

适用于：

- 会话装配完成后的首条用户可见回复
- `display_mode=forensic` 的任意阶段回复
- 预立单 / 已立单 / 复审 / closeout 阶段的显示完整性检查
- 旧抬头清理、字段缺栏位审计、显示模板选择错误审计

不适用于：

- 真相拍板
- 执行层改代码
- 业务规则本身的对错裁定

---

## 输入模板

```yaml
CONVERSATION-DISPLAY-CHECKER-INPUT:
  activation_state: "active | inactive"
  display_mode: "off | compact | standard | forensic"
  rendered_headers:
    - "自动化链路：已开启"
    - "显示：全审计"
  current_stage: "pre_ticket | ticketed | reviewing | closeout"
  rendered_payload:
    ticket_id: "<当前显示值>"
    priority_rank: "<当前显示值>"
    problem_statement: "<当前显示值>"
    blocking_reasons:
      - "<当前显示值>"
    linked_files_to_modify:
      - "<当前显示值>"
    linked_records_to_update:
      - "<当前显示值>"
    dispatch_target_skill: "<当前显示值>"
  legacy_headers_seen:
    - "全自动化链路Skill：已开启"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
CONVERSATION-DISPLAY-CHECKER-OUTPUT:
  compliance_result: "pass | partial | fail | legacy_header_detected"
  header_check:
    status_header: "pass | missing | wrong"
    display_mode_header: "pass | missing | wrong"
    legacy_header: "clean | detected"
  stage_template_check:
    expected_template: "pre_ticket | ticketed | reviewing | closeout"
    rendered_template_fit: "pass | drift"
  missing_fields:
    - "<缺失字段>"
  weak_fields:
    - field: "<字段名>"
      issue: "placeholder_missing | empty | vague | wrong_phase"
  corrective_actions:
    - "<替换旧抬头 / 补安全占位值 / 改用已立单模板>"
  can_claim_forensic_complete: true
```

---

## 默认检查规则

### 规则 1：抬头硬约束

- 激活后必须显示：`自动化链路：已开启`
- `display_mode=forensic` 时必须显示：`显示：全审计`
- 检测到 `全自动化链路Skill：已开启` 直接判定为 `legacy_header_detected`

### 规则 2：阶段模板检查

- `pre_ticket`：允许 `ticket_id=provisional`
- `ticketed`：必须有 `priority_rank`
- `reviewing` / `closeout`：必须有当前阶段对应的票据绑定与审计字段

### 规则 3：关键字段缺失不得伪装完整

以下任一缺失时，`can_claim_forensic_complete=false`：

- `ticket_id`
- `problem_statement`
- `dispatch_target_skill`

### 规则 4：允许安全占位，不允许静默留空

允许：
- `ticket_id=provisional`
- `linked_files_to_modify=[pending_after_owner_inference]`
- `linked_records_to_update=[pending_after_issue_registration]`

禁止：
- 留空
- 省略字段
- 用旧抬头掩盖缺字段

---

## 调用规则

- 优先由 `00_HGS_Master_Loader.md` 在首条用户可见回复前调用
- `20_P9_Principal_SKILL.md` 在重派单、复审阶段可调用
- `39_Knowledge_Documentation_Owner_SKILL.md` 在显示规范沉淀前可调用

---

## 禁止行为

- 禁止检测到旧抬头仍继续原样输出
- 禁止字段缺失时仍声称“全审计”
- 禁止把模板漂移解释成“用户没要求显示”

---

## 激活确认

```text
[Conversation Display Compliance Checker Tool 已激活]
定位：对话显示硬约束检查器 · 全审计字段合规检查器 · 旧抬头清理闸门
默认输出：CONVERSATION-DISPLAY-CHECKER-OUTPUT
```
