---
name: runtime-incident-replayer
description: 基于 trace、heartbeat、runtime event 与 worker identity 证据重建运行事故时间线，辅助执行平面与 SRE 做 incident replay。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
---

# 113 Runtime Incident Replayer

## 作用
重建运行事故时间线，识别：
- 事件发生顺序
- 链路断点
- 关键缺口窗口
- 恢复前后的状态差异

## 典型输入
- trace_events
- heartbeat_events
- worker_identity_records
- deployment_or_config_events

## 典型输出
- replay_timeline
- suspected_breakpoints
- confidence_assessment
- evidence_gaps
- followup_checks

## 适用场景
- 在线/离线抖动
- worker 漂移
- 事故复盘
- 运行面 closeout 前复审
