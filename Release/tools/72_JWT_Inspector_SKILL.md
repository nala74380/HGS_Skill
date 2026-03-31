---
name: jwt-inspector
description: JWT 检视工具。用于解析 Token 类型、作用域、有效期、主体一致性与常见认证异常，不替代 Auth Owner 最终裁定。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# JWT Inspector Tool

## 发布版装配位置

- 运行层级：`tools/72_JWT_Inspector_SKILL.md`
- 本文件是 **工具型 Skill**，不是角色 Skill
- 不替代 `12_Auth_Identity_Owner_SKILL.md` 最终拍板

---

## 核心定位

这个工具专门解决：
- 当前 token 到底是什么类型
- token 是否过期
- aud / scope / actor_type 是否匹配
- 当前请求与 token 主体是否一致
- 当前问题更像认证失败、授权失败，还是 token 混用

一句话：**把 token 从黑盒还原成可判定的身份证据。**

---

## 适用场景

适用于：
- ConsoleToken / WorkerToken 混用排查
- project_scope 不匹配排查
- refresh / recent-auth / step-up 相关争议
- 401 / 403 / device mismatch / session revoked 分型

不适用于：
- 纯业务规则裁定
- 纯流水对账
- 没有 token 样本时的空泛推测

---

## 输入模板

```yaml
JWT-INSPECTOR-INPUT:
  token_sample: "<JWT字符串或解码结果>"
  request_context:
    endpoint: "<请求接口>"
    actor: "console | worker | agent | enduser"
    project_id: "<项目ID，可为空>"
  expected_token_type: "ConsoleToken | WorkerToken | unknown"
  known_errors:
    - "401"
    - "403"
    - "device_mismatch"
```

---

## 输出模板

```yaml
JWT-INSPECTOR-OUTPUT:
  token_type_detected: "ConsoleToken | WorkerToken | unknown"
  claims_summary:
    aud: "<aud>"
    scope: "<scope>"
    actor_type: "<actor_type>"
    exp_state: "valid | expired | unknown"
    project_scope_state: "match | mismatch | unknown"
  principal_consistency: "consistent | inconsistent | unclear"
  likely_classification: "auth_failure | authz_failure | token_misuse | session_conflict | normal_case"
  findings:
    - "<发现1>"
    - "<发现2>"
  recommended_next_owner: "Auth / Identity Owner"
```

---

## 典型长处

1. **擅长快速拆清 token 类型和 scope**
2. **擅长把 401/403 类问题分层**
3. **擅长给 Auth Owner 提供结构化证据**
4. **适合前置过滤“看起来像认证问题”的大量噪音**

---

## 调用规则

- 优先由 `12_Auth_Identity_Owner_SKILL.md` 调用
- P9 / Backend / PC Console / Worker 在怀疑 token 问题时可先调用
- 结果必须进入 `IDENTITY-DECISION` 或 issue evidence，不得直接替代裁定

---

## 禁止行为

- 禁止仅凭 token 解析结果直接决定业务允许范围
- 禁止把签名真实性和会话真实性混为一谈
- 禁止在没有上下文的情况下过度推断

---

## 激活确认

```text
[JWT Inspector Tool 已激活]
定位：Token类型解析 · Claim结构检查 · 认证异常分型辅助
默认输出：JWT-INSPECTOR-OUTPUT
```
