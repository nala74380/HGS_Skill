# HGS 角色调用关系总表

> 版本：formal-2026-03-31-r2  
> 目的：把 HGS 网络验证系统中各角色的调用顺序、拍板权限、协同边界、升级路径，以及在**评分驱动 + 清零治理 + 新增门禁动作**下的职责一次性钉死。  
> 说明：本文件是**角色调用治理文档**，不是运行入口，不替代 `MANIFEST` / `Master Loader`，但为角色协同、工具绑定、边界验证提供唯一角色治理依据。

---

# 一、总原则

## 1. 角色调用的四层顺序

HGS 的角色协同仍按以下顺序运行：

```text
真相层 → 审查裁决层 → 执行层 → 验证/运行/沉淀层
```

对应到当前角色体系：

- **真相层**：P10、Product / Business Rules、Auth / Identity、Billing / Entitlement、Release / Config、Security / Risk、Agent Ops、EndUser Support、Control Plane、Execution Plane
- **审查裁决层**：P9 Principal
- **执行层**：P8 Backend、Frontend Logic、UI Surface、Console Runtime、Console Management Experience、LanrenJingling、Agent、EndUser、P8 Enhanced
- **验证/运行/沉淀层**：QA、SRE、Knowledge / Documentation

## 2. 在 int11 口径下新增的一条硬规则

角色治理现在不只回答“谁拍板”，还必须回答：

1. **默认先跑哪些工具？**
2. **命中哪些门禁动作？**
3. **必须落哪些协议字段？**
4. **在清零循环里承担哪一段责任？**

## 3. 一条硬边界

**执行角色不能替代真相角色拍板；真相角色不能跳过 P9 直接裸派执行；验证角色不能替代真相角色重新定义问题；文档角色不能把未裁定争议写成正式规则。**

---

# 二、角色调用总流程

## 标准调用链

```text
P10（仅战略级初筛或冲突时）
  ↓
真相 Owner 识别（Product / Auth / Billing / Release / Security / Agent Ops / EndUser Support / Control Plane / Execution Plane）
  ↓
P9 Principal 审查、拆单、定 owner、定边界、定门禁、定评分/清零路径
  ↓
对应 P8 执行角色处理
  ↓
QA 验证 / SRE 运行观测 / 体验协议回收 / Docs 沉淀
  ↓
P9 复审
  ↓
P10 终审（仅必要时）
  ↓
Closeout
```

## 什么时候不从 P10 开始

绝大多数问题**不需要**先找 P10。只有出现以下情况，才需要 P10 先入场：

- 路线冲突
- 优先级重排
- 高风险与推进速度之间要做战略权衡
- 会改变平台/代理/用户的利益或承诺

否则，默认从**真相 Owner 识别 + P9 审查**开始。

---

# 三、角色总表（升级版）

