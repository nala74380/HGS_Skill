---
name: stepup-resume-checker
description: Step-up 恢复检查工具。用于检查 recent-auth / step-up 前后是否正确保存上下文、返回原动作、恢复目标对象并在失败后安全回退。
version: formal-2026-03-31-t3
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Step-up Resume Checker Tool

## 核心定位

这个工具专门解决：
- step-up / recent-auth 后为什么没有回到原动作
- 提权回来后为什么对象错了、状态丢了、操作重复了
- 提权失败后为什么页面停在半残状态
- 管理动作前的二次认证链有没有正确闭环

一句话：**把“提权回来后不对劲”拆成保存、返回、恢复、回退四段检查。**

---

## 适用场景

适用于：
- Console 管理动作前 step-up / recent-auth
- Frontend 关键操作前二次确认认证
- 提权完成后需要继续执行原动作的链路
- 提权失败、取消、超时后的安全回退检查

不适用于：
- 纯 token 过期问题
- 没有提权链存在的普通登录问题
- 纯 UI 布局问题

---

## 输入模板

```yaml
STEPUP-RESUME-CHECKER-INPUT:
  trigger_action: "<触发提权的原动作>"
  pre_stepup_context:
    route: "<提权前页面/路由>"
    project_id: "<提权前project_id，可为空>"
    account_id: "<提权前account_id，可为空>"
    target_object: "<提权前目标对象，可为空>"
  stepup_events:
    - "step_up_started"
    - "step_up_completed | step_up_failed | step_up_cancelled"
  post_stepup_context:
    route: "<提权后页面/路由>"
    project_id: "<提权后project_id，可为空>"
    account_id: "<提权后account_id，可为空>"
    target_object: "<提权后目标对象，可为空>"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
STEPUP-RESUME-CHECKER-OUTPUT:
  resume_result: "correct_resume | lost_context | wrong_target_resume | duplicate_action_risk | unsafe_fallback | unclear"
  findings:
    saved_context_status:
      - "<提权前保存情况>"
    return_path_status:
      - "<返回路径问题>"
    restore_status:
      - "<恢复问题>"
    fallback_status:
      - "<失败/取消后的回退问题>"
  recommended_next_owner: "Console Runtime | Frontend Logic | Auth / Identity Owner"
  evidence:
    - "<关键证据>"
```

---

## 长处

1. **特别适合检查高风险动作前的二次认证恢复链**
2. **能把“提权回来不对”拆成明确四段：保存、返回、恢复、回退**
3. **对 Console Runtime、Frontend Logic、Auth 三方都非常实用**
4. **很适合高风险管理动作与用户关键操作的复审**

---

## 调用规则

- 优先由 `33A_P8_Console_Runtime_Engineer_SKILL.md` 调用
- `32B_P8_Frontend_Logic_Engineer_SKILL.md` 在前端关键操作提权场景可调用
- `12_Auth_Identity_Owner_SKILL.md` 在判定 recent-auth / step-up 真相时可协同使用
- 输出应进入 `CONSOLE-RUNTIME-VERDICT`、`FRONTEND-LOGIC-VERDICT` 或 `IDENTITY-DECISION` 的 evidence 区

---

## 禁止行为

- 禁止只验证“提权成功”而不验证“是否回到原动作”
- 禁止忽略失败 / 取消 / 超时后的回退安全性
- 禁止把对象漂移误判成普通会话问题

---

## 激活确认

```text
[Step-up Resume Checker Tool 已激活]
定位：提权恢复链检查器 · 原动作返回与安全回退验证器
默认输出：STEPUP-RESUME-CHECKER-OUTPUT
```
