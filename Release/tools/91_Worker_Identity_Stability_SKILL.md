---
name: worker-identity-stability
description: Worker 身份稳定性分析工具。用于重建 installation_id、worker_id、device_id、token 绑定与重装迁移关系，识别 Worker 身份漂移、重复注册、错误复用与身份抖动问题。
version: formal-2026-03-31-t6
author: OpenAI
role: Tool
status: active
kind: runtime_tool
---

# Worker Identity Stability Tool

## 核心定位

这个工具专门解决：
- Worker 为什么一会儿像老设备，一会儿像新设备
- installation_id / worker_id / device_id / token 到底是不是同一个执行主体
- 重装、换机、迁移后为什么出现重复注册或错误复用
- 执行面身份不稳定，导致门禁、心跳、运行状态都看起来不可信

一句话：**把“这个 Worker 到底是谁、稳不稳定”拆成身份绑定链与漂移模式分析。**

---

## 适用场景

适用于：
- Worker 身份漂移
- installation_id / worker_id / device_id 对不齐
- 重装后被识别成新主体或错误复用旧主体
- token 绑定错位导致执行门禁异常
- Execution Plane / Auth / LanrenJingling 对同一执行主体结论不一致

不适用于：
- 纯业务规则争议
- 纯 UI 表面问题
- 没有任何身份样本时的空泛猜测

---

## 输入模板

```yaml
WORKER-IDENTITY-STABILITY-INPUT:
  subject_scope:
    installation_id: "<可为空>"
    worker_id: "<可为空>"
    device_id: "<可为空>"
    token_id: "<可为空>"
    project_id: "<可为空>"
  identity_events:
    - time: "<时间点>"
      event: "install | first_register | rebind | token_refresh | reinstall | migrate | heartbeat | unregister"
      note: "<补充说明>"
  observed_mappings:
    - installation_id: "<可为空>"
      worker_id: "<可为空>"
      device_id: "<可为空>"
      token_id: "<可为空>"
      state: "stable | drifting | duplicated | unknown"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
WORKER-IDENTITY-STABILITY-OUTPUT:
  stability_result: "stable | drifting | duplicated | reused_wrong_identity | unclear"
  identity_findings:
    stable_bindings:
      - "<稳定绑定>"
    drift_signals:
      - "<漂移信号>"
    duplicate_signals:
      - "<重复注册/重复主体>"
  likely_root_cause: "reinstall_identity_reset | token_reuse_mismatch | duplicate_registration | mapping_conflict | unclear"
  recommended_actions:
    - "<建议动作>"
  recommended_next_owner: "Execution Plane Owner | Auth / Identity Owner | P8 LanrenJingling"
```

---

## 长处

1. **特别适合把 Worker 执行主体的混乱状态压成绑定链结论**
2. **能把重装/换机/迁移导致的身份问题和普通在线异常区分开**
3. **对 Execution Plane、Auth、LanrenJingling 三方都非常高频**
4. **是运行面工具里最核心的“主体可信度检查器”之一**

---

## 调用规则

- 优先由 `19_Execution_Plane_Owner_SKILL.md` 调用
- `12_Auth_Identity_Owner_SKILL.md` 在 Worker 身份真相争议时可协同调用
- `34_P8_LanrenJingling_PUA_SKILL.md` 在安装/重装/执行端排查时可引用输出
- 输出应进入 `EXECUTION-PLANE-VERDICT`、`IDENTITY-DECISION` 或 `P8-EXEC-REPORT`

---

## 禁止行为

- 禁止只看单一 ID 就断言主体稳定
- 禁止把身份漂移误判成普通弱网或单次 token 过期
- 禁止忽略 reinstall / migrate 对 identity mapping 的影响

---

## 激活确认

```text
[Worker Identity Stability Tool 已激活]
定位：Worker主体绑定链分析器 · 身份漂移与重复注册识别器
默认输出：WORKER-IDENTITY-STABILITY-OUTPUT
```
