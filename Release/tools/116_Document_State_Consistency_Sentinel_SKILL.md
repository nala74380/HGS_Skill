---
name: document-state-consistency-sentinel
description: 巡检治理文档中的版本口径、时序表述、装配名单与仓库真实状态是否一致，发现“文档已升版但正文仍旧”或“文档存在但未装配”等问题。
version: formal-2026-03-31-t1
author: OpenAI
role: Tool
status: active
---

# 116 Document State Consistency Sentinel

## 作用
自动发现治理文档状态漂移，例如：
- 文档版本已更新，但正文仍引用旧版本状态
- 文档已存在，但 MANIFEST / Loader 未纳入装配清单
- 审计结论与当前 active chain 不一致

## 典型输入
- manifest_doc_lists
- loader_doc_lists
- governance_docs
- document_versions
- document_body_claims

## 典型输出
- consistency_result: pass | conditional | fail
- stale_body_claims
- missing_doc_registrations
- required_doc_sync_actions
