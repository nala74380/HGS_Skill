# HGS 角色边界验证台账

> 版本：formal-2026-03-31-ledger2  
> 目的：把 HGS 关键角色边界、协同边界、门禁边界在当前 `int11` 口径下做**静态治理验证 + 复杂场景复演验证**，避免“角色看起来已经分层，但真实协同时边界又模糊”。  
> 说明：本台账评估的是**静态治理边界验证与复杂场景复演验证**，不是生产环境长期运行验证报告。

---

# 一、总览

## BOUNDARY-VERIFICATION-SUMMARY

```yaml
BOUNDARY-VERIFICATION-SUMMARY:
  batch_id: "hgs-role-boundary-verification-2026-03-31"
  total_boundary_checks: 14
  pass_count: 12
  conditional_pass_count: 2
  fail_count: 0
  static_governance_ready: "yes"
  complex_scenario_rehearsal_ready: "yes"
  runtime_long_run_validation_pending: "yes"
```

说明：
- 当前 14 项关键边界检查中，无 fail
- 本轮对 3 个旧 `conditional_pass` 主题做了复杂场景复演验证
- 其中 1 项升级为 `pass`，2 项仍保留 `conditional_pass`

---

# 二、边界验证清单

| check_id | 边界主题 | 参与角色 | 验证点 | 当前结果 | 依据 | 后续要求 |
|---|---|---|---|---|---|---|
| RBV-001 | P10 vs P9 | 10 / 20 | P10 管战略拍板；P9 管拆单/复审/路由 | pass | 角色总表 r2 / Loader int11 | 无 |
| RBV-002 | Product vs Auth | 11 / 12 | 业务规则真相与身份真相分离 | pass | 角色总表 r2 | 无 |
| RBV-003 | Product vs Billing | 11 / 13 | 规则口径与账务权益真相分离 | pass | 角色总表 r2 | 无 |
| RBV-004 | Control Plane vs Execution Plane | 18 / 19 | 控制平面真相与执行平面运行事实分离 | conditional_pass | 角色总表 r2 / runtime gate 接入 / 复杂场景复演 A | 建议继续观察复杂运行面批次 |
| RBV-005 | Security vs Auth | 15 / 12 | 安全门禁不越权代替身份真相；身份真相不代替安全风险裁定 | pass | 角色总表 r2 / 109 / 110 | 无 |
| RBV-006 | P9 vs P8 Enhanced | 20 / 30 | P9 负责裁决与复审；P8 Enhanced 只做兜底执行 | pass | 角色总表 r2 / 61 p5 | 无 |
| RBV-007 | Backend vs Owner Truth | 31 / 11/12/13/14/15 | Backend 负责实现，不重写真相 | pass | 角色总表 r2 | 无 |
| RBV-008 | UI Surface vs Frontend Logic | 32A / 32B | 表面体验与状态/上下文逻辑分层 | pass | 角色总表 r2 | 无 |
| RBV-009 | Console Runtime vs Console Management Experience | 33A / 33B | 管理入口运行逻辑与管理体验设计分层 | pass | 角色总表 r2 | 无 |
| RBV-010 | Agent Ops vs P8 Agent | 16 / 35 | owner 层 SOP 与逐单执行分层 | pass | 角色总表 r2 | 无 |
| RBV-011 | EndUser Support vs P8 EndUser | 17 / 36 | owner 层支持路径与逐单排查分层 | pass | 角色总表 r2 | 无 |
| RBV-012 | QA vs Docs | 37 / 39 | QA 负责证明修好；Docs 负责沉淀，不互相代位 | pass | 角色总表 r2 | 无 |
| RBV-013 | SRE vs Execution Plane | 38 / 19 | SRE 负责观测与归因；Execution Plane 负责运行事实语义 | conditional_pass | 角色总表 r2 / 113 / runtime gate / 复杂场景复演 B | 建议继续观察真实复杂事故复盘 |
| RBV-014 | Docs vs Unresolved Truth | 39 / all truth owners | Docs 不得把未裁定争议写成正式规则 | pass | 角色总表 r2 / 116 / 复杂场景复演 C | 持续用 116 做巡检 |

---

# 三、复杂场景复演验证

