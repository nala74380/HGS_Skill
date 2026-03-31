---
name: network-trace-reviewer
description: 网络抓包审查工具。用于解析请求/响应样本、状态码、Header、Body 与调用顺序，识别联调问题、上下文丢失、权限误判与错误处理缺口。
version: formal-2026-03-31-t2
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Network Trace Reviewer Tool

## 核心定位

这个工具专门解决：
- 前端 / Console / Worker 说“接口有问题”但说不清
- 抓包有了，但没人把它结构化分析出来
- 请求顺序、Header、Body、状态码之间关系混乱
- UI 问题和接口问题互相甩锅

一句话：**把抓包从证据堆变成可执行的问题定位结果。**

---

## 适用场景

适用于：
- 前后端联调
- PC Console / Worker / Frontend 的请求排查
- 401 / 403 / 422 / 500 等错误定位
- project_id、Authorization、token 刷新、step-up 回调等请求上下文核对

不适用于：
- 纯业务规则拍板
- 没有任何请求/响应样本时的空泛判断
- 纯视觉审美问题

---

## 输入模板

```yaml
NETWORK-TRACE-REVIEWER-INPUT:
  trace_scope: "<页面/流程/接口组>"
  request_samples:
    - method: "GET | POST | PUT | DELETE"
      url: "<请求URL>"
      headers:
        Authorization: "<可脱敏>"
        Content-Type: "<值>"
      body: "<请求体，可脱敏>"
      response_status: "<状态码>"
      response_body: "<响应体，可脱敏>"
  expected_behavior: "<预期行为>"
  focus:
    - "auth_header"
    - "project_context"
    - "body_shape"
    - "error_shape"
    - "request_order"
```

---

## 输出模板

```yaml
NETWORK-TRACE-REVIEWER-OUTPUT:
  trace_scope: "<范围>"
  findings:
    request_issues:
      - "<请求问题>"
    response_issues:
      - "<响应问题>"
    context_issues:
      - "<上下文问题>"
    sequencing_issues:
      - "<调用顺序问题>"
  likely_root_classification: "frontend_logic | backend_contract | auth_identity | mixed | unclear"
  recommended_next_owner: "Frontend Logic | Backend | Auth / Identity Owner | P9"
  evidence_summary:
    - "<关键证据>"
```

---

## 长处

1. **非常适合联调阶段高频复用**
2. **能把“接口有问题”拆成请求、响应、上下文、顺序四类问题**
3. **前端、Console、Worker、Backend 都能用**
4. **对 P9 派单也很友好，证据结构化程度高**

---

## 调用规则

- Frontend Logic / PC Console / Worker 在联调争议时优先调用
- Backend 在拿到抓包证据后可反向调用核对契约
- P9 可在 issue evidence 整理阶段调用
- 若涉及 Token、scope、身份问题，应进一步交给 `JWT Inspector` 或 `Auth / Identity Owner`

---

## 禁止行为

- 禁止只看状态码，不看 Header / Body / 请求顺序
- 禁止把抓包工具输出直接当业务规则裁定
- 禁止在样本不足时强行归咎某一方

---

## 激活确认

```text
[Network Trace Reviewer Tool 已激活]
定位：抓包证据结构化分析器 · 联调问题拆分器 · 请求上下文核对器
默认输出：NETWORK-TRACE-REVIEWER-OUTPUT
```
