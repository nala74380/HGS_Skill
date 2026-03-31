---
name: freeze-reversal-diagnoser
description: 冻结与冲正诊断工具。用于重建点数冻结、释放、冲正链路，识别异常冻结、漏冲正、不当冲正与冻结后果归因，辅助 Billing / Agent Ops / Backend 处理经营争议。
version: formal-2026-03-31-t4
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Freeze Reversal Diagnoser Tool

## 核心定位

这个工具专门解决：
- 为什么点数冻结了没释放
- 这次失败到底该不该冲正
- 是漏冲正、误冲正，还是根本不该冲
- 当前冻结 / 释放 / 冲正链到底断在了哪一步

一句话：**把“点数卡住了”拆成冻结、释放、冲正三段链路的具体诊断。**

---

## 适用场景

适用于：
- 授权 / 续期 / 开通失败后冻结未释放
- 代理投诉“点数被扣了但没成功”
- 某次失败应冲正但账本没有回补
- 疑似重复冲正 / 不当冲正
- Billing Owner 需要判断该由系统自动处理还是必须人工介入

不适用于：
- 纯名额占用争议
- 纯 token / session 问题
- 没有冻结/冲正流水时的空泛推测

---

## 输入模板

```yaml
FREEZE-REVERSAL-DIAGNOSER-INPUT:
  subject_scope:
    account_id: "<账号ID，可为空>"
    agent_id: "<代理ID，可为空>"
    project_id: "<项目ID，可为空>"
  transaction_timeline:
    - time: "<时间点>"
      event: "freeze_created | operation_started | operation_failed | operation_succeeded | freeze_released | reversal_created"
      amount: <数值>
      note: "<补充说明>"
  current_snapshot:
    balance: <数值>
    frozen: <数值>
    available: <数值>
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
FREEZE-REVERSAL-DIAGNOSER-OUTPUT:
  chain_result: "normal | abnormal_freeze | missing_reversal | improper_reversal | partial | unclear"
  chain_findings:
    freeze_stage:
      - "<冻结阶段发现>"
    release_stage:
      - "<释放阶段发现>"
    reversal_stage:
      - "<冲正阶段发现>"
  likely_root_cause: "expected_freeze_no_issue | freeze_not_released | failure_without_reversal | duplicate_reversal | mismatch_between_timeline_and_snapshot | unclear"
  recommended_actions:
    - "<建议动作>"
  recommended_next_owner: "Billing / Entitlement Owner | Agent Operations Owner | Backend"
  evidence:
    - "<关键证据>"
```

---

## 长处

1. **非常适合处理“扣了但没成”“冻结了没回”的经营争议**
2. **比单纯账本对账更聚焦冻结 / 冲正链**
3. **对 Billing、Agent Ops、Backend 都是高频辅助工具**
4. **能帮助区分系统自动可修 vs 必须人工介入**

---

## 调用规则

- 优先由 `13_Billing_Entitlement_Owner_SKILL.md` 调用
- `16_Agent_Operations_Owner_SKILL.md` 在代理投诉与续期争议时可前置调用
- `31_P8_Backend_PUA_SKILL.md` 在冻结/冲正实现问题排查时可引用输出
- 输出应进入 `BILLING-VERDICT`、`AGENT-OPS-VERDICT` 或执行 issue 的 evidence 区

---

## 禁止行为

- 禁止只看余额快照，不还原冻结/冲正时间线
- 禁止把所有失败都简单归为“应冲正”
- 禁止在没有 transaction_timeline 时给出精确账务动作建议

---

## 激活确认

```text
[Freeze Reversal Diagnoser Tool 已激活]
定位：冻结/释放/冲正链诊断器 · 经营争议归因辅助器
默认输出：FREEZE-REVERSAL-DIAGNOSER-OUTPUT
```
