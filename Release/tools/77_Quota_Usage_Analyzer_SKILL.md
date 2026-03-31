---
name: quota-usage-analyzer
description: 名额占用分析工具。用于重建账号/代理/项目当前配额占用、已分配、可释放与异常占用状态，辅助 Billing / Agent Ops / EndUser Support 识别“名额为什么满了”。
version: formal-2026-03-31-t4
author: OpenAI
role: Tool
status: active
kind: analysis_tool
---

# Quota Usage Analyzer Tool

## 核心定位

这个工具专门解决：
- 为什么名额满了
- 当前到底哪些设备 / 安装 / 项目占用了配额
- 名额释放了没有
- 是正常占用、重复占用、僵尸占用，还是显示错了

一句话：**把“名额怎么就没了”拆成具体占用对象、占用原因和可释放边界。**

---

## 适用场景

适用于：
- 终端用户报“名额已满”
- 代理侧需要协助释放/核对名额
- 配额显示与实际激活设备不一致
- 换机 / 重装 / 卸载后名额未按预期释放
- 授权记录、设备记录、配额记录互相对不上

不适用于：
- 纯点数冻结/冲正问题
- 纯 token / session 问题
- 没有任何配额、设备、授权样本时的空泛判断

---

## 输入模板

```yaml
QUOTA-USAGE-ANALYZER-INPUT:
  subject_scope:
    account_id: "<账号ID，可为空>"
    agent_id: "<代理ID，可为空>"
    project_id: "<项目ID，可为空>"
  quota_snapshot:
    quota_total: <总名额>
    quota_used: <已占用>
    quota_available: <可用>
  occupancy_records:
    - subject: "<设备/安装/激活主体>"
      installation_id: "<可为空>"
      device_id: "<可为空>"
      activation_id: "<可为空>"
      project_id: "<可为空>"
      state: "occupied | released | expired | unknown"
  current_question: "<当前争议>"
```

---

## 输出模板

```yaml
QUOTA-USAGE-ANALYZER-OUTPUT:
  quota_truth:
    quota_total: <总名额>
    quota_used: <真实占用>
    quota_available: <真实可用>
  occupancy_classification:
    normal_occupancy:
      - "<正常占用对象>"
    stale_occupancy:
      - "<僵尸占用对象>"
    duplicate_occupancy:
      - "<重复占用对象>"
    unclear_occupancy:
      - "<无法确认的占用对象>"
  likely_root_cause: "normal_limit | stale_occupancy | duplicate_bind | mismatch_between_records | unclear"
  recommended_next_owner: "Billing / Entitlement Owner | Agent Operations Owner | EndUser Support Owner"
  evidence:
    - "<关键证据>"
```

---

## 长处

1. **特别适合处理“名额已满”这类高频争议**
2. **能把配额占用拆到具体设备/安装/激活对象**
3. **适合 Billing / Agent Ops / EndUser 三方共用**
4. **能帮助判断是该释放、该升级，还是根本就是真满了**

---

## 调用规则

- 优先由 `13_Billing_Entitlement_Owner_SKILL.md` 调用
- `16_Agent_Operations_Owner_SKILL.md` 与 `17_EndUser_Support_Owner_SKILL.md` 在名额争议时可前置调用
- `35_P8_Agent_PUA_SKILL.md` 与 `36_P8_EndUser_PUA_SKILL.md` 在逐单排查时可引用输出
- 输出应进入 `BILLING-VERDICT`、`AGENT-OPS-VERDICT` 或 `ENDUSER-SUPPORT-VERDICT` 的 evidence 区

---

## 禁止行为

- 禁止只看配额总数，不核对实际占用对象
- 禁止把“显示已满”直接当真满，不检查僵尸占用和重复占用
- 禁止在没有 occupancy records 时输出精确释放建议

---

## 激活确认

```text
[Quota Usage Analyzer Tool 已激活]
定位：名额占用重建器 · 僵尸/重复占用识别器 · 配额争议辅助器
默认输出：QUOTA-USAGE-ANALYZER-OUTPUT
```
