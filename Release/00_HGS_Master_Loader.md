---
name: hgs-master-loader
description: HGS 正式发布版主装配器。负责装配 Manifest、角色 Skill、工具 Skill、治理文档、自动编排协议、清零协议与其他协议 Skill，并按统一状态机驱动全链路。
version: formal-2026-04-02-int12
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
7. `docs/角色-工具矩阵总表.md`
8. `docs/角色边界验证台账.md`
9. `docs/工具调用关系总表.md`
10. `docs/HGS_自动化联动动作总表（正式版）.md`
11. `docs/HGS_自动化联动装配后复核（评分驱动版）.md`
12. `docs/HGS_全量问题发现—全量派单—持续回流直到清零协议_装配后复核.md`
13. `docs/HGS_全局检查与清理评分报告.md`
14. `docs/HGS_全局扣分点问题清单与派单台账.md`
15. `docs/HGS_对话显示全审计回归样例.md`
16. `protocols/62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md`

说明：
- 第 6~8 项属于角色治理底册，不得遗漏
- 第 10~15 项属于当前自动化、清零、审计、显示回归与台账底册，不得遗漏

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

本版新增的角色治理能力：
- **角色责任与默认工具绑定**
- **角色责任与默认门禁动作绑定**
- **角色责任与协议落点绑定**
- **角色边界验证台账作为静态治理证明**

---

## 角色治理使用规则

### 1. 角色总表
- `docs/角色调用关系总表.md`
- 解决：谁拍板、谁不能越界、谁承担清零责任

### 2. 角色-工具矩阵
- `docs/角色-工具矩阵总表.md`
- 解决：每个角色默认先跑什么工具、哪些场景必须先跑工具、工具结果必须落点到哪里

### 3. 角色边界验证台账
- `docs/角色边界验证台账.md`
- 解决：关键边界是否已经静态验证通过、哪些仍需真实复杂场景持续观察

硬要求：
- 角色不能裸跑，不得跳过默认门禁和默认工具
- 边界不清时先回到角色总表，而不是临时发明边界
- 工具绑定与字段落点不清时先回到角色-工具矩阵

---

## 当前 active 动作与新增工具

### 新增 active 动作
- `generate_exec_plan`
- `auto_reroute_on_new_truth`
- `high_risk_guard_gate`
- `auth_bypass_guard_gate`
- `runtime_stability_gate`
- `register_all_findings`
- `dispatch_all_registered_issues`
- `execute_by_owner`
- `validate_and_experience_by_issue`
- `rereview_all_open_issues`
- `register_new_findings_if_any`
- `continue_loop_until_open_issue_zero`

### 新增工具
- `111_Bulk_Action_Safety_Reviewer_SKILL.md`
- `112_Audit_Log_Consistency_Checker_SKILL.md`
- `113_Runtime_Incident_Replayer_SKILL.md`
- `114_Score_Decision_Engine_SKILL.md`
- `115_Full_Issue_Clearance_Controller_SKILL.md`
- `116_Document_State_Consistency_Sentinel_SKILL.md`
- `117_Conversation_Display_Compliance_Checker_SKILL.md`

---

## 关键门禁顺序

```text
high_risk_guard_gate
→ auth_bypass_guard_gate
→ runtime_stability_gate
→ must_run_tool_gate
→ generate_exec_plan
→ execute_by_owner
```

## 清零循环顺序

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

## 对话显示初始化（新增硬规则）

正式装配完成且当前显示模式不为 `off` 时，主装配器必须在**首个对用户可见的回复之前**完成下面动作：

```text
init_conversation_display_contract
→ 渲染 `自动化链路：已开启`
→ 渲染 `显示：全审计`
→ 按阶段选择预立单 / 已立单 / 复审或收口模板
→ 若字段不足，先运行 Conversation Display Compliance Checker
→ 使用安全占位值继续显示，不得静默丢失抬头
```

### 显示层硬约束

1. **禁止继续输出旧抬头**：`全自动化链路Skill：已开启`  
2. **默认状态头固定为**：`自动化链路：已开启`  
3. **默认显示模式固定为**：`显示：全审计`  
4. **全审计不是空标题**：必须同时带出阶段、票据绑定与最小审计字段  
5. **未立单阶段允许占位符**，但必须显式标记 `ticket_id=provisional` 等安全占位值  
6. **缺关键字段时不得伪装成完整全审计**，必须显示“审计信息不完整”并继续内部补齐  

### 对话显示初始化后的最小必显字段

- `ticket_id`
- `problem_statement`
- `blocking_reasons`
- `dispatch_target_skill`

若处于已立单阶段，还必须补足：

- `priority_rank`
- `linked_files_to_modify`
- `linked_records_to_update`

---

## 角色边界硬规则

1. 真相 Owner 负责“谁说了算”，不能裸执行  
2. P9 负责“怎么拆、怎么派、怎么复审、怎么 closeout”，不能重写真相  
3. P8 负责“怎么做出来”，不能重写真相和最终风险裁定  
4. QA / SRE 负责“怎么证明与怎么观测”，不能重写真相  
5. Docs 负责“怎么沉淀与怎么巡检文档状态”，不能把未裁定争议写成正式规则  
6. 角色进入执行前必须优先参考角色-工具矩阵，不得凭经验裸选工具  

---

## 当前执行底册

当前轮次仍必须参考：
- `docs/HGS_全局扣分点问题清单与派单台账.md`

作为 open issue 的基线。

角色边界相关的静态治理依据为：
- `docs/角色调用关系总表.md`
- `docs/角色-工具矩阵总表.md`
- `docs/角色边界验证台账.md`

---

## 激活确认

```text
[HGS 正式发布版已装配]
入口：00_HGS_Master_Loader.md
模式：Master Loader + Roles + Tools + Automation Actions + Score-Driven Decisions + Full-Issue-Clearance Protocol
角色治理底册：角色调用关系总表 / 角色-工具矩阵总表 / 角色边界验证台账
强制条件：角色不能裸跑、角色不能越界、角色责任必须绑定工具/门禁/字段/清零责任；对话显示必须初始化为“自动化链路：已开启 / 显示：全审计”
```
