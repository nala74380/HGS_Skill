---
name: session-refresh-trace
description: 会话刷新链路工具。用于还原 access token / refresh token / recent-auth 的刷新顺序、并发竞争、失效时机与恢复结果，辅助 Auth / Console / Frontend 角色定位会话异常。
version: formal-2026-03-31-t3
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Session Refresh Trace Tool

## 核心定位

这个工具专门解决：
- 为什么明明刚登录过，还是突然失效
- refresh token 到底有没有按预期刷新
- 多标签 / 多页面 / 多请求并发时，会话刷新是不是打架了
- recent-auth / step-up 之后，会话恢复是不是断了

一句话：**把“会话怎么又掉了”拆成刷新顺序、并发竞争、失效时机与恢复结果。**

---

## 适用场景

适用于：
- access token 过期后自动刷新异常
- refresh token 串行化 / 并发刷新冲突
- recent-auth / step-up 触发后返回路径与会话恢复异常
- 登录后短时间内反复 401 / 403 / forced re-auth
- Console / Frontend 多标签、重开页、切项目后的会话不一致

不适用于：
- 纯业务规则争议
- 纯 UI 表面问题
- 完全没有会话样本或刷新事件时的空泛猜测

---

## 输入模板

```yaml
SESSION-REFRESH-TRACE-INPUT:
  actor: "console | frontend | enduser | agent"
  token_timeline:
    - time: "<时间点>"
      event: "login | token_issued | token_expired | refresh_started | refresh_succeeded | refresh_failed | recent_auth_required | step_up_required | logout"
      note: "<补充说明>"
  request_samples:
    - url: "<请求URL>"
      status: "<状态码>"
      auth_state: "<携带token/未携带/已过期/未知>"
  current_question: "<当前争议>"
  context:
    tabs: <数量或描述>
    route: "<当前路由/页面>"
```

---

## 输出模板

```yaml
SESSION-REFRESH-TRACE-OUTPUT:
  timeline_summary:
    - "<关键时间线结论>"
  concurrency_findings:
    - "<并发/串行问题>"
  likely_failure_point: "token_expiry | refresh_race | stale_session | recent_auth_resume | mixed | unclear"
  evidence:
    - "<关键证据>"
  recommended_next_owner: "Auth / Identity Owner | Frontend Logic | Console Runtime"
```

---

## 长处

1. **特别擅长把“掉登录态”从抱怨变成时间线**
2. **能把 refresh race 和普通过期区分开**
3. **对 Auth / Frontend / Console Runtime 三方都高频复用**
4. **很适合在 P9 复审前提供结构化证据**

---

## 调用规则

- 优先由 `12_Auth_Identity_Owner_SKILL.md` 调用
- `32B_P8_Frontend_Logic_Engineer_SKILL.md` 与 `33A_P8_Console_Runtime_Engineer_SKILL.md` 在会话问题时可前置调用
- 输出必须进入 `IDENTITY-DECISION`、`FRONTEND-LOGIC-VERDICT` 或 `CONSOLE-RUNTIME-VERDICT` 的 evidence 区

---

## 禁止行为

- 禁止只看单个 401 就断言 refresh 失效
- 禁止忽略多标签 / 并发请求对刷新链路的影响
- 禁止把业务强制重新认证误判为技术性会话掉线

---

## 激活确认

```text
[Session Refresh Trace Tool 已激活]
定位：会话刷新时间线还原器 · refresh竞争分析器 · recent-auth恢复辅助器
默认输出：SESSION-REFRESH-TRACE-OUTPUT
```
