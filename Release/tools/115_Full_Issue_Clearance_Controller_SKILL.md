---
name: full-issue-clearance-controller
description: 对全量问题发现、全量派单、循环复审与清零收口做统一控制，维护 FULL-ISSUE-INVENTORY、CLEARANCE-CYCLE-REPORT 与 CLEARANCE-GATE。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
---

# 115 Full Issue Clearance Controller

## 作用
把清零循环工具化，统一管理：
- register_all_findings
- dispatch_all_registered_issues
- rereview_all_open_issues
- continue_loop_until_open_issue_zero

## 典型输入
- current_issue_inventory
- newly_found_issues
- owner_assignment_map
- execution_results
- review_results

## 典型输出
- updated_full_issue_inventory
- clearance_cycle_report
- clearance_gate
- next_required_action

## 关键规则
- open_issue_count > 0 时 can_closeout 必须为 no
- review / verification / experience / docs sink 任一 pending 时 can_closeout 必须为 no
- newly_found_issues 不能为空转丢
