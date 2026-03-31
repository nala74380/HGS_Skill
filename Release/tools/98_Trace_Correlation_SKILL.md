---
name: trace-correlation
description: Trace 关联分析工具。用于关联 request_id、trace_id、span_id、worker_id、installation_id、project_id 等多源线索，重建跨前端、控制平面、执行平面与服务端的同一条运行链路。
version: formal-2026-03-31-t6
author: OpenAI
role: Tool
status: active
kind: runtime_tool
---

# Trace Correlation Tool

## 核心定位

这个工具专门解决：
- 为什么前端、后端、Worker、Console 看到的像是不同问题
- 多段 request_id / trace_id 到底是不是同一条运行链
- 一次异常到底起点在哪、传播到哪、断在了哪
- SRE 和执行层为什么总拿不到同一条完整证据链

一句话：**把分散在不同组件里的 trace 线索串成一条可复盘的运行链。**

---

## 适用场景

适用于：
- 多系统、多组件日志关联
- 前端请求、后端处理、Worker 执行、心跳事件之间的链路重建
- 一次异常跨越 Console、API、Execution Plane 的归因
- request_id / trace_id / span_id 分散，难以确认是否同源
- SRE 需要做事故时间线重建

不适用于：
- 纯业务规则争议
- 没有任何 trace / request 线索的空泛推测
- 纯 UI 体验问题

---

## 输入模板

```yaml
TRACE-CORRELATION-INPUT:
  seed_identifiers:
    trace_id: "<可为空>"
    request_id: "<可为空>"
    span_id: "<可为空>"
    worker_id: "<可为空>"
    installation_id: "<可为空>"
    project_id: "<可为空>"
  trace_fragments:
    - source: "frontend | console | backend | worker | heartbeat | other"
      identifier: "<某个关键ID>"
      time: "<时间点>"
      note: "<补充说明>"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
TRACE-CORRELATION-OUTPUT:
  correlation_result: "fully_correlated | partially_correlated | fragmented | conflicting | unclear"
  correlated_chain:
    - step: 1
      source: "<来源>"
      identifier: "<关键ID>"
      meaning: "<链路含义>"
    - step: 2
      source: "<来源>"
      identifier: "<关键ID>"
      meaning: "<链路含义>"
  broken_links:
    - "<断点>"
  likely_origin_point: "frontend | console | backend | worker | mixed | unclear"
  recommended_actions:
    - "<建议动作>"
  recommended_next_owner: "SRE / Observability Owner | Execution Plane Owner | Backend | Console Runtime"
```

---

## 长处

1. **特别适合处理“每一段日志都像说不同话”的问题**
2. **能把前端、后端、Worker、心跳、管理台线索串成一条运行链**
3. **对 SRE、Execution Plane、Backend、Console Runtime 都非常实用**
4. **是事故时间线与跨系统归因的核心工具**

---

## 调用规则

- 优先由 `38_SRE_Observability_Owner_SKILL.md` 调用
- `19_Execution_Plane_Owner_SKILL.md` 在执行链路归因时可调用
- `31_P8_Backend_PUA_SKILL.md` 与 `33A_P8_Console_Runtime_Engineer_SKILL.md` 在跨系统排查时可引用输出
- 输出应进入 `SRE-OBSERVABILITY-VERDICT`、`EXECUTION-PLANE-VERDICT` 或 `P8-EXEC-REPORT`

---

## 禁止行为

- 禁止只因为时间接近就断言多段日志同源
- 禁止忽略 identifier 冲突与链路断点
- 禁止把部分关联结果包装成完整因果链

---

## 激活确认

```text
[Trace Correlation Tool 已激活]
定位：跨系统trace线索串联器 · 事故时间线重建工具
默认输出：TRACE-CORRELATION-OUTPUT
```