| 角色 | 核心职责 | 新增默认工具 | 新增默认门禁/动作 | 必须输出 | 不能越界做什么 | 清零循环责任 |
|---|---|---|---|---|---|---|
| **10_P10_CTO** | 战略方向、优先级重排、风险容忍度 | 108 / 114 | 冲突升级、路线重裁 | P10-FINAL-DECISION | 不能代替具体 Owner 做细粒度真相裁定 | 仅在内部穷尽后做终局拍板 |
| **11_Product_Business_Rules_Owner** | 业务规则真相、状态语义、平台/代理/用户权责 | 70 / 107 / 114 | new truth 输入、reroute 参与 | Owner verdict / rule truth | 不能代替 P8 写实现 | 负责规则真相不漂移 |
| **12_Auth_Identity_Owner** | 身份真相、认证/授权分型、设备身份判定 | 72 / 73 / 74 / 88 / 110 | `auth_bypass_guard_gate` owner | Auth verdict / risk notes | 不能代替 Business Rules 定义业务允许范围 | 负责 auth 类 issue 的越权风险清零 |
| **13_Billing_Entitlement_Owner** | 账务真相、权益真相、对账结论 | 76 / 77 / 78 / 107 | 高风险账务变更前置参与 | Billing verdict / ledger truth | 不能代替 Product 决定经营策略 | 负责账务类 issue 清零 |
| **14_Release_Config_Owner** | 发布/配置边界、兼容性、灰度回滚建议 | 101 / 107 | 版本/配置 reroute、风险门禁参与 | Release verdict / compatibility notes | 不能代替工程去发布 | 负责发布边界不失真 |
| **15_Security_Risk_Owner** | 风险等级、阻断建议、必须补的门禁 | 109 / 111 / 107 | `high_risk_guard_gate` owner | Security verdict / guard requirements | 不能代替 Auth 做身份真相拍板 | 负责高风险 issue 清零与阻断 |
| **16_Agent_Operations_Owner** | 代理 owner 层 SOP、自助与升级边界 | 106 / 116 | Agent 路径校正、Docs 同步参与 | Agent owner policy / SOP notes | 不能代替 35_P8_Agent 做逐单执行 | 负责代理侧清零闭环标准 |
| **17_EndUser_Support_Owner** | 用户 owner 层支持路径、自助与升级边界 | 106 / 116 | EndUser 路径校正、Docs 同步参与 | EndUser support policy | 不能代替 36_P8_EndUser 做逐单排查 | 负责用户侧清零闭环标准 |
| **18_Control_Plane_Owner** | 控制平面归属边界、真相系统定义 | 79 / 107 / 108 | control-plane 边界判定、reroute 参与 | Control-plane verdict | 不能代替执行平面定义运行时事实 | 负责后台真相与执行平面分界 |
| **19_Execution_Plane_Owner** | 执行平面运行事实、门禁归因、运行时语义 | 91 / 92 / 98 / 113 | `runtime_stability_gate` owner | Execution-plane verdict / runtime findings | 不能代替控制平面定义归属 | 负责运行面 issue 清零 |
| **20_P9_Principal** | 拆单、定 owner、定边界、定评分/清零路径、复审 | 107 / 108 / 114 / 115 / 116 | `generate_exec_plan` / `auto_reroute_on_new_truth` / 清零循环 orchestrator | ISSUE-LEDGER / P9-REVIEW-VERDICT / reroute plan | 不能自己发明规则真相；不能裸执行代替 P8 | 负责全批次 issue inventory / reopen / closeout 路由 |
| **30_P8_PUA_Enhanced** | 多次失败、边界清晰但推进困难时兜底执行 | 107 / 108 / 114 | fallback 承接 | Exec artifacts / takeover notes | 不能代替真相 Owner 最终拍板 | 负责复杂 issue 的兜底清零 |
| **31_P8_Backend** | 后端实现修复、契约落地、数据一致性处理 | 79 / 107 / 108 / 112 / 114 | `generate_exec_plan` default executor | P8-EXEC-REPORT / protocol landing | 不能自己发明规则、授权、账务真相 | 负责主链实现与协议落点 |
| **32A_P8_UI_Surface_Engineer** | 界面表面设计与落地 | 85 / 95 / 96 | UI 风险可见性修复 | UI change notes / experience evidence | 不能代替逻辑层和业务真相拍板 | 负责表面体验类 issue 清零 |
| **32B_P8_Frontend_Logic_Engineer** | 前端状态、上下文、请求编排、竞态 | 79 / 85 / 95 / 96 | exec plan 前端实现支线 | P8-EXEC-REPORT / regression scope | 不能代替服务端权限闭环 | 负责前端逻辑类 issue 清零 |
| **33A_P8_Console_Runtime_Engineer** | Console 运行时逻辑与上下文修复 | 88 / 90 / 79 / 95 | Console runtime gate / reroute 参与 | Console runtime exec notes | 不能代替 Console UX 设计管理体验 | 负责管理台运行逻辑清零 |
| **33B_P8_Console_Management_Experience_Engineer** | 管理台 UX 设计与修正 | 85 / 95 / 96 / 116 | 高风险操作反馈设计 | UX evidence / docs feedback | 不能代替 Runtime 修运行逻辑 | 负责管理台体验类 issue 清零 |
| **34_P8_LanrenJingling** | Worker / 执行端实现修复 | 91 / 92 / 98 / 113 | runtime gate 执行支线 | Worker exec notes / runtime evidence | 不能定义身份真相和版本策略 | 负责 worker/执行端 issue 清零 |
| **35_P8_Agent** | 代理侧逐单执行与问题穷尽 | 106 / 95 / 96 | agent experience 路径执行 | Agent experience record | 不能代替 Agent Ops 定义 SOP | 负责代理逐单 issue 清零 |
| **36_P8_EndUser** | 用户侧逐单排查与快速恢复 | 106 / 95 / 96 | enduser experience 路径执行 | EndUser experience record | 不能代替 EndUser Support 定义边界 | 负责用户逐单 issue 清零 |
| **37_QA_Validation_Owner** | 验证策略、矩阵、回归、验收结论 | 95 / 96 / 107 / 114 | `validate_and_experience_by_issue` partner | QA-VALIDATION-PLAN / QA-VERIFICATION-RESULT | 不能自己改规则真相 | 负责 issue 验证闭环 |
| **38_SRE_Observability_Owner** | 运行观测、归因、止血建议、观测缺口识别 | 98 / 113 / 112 / 107 | `runtime_stability_gate` support / incident replay | runtime findings / observability gaps | 不能代替 Release 决定是否发布 | 负责运行面证据与 replay |
| **39_Knowledge_Documentation_Owner** | FAQ、SOP、错误码解释、角色边界、知识沉淀 | 106 / 116 / 107 | docs sink / stale-state cleanup | DOCS-KNOWLEDGE-UPDATE / SOP draft | 不能把未裁定争议写成正式规则 | 负责 docs sink 与边界文档不漂移 |

