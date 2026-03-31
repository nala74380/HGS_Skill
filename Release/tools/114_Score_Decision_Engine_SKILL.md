---
name: score-decision-engine
description: 对 owner confidence、route stability、tool coverage、evidence completeness、reopen risk、closeout readiness 做统一评分，并输出 dispatch/review/reopen/done 建议。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
---

# 114 Score Decision Engine

## 作用
将评分动作工具化，统一计算并输出：
- owner_confidence
- route_stability_score
- tool_coverage_score
- evidence_completeness_score
- reopen_risk_score
- closeout_readiness_score

## 典型输入
- issue_profile
- owner_candidates
- must_run_tools
- executed_tools
- protocol_payloads
- review_findings
- validation_results
- experience_results

## 典型输出
- score_snapshot
- dispatch_decision
- review_decision
- reopen_decision
- done_decision
- blocking_reasons

## 默认阈值
- owner_confidence >= 70
- route_stability >= 65
- tool_coverage >= 85
- evidence_completeness >= 80
- reopen_risk < 60
- closeout_readiness >= 85
