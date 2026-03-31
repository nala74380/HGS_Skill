---
name: api-contract-diff
description: API 合约差异工具。用于对比接口文档、前端/客户端预期与后端实际响应，识别字段漂移、枚举不一致、边界变化。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# API Contract Diff Tool

## 核心定位

用于回答：
- 前后端到底哪里没对齐
- 哪个字段变了
- 哪个枚举不一致
- 是契约漂移、文档漂移，还是实现漂移

一句话：**把“接口不对”拆成明确的 contract diff。**

## 输入模板

```yaml
API-CONTRACT-DIFF-INPUT:
  expected_contract:
    source: "<文档/前端类型/客户端预期>"
    content: "<结构化内容>"
  actual_contract:
    source: "<接口响应/后端实现/抓包样本>"
    content: "<结构化内容>"
  comparison_focus:
    - "fields"
    - "enum_values"
    - "error_shape"
    - "nullable_rules"
```

## 输出模板

```yaml
API-CONTRACT-DIFF-OUTPUT:
  diff_summary:
    fields_added:
      - "<字段>"
    fields_missing:
      - "<字段>"
    enum_mismatch:
      - "<枚举差异>"
    error_shape_mismatch:
      - "<错误结构差异>"
  likely_source_of_drift: "frontend | backend | docs | mixed"
  recommended_next_owner: "P9 / Backend / Frontend Logic"
```

## 长处

- 擅长抓“看起来差不多，但就是联不起来”的接口问题
- 对 P9 复审、Frontend Logic、Backend 非常高频
- 很适合进入 ISSUE evidence 和 REVIEW verdict

## 调用规则

- P9、Backend、Frontend Logic 均可高频调用
- 结果必须落入 issue evidence，不直接宣布谁对谁错
- 如涉及业务含义差异，再交 Product / Business Rules Owner

## 禁止行为

- 禁止把 contract diff 当成业务规则裁定
- 禁止只对比正常路径，忽略错误结构和边界值

## 激活确认

```text
[API Contract Diff Tool 已激活]
定位：字段/枚举/错误结构差异分析器
默认输出：API-CONTRACT-DIFF-OUTPUT
```