## 场景 A：Control Plane vs Execution Plane

### 场景描述
- 控制平面记录 worker 绑定状态已切换到新 project
- 执行平面心跳与 trace 仍显示旧 worker 在旧 project 上周期性上报
- 同时触发：project context 漂移、runtime stability gate、reroute 判断

### 预期边界
- `18_Control_Plane_Owner` 负责后台真相与归属边界
- `19_Execution_Plane_Owner` 负责运行事实与执行平面语义
- `20_P9_Principal` 负责 route dry-run、reroute、拆 owner
- 不允许任一方单独把“后台真相”或“运行事实”吃掉

### 复演结果
- 角色边界在文档与动作层面已清楚
- `runtime_stability_gate` + `108` + `114` 的组合能阻止单方裸裁定
- 但在真实复杂运行批次中，控制平面真相与执行平面事实可能仍出现长时间交叉，需要继续长期验证

### 结论
`conditional_pass`

---

## 场景 B：SRE vs Execution Plane

### 场景描述
- incident replay 通过 `113` 重建出一条跨 trace / heartbeat / worker event 的事故时间线
- SRE 认为根因在心跳采集缺口
- Execution Plane Owner 认为根因在执行主体漂移与 runtime gate 缺失
- 两者都握有部分证据，但归因角度不同

### 预期边界
- `38_SRE_Observability_Owner` 负责观测、时间线、证据缺口与线上归因建议
- `19_Execution_Plane_Owner` 负责执行平面运行事实语义与门禁归因
- 不允许 SRE 代替 Execution Plane 定义运行事实
- 不允许 Execution Plane 代替 SRE 声称监控结论已完备

### 复演结果
- 工具与角色边界已足以避免“谁都能拍根因”
- 但复杂事故复盘中，观测归因与执行事实语义之间仍需要更多真实案例校准

### 结论
`conditional_pass`

---

## 场景 C：Docs vs Unresolved Truth

### 场景描述
- 某个复杂问题经历了多轮升级
- Docs 已想把排查路径沉淀为 SOP
- 但 Product / Auth / Security 中仍有一个真相点未完全收敛
- 同时触发 `106`、`107`、`116`

### 预期边界
- `39_Knowledge_Documentation_Owner` 负责沉淀，但不得先于真相 Owner 写死结论
- `116` 必须发现正文中任何“把未裁定争议写成正式规则”的漂移
- `20_P9_Principal` 必须阻止未裁定 closeout 文档固化

### 复演结果
- 角色总表、工具矩阵、`116` 的组合已能把这类问题拦下来
- 文档先收敛于真相的问题在当前治理结构下已可被有效发现与阻断

### 结论
`pass`

---

# 四、当前通过的核心原因

## 1. 角色总表已升级到 r2
角色文档已经不只写：
- 谁说了算
- 谁不能越界

还写清了：
- 默认先跑哪些工具
- 默认命中哪些门禁动作
- 必须落哪些协议字段
- 清零循环里承担什么责任

## 2. 工具绑定关系已显式化
通过《角色-工具矩阵总表》，角色与工具的默认绑定关系已显式治理，不再靠隐含理解。

## 3. 门禁动作已 active 化
高风险、越权、运行面门禁已进入 active chain，边界不再只是文档原则，而是执行规则。

## 4. 复杂场景复演已覆盖旧 conditional 项
本轮已对旧 `conditional_pass` 项目完成一轮复杂场景复演验证，不再只停留在静态描述。

---

# 五、为什么仍有 2 项是 conditional pass

这 2 项不是因为静态治理不清，而是因为它们更依赖真实复杂场景长期验证：

1. **Control Plane vs Execution Plane**  
   在复杂运行面批次下，后台真相与运行事实可能长期交叉，需要更多真实批次复核。

2. **SRE vs Execution Plane**  
   incident replay 与 runtime gate 已接入，但真实复杂事故复盘中，观测归因与执行事实语义仍需继续校准。

---

# 六、结论

本台账当前阶段的结论只有一个：

**HGS 的角色边界在静态治理层面已经清晰，在复杂场景复演层面已经补强；剩余差距主要集中在 Control Plane / Execution Plane / SRE 三方相关的真实长期运行验证。**
