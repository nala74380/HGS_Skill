---
name: authorization-bypass-path-reviewer
description: 授权绕过路径审查工具。用于审查对象级授权、前后端权限表达、隐式上下文、调试口子与接口组合是否形成可绕过路径，辅助 Security / Risk、Auth、Backend 做越权风险识别。
version: formal-2026-03-31-t5
author: OpenAI
role: Tool
status: active
kind: security_tool
---

# Authorization Bypass Path Reviewer Tool

## 核心定位

这个工具专门解决：
- 这个接口是不是只靠前端显隐拦住了用户
- 有没有通过换参数、改 project_id、直调接口就能绕过去的路径
- 对象级授权是不是缺失了
- 调试口子、组合接口、隐式上下文是不是形成了越权面

一句话：**把“可能被绕过”拆成真实的授权绕过路径审查。**

---

## 适用场景

适用于：
- Console / 管理台高权限操作
- project/account/object 级别资源访问控制
- 前端显隐与后端授权不一致
- 通过改参数、跨对象、跨 project 访问的疑似越权问题
- Security / Risk 需要判断当前实现是否存在 bypass path

不适用于：
- 纯 UI 体验问题
- 纯账务对账问题
- 没有资源对象和访问路径定义的空泛讨论

---

## 输入模板

```yaml
AUTHORIZATION-BYPASS-PATH-REVIEWER-INPUT:
  protected_action_or_resource: "<被保护的动作/资源>"
  actor_profile:
    actor_type: "console | agent | enduser | operator | system"
    expected_scope: "<应允许的范围>"
  visible_guards:
    frontend_visibility_guard: "yes | no | unknown"
    backend_object_authorization: "yes | no | unknown"
    project_scope_check: "yes | no | unknown"
    token_scope_check: "yes | no | unknown"
  suspected_bypass_vectors:
    - "change_project_id"
    - "direct_api_call"
    - "reuse_old_context"
    - "debug_flag"
    - "cross_object_access"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
AUTHORIZATION-BYPASS-PATH-REVIEWER-OUTPUT:
  review_result: "no_obvious_bypass | weak_authorization | likely_bypass_path | critical_bypass_risk | unclear"
  risky_vectors:
    - vector: "<可疑路径>"
      reason: "<为什么危险>"
  missing_checks:
    - "<缺失的授权检查>"
  likely_boundary_failure: "frontend_only_guard | object_auth_missing | project_scope_mismatch | token_scope_mismatch | mixed | unclear"
  recommended_actions:
    - "<建议补强动作>"
  recommended_next_owner: "Security / Risk Owner | Auth / Identity Owner | Backend | Control Plane Owner"
```

---

## 长处

1. **特别适合把“怀疑越权”压成具体 bypass vector**
2. **能抓前端显隐代替服务端授权、对象级校验缺失、project scope 漏检**
3. **对 Security / Risk、Auth、Backend、Control Plane 都很实用**
4. **是安全审查从抽象风险走向路径级审查的关键工具**

---

## 调用规则

- 优先由 `15_Security_Risk_Owner_SKILL.md` 调用
- `12_Auth_Identity_Owner_SKILL.md` 在 scope / token / project 边界争议时可协同调用
- `31_P8_Backend_PUA_SKILL.md` 在对象级授权实现排查时可引用输出
- `18_Control_Plane_Owner_SKILL.md` 在后台归属与对象边界争议时可协同使用
- 输出应进入 `SECURITY-RISK-VERDICT`、`IDENTITY-DECISION` 或 `ISSUE-LEDGER.evidence`

---

## 禁止行为

- 禁止把“前端看不到按钮”当作没有绕过路径
- 禁止只审 token，不审对象级授权和 project scope
- 禁止把绕过怀疑写成结论但不给具体 vector

---

## 激活确认

```text
[Authorization Bypass Path Reviewer Tool 已激活]
定位：越权绕过路径审查器 · 对象级授权缺口发现器
默认输出：AUTHORIZATION-BYPASS-PATH-REVIEWER-OUTPUT
```
