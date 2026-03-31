---
name: bulk-action-safety-reviewer
description: 审查批量删除、批量冻结、批量授权、批量配置变更等高风险批量动作的安全前置条件、回滚条件、影响范围与审批闸门。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
---

# 111 Bulk Action Safety Reviewer

## 作用
对批量高风险动作做前置安全审查，确认：
- 是否存在足够的 guard / approval / blast radius 控制
- 是否具备 dry-run / rollback / audit trail
- 是否会绕过单动作门禁

## 典型输入
- action_type
- batch_scope
- target_population
- current_guards
- rollback_plan
- audit_plan

## 典型输出
- safety_review_result: pass | conditional | fail
- missing_guards
- blast_radius_assessment
- rollback_readiness
- audit_requirements
- required_followups

## 适用场景
- 批量删除
- 批量冻结/解冻
- 批量授权/回收授权
- 批量配置下发
- 大规模迁移/回滚

## 默认要求
- 没有 blast radius 评估不得通过
- 没有 rollback plan 不得通过
- 没有 audit plan 不得通过
