---
name: high-risk-action-guard-checker
description: 高风险动作门禁检查工具。用于检查删除、解绑、冻结、扣点、授权、回滚等高风险动作是否具备对象级校验、step-up、确认反馈、失败回退与审计记录。
version: formal-2026-03-31-t5
author: OpenAI
role: Tool
status: active
kind: security_tool
---

# High Risk Action Guard Checker Tool

## 核心定位

这个工具专门解决：
- 高风险动作有没有足够门禁
- 是不是只有 UI 确认，没有服务端校验
- step-up / recent-auth 是否该触发却没触发
- 动作失败后有没有安全回退与审计留痕

一句话：**把“这个按钮很危险”拆成对象校验、提权、确认、反馈、审计五道闸门。**

---

## 适用场景

适用于：
- 删除、冻结、解绑、扣点、授权、回滚、批量修改等高风险动作
- Console 管理台高风险操作
- 前端 / 后端 / 控制平面之间对门禁理解不一致
- Security / Risk 需要判断当前动作是否可接受上线

不适用于：
- 普通只读查询动作
- 纯业务规则拍板
- 没有明确高风险动作定义的空泛讨论

---

## 输入模板

```yaml
HIGH-RISK-ACTION-GUARD-CHECKER-INPUT:
  action_name: "<高风险动作名称>"
  action_scope:
    target_object: "<目标对象>"
    actor_type: "console | agent | enduser | operator | system"
  current_guards:
    object_level_authorization: "yes | no | unknown"
    step_up_or_recent_auth: "yes | no | unknown"
    explicit_confirmation: "yes | no | unknown"
    success_failure_feedback: "yes | no | unknown"
    audit_logging: "yes | no | unknown"
    rollback_or_safe_fallback: "yes | no | unknown"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
HIGH-RISK-ACTION-GUARD-CHECKER-OUTPUT:
  action_name: "<动作名称>"
  guard_result: "sufficient | partial | insufficient | dangerous"
  missing_guards:
    - "<缺失门禁>"
  weak_guards:
    - "<虽存在但不足的门禁>"
  risk_classification: "low | medium | high | critical"
  required_actions:
    - "<必须补的动作>"
  recommended_next_owner: "Security / Risk Owner | Auth / Identity Owner | Console Management Experience | Backend"
```

---

## 长处

1. **特别适合把“高风险动作”从感觉风险变成门禁清单**
2. **能同时检查服务端、提权、交互反馈和审计层**
3. **对 Security / Risk、Console UX、Backend 都非常有价值**
4. **适合作为发版前高风险动作审查闸门**

---

## 调用规则

- 优先由 `15_Security_Risk_Owner_SKILL.md` 调用
- `33B_P8_Console_Management_Experience_Engineer_SKILL.md` 在管理台高风险动作设计审查时可调用
- `31_P8_Backend_PUA_SKILL.md` 在服务端门禁检查时可引用输出
- 输出应进入 `SECURITY-RISK-VERDICT`、`P8-EXEC-REPORT` 或发布审计记录

---

## 禁止行为

- 禁止把二次确认弹窗误当成完整安全门禁
- 禁止只检查 UI，不检查服务端对象级授权
- 禁止忽略失败回退和审计留痕

---

## 激活确认

```text
[High Risk Action Guard Checker Tool 已激活]
定位：高风险动作五闸门检查器 · 安全门禁充分性审查器
默认输出：HIGH-RISK-ACTION-GUARD-CHECKER-OUTPUT
```
