---
name: compatibility-matrix
description: 兼容矩阵工具。用于对比客户端、服务端、脚本包、接口字段与版本门槛，识别可兼容、需升级、不可兼容和潜在灰区。
version: formal-2026-03-31-t2
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Compatibility Matrix Tool

## 核心定位

这个工具专门解决：
- 当前版本组合到底能不能一起工作
- 是必须升级、建议升级，还是已经不可兼容
- 某次问题是代码 bug，还是版本组合本来就不兼容
- 服务端、Console、Worker、.lrj 包之间的兼容边界到底在哪里

一句话：**把“版本可能有问题”变成结构化的兼容矩阵判断。**

---

## 适用场景

适用于：
- PC Console 与服务端版本协同判断
- Worker / 懒人精灵脚本包与服务端版本判断
- `version_min` 触发后的升级判断
- 新旧接口字段兼容性分析

不适用于：
- 没有版本信息时的纯猜测
- 纯业务规则拍板
- 纯 UI 表面问题

---

## 输入模板

```yaml
COMPATIBILITY-MATRIX-INPUT:
  server_version: "<服务端版本>"
  console_version: "<Console版本，可为空>"
  worker_version: "<Worker版本，可为空>"
  package_version: "<脚本包/.lrj版本，可为空>"
  version_constraints:
    version_min: "<最低版本，可为空>"
    version_target: "<目标版本，可为空>"
  contract_notes:
    - "<字段/接口/行为变化说明>"
```

---

## 输出模板

```yaml
COMPATIBILITY-MATRIX-OUTPUT:
  overall_result: "compatible | upgrade_recommended | upgrade_required | incompatible | unclear"
  pairwise_results:
    - pair: "server-console"
      result: "compatible | incompatible | unclear"
    - pair: "server-worker"
      result: "compatible | incompatible | unclear"
    - pair: "server-package"
      result: "compatible | incompatible | unclear"
  blocking_reasons:
    - "<阻断原因>"
  recommended_actions:
    - "<建议动作>"
  recommended_next_owner: "Release / Config Owner | QA | P9"
```

---

## 长处

1. **非常适合版本争议和升级判断**
2. **能把“先更新试试”变成明确的兼容性结论**
3. **对 Console、Worker、Release、QA 都有价值**
4. **在 `version_min` / 热更新 / 回滚判断里尤其有用**

---

## 调用规则

- Release / Config Owner 未来补齐后应作为首要使用者
- 现在可由 PC Console、Worker、QA、P9 在版本争议时前置调用
- 输出不得替代 P10 的发布路线拍板
- 若涉及真实升级决策，应进一步交给 Release / Config / P10

---

## 禁止行为

- 禁止没有版本样本就输出精确兼容结论
- 禁止把兼容矩阵结果直接当发布批准
- 禁止忽略接口行为变化，只比版本号大小

---

## 激活确认

```text
[Compatibility Matrix Tool 已激活]
定位：版本组合兼容性判断器 · 升级/阻断边界分析器
默认输出：COMPATIBILITY-MATRIX-OUTPUT
```