---

# 四、必须协同、不能单飞的新增组合

## 1. P9 + QA + Score Decision Engine

适用于：
- dispatch / review / reopen / done 的阈值判断
- owner_confidence / route_stability / evidence completeness 的决策

## 2. P9 + 15 Security + 12 Auth

适用于：
- 高风险动作
- 授权绕过 / 越权链路
- 高风险门禁与 auth bypass 同时出现

## 3. 19 Execution Plane + 38 SRE + 34 LanrenJingling

适用于：
- runtime gate
- worker identity / heartbeat / trace 三类证据交叉
- incident replay

## 4. 39 Docs + 20 P9 + 116 Sentinel

适用于：
- 文档状态漂移
- 文档正文仍残留旧版表述
- 装配名单与真实文档不同步

## 5. 20 P9 + 115 Clearance Controller

适用于：
- FULL-ISSUE-INVENTORY 更新
- CLEARANCE-CYCLE-REPORT 更新
- CLEARANCE-GATE closeout 允许性判定

---

# 五、角色边界升级规则

## 1. 谁能拍板

仍由真相 Owner 拍板：
- 业务规则真相 → 11
- 身份真相 → 12
- 账务与权益真相 → 13
- 发布与配置边界 → 14
- 安全风险边界 → 15
- 代理 owner 边界 → 16
- 用户支持 owner 边界 → 17
- 控制平面边界 → 18
- 执行平面运行事实 → 19

## 2. 谁能裁决流程

- **20_P9_Principal**：能拆单、定 owner、定边界、定 wave、定 reroute、定 closeout path，但不能越权重写真相。
- **37_QA_Validation_Owner**：能判断验证是否足够，但不能重写真相。
- **38_SRE_Observability_Owner**：能判断线上归因与止血建议，但不能重写真相。
- **39_Knowledge_Documentation_Owner**：能沉淀规则，但不能先于真相角色拍板。

## 3. 谁不能单飞

以下场景禁止单角色裸做：
- 高风险动作
- Auth bypass 风险
- Runtime instability 风险
- Closeout 判定
- 文档升级后状态一致性审查

这些场景必须至少经过：
- 对应 owner
- P9
- 对应工具门禁 / 评分工具 / 清零工具

---

# 六、当前最重要的结论

1. 角色体系本身已经稳定，不再靠继续细分角色来提质。  
2. 角色责任现在必须与**默认工具、默认门禁、默认协议输出、清零循环责任**绑定。  
3. 角色边界不是只写“谁说了算”，还要写“谁负责把 issue 从 open 推到 done”。  
4. 当前角色治理文档已经升级到 `int11` 口径，可作为角色边界的唯一治理依据。  

---

# 七、结论

到当前阶段，HGS 角色体系已经从“按岗位名堆角色”，进入到“按真相、裁决、执行、验证、运行、沉淀 + 工具绑定 + 清零责任”分层协同。  
本总表的使命只有一个：

**让每个问题进来后，不只知道该先找谁、谁能拍板、谁不能越界，还知道谁默认先跑什么工具、谁必须落什么字段、谁负责把问题真正清零。**
