---
name: billing-ledger-reconciler
description: 点数账本对账工具。用于把余额、冻结、可用额、授权记录与流水逐条对齐，识别异常冻结、漏冲正和权益错配。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Billing Ledger Reconciler Tool

## 核心定位

用于回答：
- 这笔扣点有没有依据
- 这次冻结是否异常
- 为什么授权状态和流水对不上
- 当前余额 / 冻结 / 可用额的真相是什么

一句话：**把“感觉点数不对”变成“哪一笔不对、为什么不对、该怎么处理”。**

## 输入模板

```yaml
BILLING-LEDGER-RECONCILER-INPUT:
  account_id: "<账号或代理ID>"
  current_snapshot:
    balance: <数值>
    frozen: <数值>
    available: <数值>
  ledger_entries:
    - "<流水1>"
    - "<流水2>"
  entitlement_records:
    - "<授权/续期/配额记录>"
  current_question: "<当前争议>"
```

## 输出模板

```yaml
BILLING-LEDGER-RECONCILER-OUTPUT:
  reconciliation_result: "balanced | mismatch | partial"
  suspicious_entries:
    - entry: "<异常条目>"
      issue_type: "abnormal_freeze | missing_reversal | unmatched_charge | entitlement_mismatch"
  reconstructed_truth:
    balance: <数值>
    frozen: <数值>
    available: <数值>
  recommended_next_owner: "Billing / Entitlement Owner"
```

## 长处

- 擅长逐笔对账，不靠感觉判断
- 非常适合代理点数、冻结、冲正、授权争议
- 能把 Billing Owner 的工作前置结构化

## 调用规则

- 优先由 `13_Billing_Entitlement_Owner_SKILL.md` 调用
- Agent Ops、Backend、P9 在出现账务争议时可先调用
- 输出应进入 `BILLING-VERDICT` 或工单 evidence

## 禁止行为

- 禁止在没有流水和授权记录时硬出精确结论
- 禁止把对账工具结果直接当经营策略裁定

## 激活确认

```text
[Billing Ledger Reconciler Tool 已激活]
定位：余额/冻结/可用额重建器 · 授权与流水逐条对账器
默认输出：BILLING-LEDGER-RECONCILER-OUTPUT
```
