---
name: project-context-drift
description: 项目上下文漂移工具。用于对比当前页面、请求、管理对象与实际作用对象的 project/account 上下文，识别上下文丢失、切换漂移、误作用目标与恢复路径错位。
version: formal-2026-03-31-t3
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Project Context Drift Tool

## 核心定位

这个工具专门解决：
- 页面上看的是 A 项目，实际请求打到了 B 项目
- 切项目、切账号、提权返回后，操作对象漂移了
- UI 显示的上下文和请求里的上下文不一致
- Console / Frontend 在 project_id、account_id 的解释不一致

一句话：**把“对象不对劲”拆成上下文链到底在哪一步漂移了。**

---

## 适用场景

适用于：
- Console 切项目后管理动作打错对象
- Frontend 页面跳转后 project_id / account_id 丢失
- step-up / recent-auth 返回后上下文不一致
- 多标签、多页面、返回路径导致的对象错位

不适用于：
- 纯 token 过期问题
- 纯 UI 审美问题
- 没有上下文样本时的空泛推测

---

## 输入模板

```yaml
PROJECT-CONTEXT-DRIFT-INPUT:
  visible_context:
    project_id: "<页面显示的project_id，可为空>"
    account_id: "<页面显示的account_id，可为空>"
    page_scope: "<当前页面/模块>"
  request_context:
    project_id: "<请求实际携带的project_id，可为空>"
    account_id: "<请求实际携带的account_id，可为空>"
    target_endpoint: "<目标接口>"
  navigation_chain:
    - "<进入页面的前一步>"
    - "<提权/切换/返回路径>"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
PROJECT-CONTEXT-DRIFT-OUTPUT:
  drift_result: "no_drift | partial_drift | context_lost | wrong_target | unclear"
  findings:
    visible_vs_request_mismatch:
      - "<显示与请求不一致点>"
    navigation_risk:
      - "<导航链风险>"
    likely_drift_point:
      - "<最可能漂移点>"
  recommended_next_owner: "Frontend Logic | Console Runtime | Control Plane Owner"
  evidence:
    - "<关键证据>"
```

---

## 长处

1. **特别擅长抓“看起来在 A，实际打到 B”这类高风险问题**
2. **对 Console Runtime、Frontend Logic、Control Plane 都高频有用**
3. **能把上下文问题从模糊体感拉回可证据化的链路**
4. **适合管理台高风险动作前的复审与验证**

---

## 调用规则

- 优先由 `33A_P8_Console_Runtime_Engineer_SKILL.md` 与 `32B_P8_Frontend_Logic_Engineer_SKILL.md` 调用
- `18_Control_Plane_Owner_SKILL.md` 在涉及归属真相与显示对象争议时可协同使用
- 输出应进入 `FRONTEND-LOGIC-VERDICT`、`CONSOLE-RUNTIME-VERDICT` 或 `CONTROL-PLANE-VERDICT` 的 evidence 区

---

## 禁止行为

- 禁止只看 UI 上显示的对象，不核对请求对象
- 禁止把上下文漂移误判成单纯权限不足
- 禁止忽略导航链和返回路径对上下文的影响

---

## 激活确认

```text
[Project Context Drift Tool 已激活]
定位：project/account上下文漂移分析器 · 错目标请求发现器
默认输出：PROJECT-CONTEXT-DRIFT-OUTPUT
```
