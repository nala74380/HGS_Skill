---
name: heartbeat-gap-analyzer
description: 心跳缺口分析工具。用于分析 Worker 或执行节点心跳的间隔、缺口、恢复与抖动模式，识别在线状态误判、弱网抖动、更新切换与运行面状态不一致问题。
version: formal-2026-03-31-t6
author: OpenAI
role: Tool
status: active
kind: runtime_tool
---

# Heartbeat Gap Analyzer Tool

## 核心定位

这个工具专门解决：
- 为什么系统显示离线，但节点之后又恢复了
- 心跳到底是短暂抖动、长缺口，还是更新切换期间的状态波动
- 执行平面为什么判断节点不稳定
- Console、Execution Plane、SRE 对在线状态为什么说法不一致

一句话：**把“在线状态不对劲”拆成心跳间隔、缺口长度、恢复模式与抖动类型。**

---

## 适用场景

适用于：
- Worker 在线/离线状态争议
- 心跳断续、短时间频繁抖动
- 更新切换后的心跳异常
- 弱网、重试风暴后的心跳异常
- SRE 需要判断告警是噪音还是真缺口

不适用于：
- 纯身份真相争议
- 纯账务问题
- 没有心跳样本时的空泛推测

---

## 输入模板

```yaml
HEARTBEAT-GAP-ANALYZER-INPUT:
  subject_scope:
    installation_id: "<可为空>"
    worker_id: "<可为空>"
    project_id: "<可为空>"
  expected_interval_sec: <预期心跳间隔秒数>
  heartbeat_events:
    - time: "<时间点>"
      status: "received | missing | resumed | ignored"
      latency_ms: <可为空>
      note: "<补充说明>"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
HEARTBEAT-GAP-ANALYZER-OUTPUT:
  heartbeat_result: "stable | jittery | intermittent_gap | prolonged_gap | transition_state | unclear"
  gap_findings:
    interval_deviation:
      - "<间隔偏差>"
    gap_windows:
      - "<缺口区间>"
    recovery_patterns:
      - "<恢复模式>"
  likely_root_cause: "weak_network | process_restart | update_transition | runtime_pressure | mixed | unclear"
  recommended_actions:
    - "<建议动作>"
  recommended_next_owner: "Execution Plane Owner | SRE / Observability Owner | P8 LanrenJingling"
```

---

## 长处

1. **特别适合把“看起来离线”拆成可量化的缺口模式**
2. **能区分抖动、短缺口、长缺口与切换期波动**
3. **对 Execution Plane、SRE、LanrenJingling 都非常高频**
4. **是运行态告警降噪和异常归因的重要工具**

---

## 调用规则

- 优先由 `19_Execution_Plane_Owner_SKILL.md` 调用
- `38_SRE_Observability_Owner_SKILL.md` 在心跳异常与告警归因时可调用
- `34_P8_LanrenJingling_PUA_SKILL.md` 在执行端稳定性排查时可引用输出
- 输出应进入 `EXECUTION-PLANE-VERDICT`、`SRE-OBSERVABILITY-VERDICT` 或 `P8-EXEC-REPORT`

---

## 禁止行为

- 禁止只看一个 missing event 就断言节点离线
- 禁止把所有心跳异常都归结为弱网
- 禁止忽略更新切换与运行压力对心跳的影响

---

## 激活确认

```text
[Heartbeat Gap Analyzer Tool 已激活]
定位：心跳缺口与恢复模式分析器 · 在线状态争议归因工具
默认输出：HEARTBEAT-GAP-ANALYZER-OUTPUT
```
