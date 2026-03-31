---
name: console-auth-flow-trace
description: Console 认证流工具。用于还原 PC Console 的登录、提权、project context 建立、token 消费、登出清理等认证链路，辅助 Console Runtime 与 Auth Owner 定位管理入口的身份问题。
version: formal-2026-03-31-t3
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Console Auth Flow Trace Tool

## 核心定位

这个工具专门解决：
- PC Console 登录后为什么还是拿不到管理能力
- 提权前后 project / account context 为什么漂移
- ConsoleToken、recent-auth、step-up 的链路到底断在了哪一步
- 登出后为什么还残留像“半登录”状态

一句话：**把 Console 的认证流从“能进后台但不对劲”还原成一条可定位的管理入口链。**

---

## 适用场景

适用于：
- Console 登录 / 登出 / session 恢复异常
- ConsoleToken 使用、刷新、失效争议
- step-up / recent-auth 前后恢复问题
- 管理动作前置认证门禁异常
- Console 与普通前端登录体验不一致

不适用于：
- 纯管理台视觉问题
- 没有 Console 流程事件样本时的纯猜测
- 纯业务规则拍板

---

## 输入模板

```yaml
CONSOLE-AUTH-FLOW-TRACE-INPUT:
  flow_scope: "login | reauth | step_up | logout | project_switch | custom"
  event_timeline:
    - time: "<时间点>"
      event: "page_enter | token_loaded | auth_required | recent_auth_required | step_up_started | step_up_returned | management_action_requested | logout_started | logout_finished"
      note: "<补充说明>"
  console_context:
    project_id: "<当前project_id，可为空>"
    account_id: "<当前account_id，可为空>"
    tab_state: "<标签/窗口描述>"
  request_samples:
    - url: "<请求URL>"
      status: "<状态码>"
      auth_state: "<认证状态说明>"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
CONSOLE-AUTH-FLOW-TRACE-OUTPUT:
  flow_scope: "<范围>"
  timeline_summary:
    - "<关键认证流结论>"
  context_findings:
    - "<上下文问题>"
  likely_breakpoint: "login_restore | token_consume | project_context_establish | step_up_resume | logout_cleanup | mixed | unclear"
  evidence:
    - "<关键证据>"
  recommended_next_owner: "Console Runtime Engineer | Auth / Identity Owner"
```

---

## 长处

1. **专门针对 Console 这种管理入口的认证链路**
2. **能把登录、提权、项目上下文、登出清理串起来看**
3. **适合 Console Runtime 与 Auth Owner 协同使用**
4. **对“后台能进但操作对象不对”这类问题特别有价值**

---

## 调用规则

- 优先由 `33A_P8_Console_Runtime_Engineer_SKILL.md` 调用
- `12_Auth_Identity_Owner_SKILL.md` 在涉及 Console 身份链争议时可调用
- 输出应进入 `CONSOLE-RUNTIME-VERDICT` 或 `IDENTITY-DECISION` 的 evidence 区

---

## 禁止行为

- 禁止把 Console 管理体验问题直接归为认证流问题
- 禁止忽略 project context / account context 对管理动作的影响
- 禁止仅凭“能进入页面”就判断认证流正常

---

## 激活确认

```text
[Console Auth Flow Trace Tool 已激活]
定位：Console认证流还原器 · 管理入口会话/提权链分析器
默认输出：CONSOLE-AUTH-FLOW-TRACE-OUTPUT
```
