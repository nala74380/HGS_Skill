---
name: audit-log-consistency-checker
description: 检查动作执行记录、协议字段、操作日志与审计日志之间的一致性，识别“动作已发生但审计不完整/不一致”的问题。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
---

# 112 Audit Log Consistency Checker

## 作用
校验执行事实与审计事实是否一致，重点发现：
- action happened but audit missing
- audit exists but protocol landing missing
- object / actor / timestamp / scope mismatch

## 典型输入
- executed_actions
- audit_logs
- protocol_payloads
- actor_identifiers
- object_identifiers

## 典型输出
- consistency_result: pass | conditional | fail
- missing_audit_events
- mismatched_fields
- orphan_audit_records
- remediation_steps

## 适用场景
- 管理台操作
- 高风险动作
- 权限与账务动作
- 清零循环中的 closeout 前复核
