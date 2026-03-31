---
name: device-identity-diff
description: 设备身份差异分析工具。用于对比 installation_id、device_id、activation_id 与上下游记录，识别正常换机、重装、漂移和误判新设备。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Device Identity Diff Tool

## 核心定位

用于回答：
- 这是不是同一台设备
- 是正常换机 / 重装 / OTA，还是身份漂移
- 为什么系统把它判成了新设备

一句话：**把“设备不一样了”拆成结构化差异，而不是靠感觉判断。**

## 输入模板

```yaml
DEVICE-IDENTITY-DIFF-INPUT:
  current_identity:
    installation_id: "<当前值>"
    device_id: "<当前值>"
    activation_id: "<当前值，可为空>"
  historical_identity:
    installation_id: "<历史值>"
    device_id: "<历史值>"
    activation_id: "<历史值，可为空>"
  context:
    scenario: "switch_device | reinstall | ota | cache_clear | unknown"
    actor: "worker | console | enduser"
```

## 输出模板

```yaml
DEVICE-IDENTITY-DIFF-OUTPUT:
  diff_summary:
    installation_id: "same | changed | missing"
    device_id: "same | changed | missing"
    activation_id: "same | changed | missing"
  likely_case: "normal_switch | reinstall_expected | identity_drift | false_new_device | unclear"
  evidence:
    - "<证据1>"
  recommended_next_owner: "Auth / Identity Owner"
```

## 长处

- 擅长把“设备问题”从口头描述变成具体字段差异
- 对 Worker / 懒人精灵、换机、重装问题非常高频
- 是 Auth Owner 的强前置工具

## 调用规则

- 优先由 `12_Auth_Identity_Owner_SKILL.md` 调用
- Worker / EndUser / PC Console 角色在判断 device mismatch 时可前置调用
- 结果必须进入 `IDENTITY-DECISION` 或 evidence，不直接替代最终判定

## 禁止行为

- 禁止仅凭字段变化就直接下结论，不结合场景
- 禁止把正常换机场景误判为系统异常

## 激活确认

```text
[Device Identity Diff Tool 已激活]
定位：installation_id / device_id / activation_id 差异分析器
默认输出：DEVICE-IDENTITY-DIFF-OUTPUT
```
