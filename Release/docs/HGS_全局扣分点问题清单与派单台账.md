# HGS 工具调用关系总表

> 版本：formal-2026-03-31-r4  
> 目的：把 HGS 当前已经落库并已接入装配链的 Tool Skill 的调用规则、优先角色、适用场景、结果落点与越界边界一次性钉死。  
> 说明：本文件是**工具治理文档**，不是运行入口；不替代 `MANIFEST` / `Master Loader`，但为正式装配链提供唯一工具调用依据。

---

# 一、总原则

## 1. 工具不是角色

HGS 中的工具 Skill 只做五件事：

1. 结构化分析  
2. 证据抽取  
3. 差异识别  
4. 门禁/评分/清零控制  
5. 结果格式化  

工具 **不能** 做四件事：

1. 替代 Owner 拍板真相  
2. 越权定义业务规则  
3. 宣布已闭环  
4. 绕过 P9 / P10 的裁决链  

一句话：

**工具负责“看清楚、判门禁、给分数、压实字段”，角色负责“拍板、执行、验证、收口”。**

## 2. 工具调用的基本顺序

```text
先识别真相 Owner / 执行 Owner
  ↓
再选对应工具做结构化分析 / 门禁 / 评分 / 清零控制
  ↓
工具结果进入 issue evidence / verdict / plan / inventory / clearance gate
  ↓
角色基于工具结果拍板或执行
```

## 3. 工具结果的默认落点

工具输出不得悬空，必须进入至少一个协议或角色输出：

- `ISSUE-LEDGER`
- `FULL-ISSUE-INVENTORY`
- `CLEARANCE-CYCLE-REPORT`
- `CLEARANCE-GATE`
- `P8-EXEC-REPORT`
- `P9-REVIEW-VERDICT`
- `QA-VALIDATION-PLAN`
- `QA-VERIFICATION-RESULT`
- `BUSINESS-RULE-DECISION`
- `IDENTITY-DECISION`
- `BILLING-VERDICT`
- `RELEASE-CONFIG-VERDICT`
- `SECURITY-RISK-VERDICT`
- `CONTROL-PLANE-VERDICT`
- `EXECUTION-PLANE-VERDICT`
- `SRE-OBSERVABILITY-VERDICT`
- `AGENT-OPS-VERDICT`
- `ENDUSER-SUPPORT-VERDICT`
- `DOCS-KNOWLEDGE-UPDATE`
- `HGS-CLOSEOUT`

---

# 二、工具分层总览

## 1. 真相判定工具

- `70_Business_Rule_Matrix_SKILL.md`
- `72_JWT_Inspector_SKILL.md`
- `73_Device_Identity_Diff_SKILL.md`
- `74_Session_Refresh_Trace_SKILL.md`
- `77_Quota_Usage_Analyzer_SKILL.md`
- `78_Freeze_Reversal_Diagnoser_SKILL.md`
- `88_Console_Auth_Flow_Trace_SKILL.md`
- `89_Project_Context_Drift_SKILL.md`
- `90_StepUp_Resume_Checker_SKILL.md`
- `101_Compatibility_Matrix_SKILL.md`

## 2. 差异 / 漂移工具

- `71_State_Machine_Consistency_SKILL.md`
- `79_API_Contract_Diff_SKILL.md`
- `82_Network_Trace_Reviewer_SKILL.md`
- `89_Project_Context_Drift_SKILL.md`
- `116_Document_State_Consistency_Sentinel_SKILL.md`

## 3. 运行面工具

- `91_Worker_Identity_Stability_SKILL.md`
- `92_Heartbeat_Gap_Analyzer_SKILL.md`
- `98_Trace_Correlation_SKILL.md`
- `113_Runtime_Incident_Replayer_SKILL.md`

## 4. 体验 / 表面审查工具

- `85_UI_Surface_Audit_SKILL.md`

## 5. 验证 / 治理工具

- `95_Test_Matrix_Builder_SKILL.md`
- `96_Regression_Checklist_SKILL.md`
- `107_Protocol_Field_Completeness_Checker_SKILL.md`
- `108_Chain_Route_Simulator_SKILL.md`
- `112_Audit_Log_Consistency_Checker_SKILL.md`
- `114_Score_Decision_Engine_SKILL.md`
- `115_Full_Issue_Clearance_Controller_SKILL.md`

## 6. 安全 / 门禁工具

- `109_High_Risk_Action_Guard_Checker_SKILL.md`
- `110_Authorization_Bypass_Path_Reviewer_SKILL.md`
- `111_Bulk_Action_Safety_Reviewer_SKILL.md`

## 7. 沉淀工具

- `106_SOP_Generator_SKILL.md`
- `116_Document_State_Consistency_Sentinel_SKILL.md`

---

# 三、工具调用总表

## 1. 当前全量工具表

| 工具 | 首要使用角色 | 次要使用角色 | 典型场景 | 默认结果落点 | 绝不能替代 |
|---|---|---|---|---|---|
| **70 Business Rule Matrix** | Product / Business Rules Owner | P9、Agent Ops、EndUser Support | 规则口径不清、状态含义冲突、自助边界争议 | `BUSINESS-RULE-DECISION` / `ISSUE-LEDGER` | Product / P10 拍板 |
| **71 State Machine Consistency** | Product / Business Rules Owner、P9 | Backend、Frontend Logic | 状态名漂移、缺失跳转、非法状态 | `BUSINESS-RULE-DECISION` / `P9-REVIEW-VERDICT` | 业务状态真相拍板 |
| **72 JWT Inspector** | Auth / Identity Owner | Frontend Logic、Console Runtime、Backend | token 类型、scope、exp、auth/authz 分型 | `IDENTITY-DECISION` / `ISSUE-LEDGER` | 身份真相拍板 |
| **73 Device Identity Diff** | Auth / Identity Owner | LanrenJingling、EndUser、Console Runtime | 换机、重装、device mismatch、误判新设备 | `IDENTITY-DECISION` / `ISSUE-LEDGER` | 身份边界拍板 |
| **74 Session Refresh Trace** | Auth / Identity Owner | Frontend Logic、Console Runtime | refresh 竞争、多标签、会话异常、recent-auth 恢复 | `IDENTITY-DECISION` / `FRONTEND-LOGIC-VERDICT` / `CONSOLE-RUNTIME-VERDICT` | 业务强制 re-auth 是否合理 |
| **76 Billing Ledger Reconciler** | Billing / Entitlement Owner | Agent Ops、Backend、P9 | 余额/冻结/可用额/授权记录对不齐 | `BILLING-VERDICT` / `ISSUE-LEDGER` | 经营规则拍板 |
| **77 Quota Usage Analyzer** | Billing / Entitlement Owner | Agent Ops、EndUser Support | 名额满、僵尸占用、重复占用、配额争议 | `BILLING-VERDICT` / `AGENT-OPS-VERDICT` / `ENDUSER-SUPPORT-VERDICT` | 名额规则拍板 |
| **78 Freeze Reversal Diagnoser** | Billing / Entitlement Owner | Agent Ops、Backend | 冻结未释放、漏冲正、误冲正 | `BILLING-VERDICT` / `ISSUE-LEDGER` | 是否允许免费恢复等经营决策 |
| **79 API Contract Diff** | P9、Backend、Frontend Logic | Console Runtime | 字段/枚举/错误结构漂移 | `ISSUE-LEDGER` / `P9-REVIEW-VERDICT` | 业务规则真相 |
| **82 Network Trace Reviewer** | Frontend Logic、Console Runtime、Backend | P9、Auth、SRE | 联调抓包、请求/响应/上下文/顺序异常 | `ISSUE-LEDGER` / `P8-EXEC-REPORT` / `P9-REVIEW-VERDICT` | 规则真相拍板 |
| **85 UI Surface Audit** | UI Surface Engineer | QA、Frontend Logic、Console Mgmt UX | 布局、层级、状态反馈、文案、响应式 | `P8-EXEC-REPORT` / `QA-VALIDATION-PLAN` | 逻辑根因拍板 |
| **88 Console Auth Flow Trace** | Console Runtime Engineer | Auth / Identity Owner | Console 登录、登出、提权、管理入口认证流 | `CONSOLE-RUNTIME-VERDICT` / `IDENTITY-DECISION` | 管理体验问题拍板 |
| **89 Project Context Drift** | Console Runtime、Frontend Logic | Control Plane Owner | project/account/context 漂移、错目标操作 | `CONSOLE-RUNTIME-VERDICT` / `FRONTEND-LOGIC-VERDICT` / `CONTROL-PLANE-VERDICT` | 控制平面真相拍板 |
| **90 StepUp Resume Checker** | Console Runtime Engineer | Frontend Logic、Auth | 提权后返回链、恢复链、失败回退 | `CONSOLE-RUNTIME-VERDICT` / `FRONTEND-LOGIC-VERDICT` / `IDENTITY-DECISION` | recent-auth 业务边界拍板 |
| **91 Worker Identity Stability** | Execution Plane Owner | Auth / Identity Owner、P8 LanrenJingling | installation/worker/device/token 绑定漂移、重复注册、重装迁移 | `EXECUTION-PLANE-VERDICT` / `IDENTITY-DECISION` / `P8-EXEC-REPORT` | 最终身份真相拍板 |
| **92 Heartbeat Gap Analyzer** | Execution Plane Owner | SRE / Observability Owner、P8 LanrenJingling | 在线/离线争议、心跳缺口、恢复抖动、更新切换 | `EXECUTION-PLANE-VERDICT` / `SRE-OBSERVABILITY-VERDICT` / `P8-EXEC-REPORT` | 真实线上状态最终裁定 |
| **95 Test Matrix Builder** | QA / Validation Owner | P9、各 P8 角色 | 验证矩阵、关键路径、风险优先级 | `QA-VALIDATION-PLAN` | “已验证通过”结论 |
| **96 Regression Checklist** | QA / Validation Owner | P9、各 P8 角色 | 快速回归、close 前核对、最小验证清单 | `QA-VERIFICATION-RESULT` / `P9-REVIEW-VERDICT` | 完整验证矩阵设计 |
| **98 Trace Correlation** | SRE / Observability Owner | Execution Plane Owner、Backend、Console Runtime | 跨前端/后端/Worker/心跳的 trace/request 链重建 | `SRE-OBSERVABILITY-VERDICT` / `EXECUTION-PLANE-VERDICT` / `P8-EXEC-REPORT` | 完整因果链最终裁定 |
| **101 Compatibility Matrix** | Release / Config Owner | QA、Console Runtime、LanrenJingling、P9 | 版本组合、version_min、升级门槛、兼容争议 | `RELEASE-CONFIG-VERDICT` / `ISSUE-LEDGER` | 是否可以冒风险发布的战略拍板 |
| **106 SOP Generator** | Knowledge / Documentation Owner | Agent Ops、EndUser Support、P9、QA | 把裁定/执行/验证沉淀成 SOP | `DOCS-KNOWLEDGE-UPDATE` | 未拍板争议写成正式规则 |
| **107 Protocol Field Completeness Checker** | P9、QA / Validation Owner | Knowledge / Documentation Owner | 协议字段缺失、evidence 悬空、closeout 断链 | `P9-REVIEW-VERDICT` / `QA-VERIFICATION-RESULT` / `DOCS-KNOWLEDGE-UPDATE` | 问题是否已解决 |
| **108 Chain Route Simulator** | P9 Principal | P8 PUA Enhanced、Docs Owner、Execution Plane Owner | dry-run 路由预演、错派/漏工具/漏验证检查 | `ISSUE-LEDGER` / `P9-REVIEW-VERDICT` / 审计记录 | 真实执行结果 |
| **109 High Risk Action Guard Checker** | Security / Risk Owner | Console Mgmt UX、Backend、Auth | 删除/冻结/解绑/扣点/授权/回滚等高风险动作门禁 | `SECURITY-RISK-VERDICT` / `P8-EXEC-REPORT` | 最终风险容忍度拍板 |
| **110 Authorization Bypass Path Reviewer** | Security / Risk Owner | Auth、Backend、Control Plane、Frontend Logic、Console Runtime | 对象级授权缺失、前端显隐代替授权、project scope 绕过 | `SECURITY-RISK-VERDICT` / `IDENTITY-DECISION` / `ISSUE-LEDGER.evidence` | 越权风险最终裁定 |
| **111 Bulk Action Safety Reviewer** | Security / Risk Owner | Backend、Release / Config、P9 | 批量删除/冻结/授权/配置变更、blast radius、rollback readiness | `SECURITY-RISK-VERDICT` / `P9-REVIEW-VERDICT` / `ISSUE-LEDGER` | 最终风险容忍度与业务取舍拍板 |
| **112 Audit Log Consistency Checker** | SRE / Observability Owner、P9 | Backend、Docs Owner、QA | 动作执行记录、协议字段与审计日志不一致 | `SRE-OBSERVABILITY-VERDICT` / `P9-REVIEW-VERDICT` / `QA-VERIFICATION-RESULT` | 问题是否已闭环 |
| **113 Runtime Incident Replayer** | SRE / Observability Owner、Execution Plane Owner | LanrenJingling、Backend | 复杂运行事故、trace/heartbeat/worker timeline 重建 | `SRE-OBSERVABILITY-VERDICT` / `EXECUTION-PLANE-VERDICT` / `ISSUE-LEDGER.evidence` | 最终运行真相拍板 |
| **114 Score Decision Engine** | P9 Principal、QA / Validation Owner | P10、Backend、Docs Owner | dispatch/review/reopen/done 的统一评分与决策输出 | `ISSUE-LEDGER` / `P9-REVIEW-VERDICT` / `QA-VERIFICATION-RESULT` / `HGS-CLOSEOUT` | 真相 Owner 与 P10 的最终拍板 |
| **115 Full Issue Clearance Controller** | P9 Principal | QA、Docs Owner | FULL-ISSUE-INVENTORY、CLEARANCE-CYCLE-REPORT、CLEARANCE-GATE 维护与 closeout 允许性判定 | `FULL-ISSUE-INVENTORY` / `CLEARANCE-CYCLE-REPORT` / `CLEARANCE-GATE` | “问题是否真的解决”最终拍板 |
| **116 Document State Consistency Sentinel** | Knowledge / Documentation Owner | P9、Agent Ops、EndUser Support、Console Mgmt UX | 文档状态漂移、装配名单不同步、正文残留旧版表述 | `DOCS-KNOWLEDGE-UPDATE` / `ISSUE-LEDGER` / `CLEARANCE-CYCLE-REPORT` | 未裁定争议能否写成正式规则 |

---

# 四、按角色看的工具调用关系

## 1. Product / Business Rules Owner
- 优先工具：`70`、`71`、`114`
- 输出落点：`BUSINESS-RULE-DECISION`

## 2. Auth / Identity Owner
- 优先工具：`72`、`73`、`74`、`88`、`90`、`110`
- Worker/执行主体争议时协同：`91`
- 输出落点：`IDENTITY-DECISION`

## 3. Billing / Entitlement Owner
- 优先工具：`76`、`77`、`78`
- 高风险账务批量动作协同：`109`、`111`
- 输出落点：`BILLING-VERDICT`

## 4. Release / Config Owner
- 优先工具：`101`
- 高风险回滚/大范围配置变更协同：`109`、`111`
- 输出落点：`RELEASE-CONFIG-VERDICT`

## 5. Security / Risk Owner
- 优先工具：`109`、`110`、`111`
- 输出落点：`SECURITY-RISK-VERDICT`

## 6. Control Plane Owner
- 优先工具：`89`、`71`、`108`、`110`
- 输出落点：`CONTROL-PLANE-VERDICT`

## 7. Execution Plane Owner
- 优先工具：`91`、`92`、`98`、`113`
- 输出落点：`EXECUTION-PLANE-VERDICT`

## 8. P9 Principal
- 优先工具：`107`、`108`、`114`、`115`、`116`
- 输出落点：`ISSUE-LEDGER`、`P9-REVIEW-VERDICT`、`FULL-ISSUE-INVENTORY`

## 9. P8 Backend
- 优先工具：`79`、`82`、`107`、`112`、`114`
- 输出落点：`P8-EXEC-REPORT`

## 10. P8 UI / Frontend / Console / Worker
- UI：`85`、`95`、`96`
- Frontend Logic：`79`、`82`、`85`、`95`、`96`
- Console Runtime：`88`、`90`、`79`、`95`
- Worker/LanrenJingling：`91`、`92`、`98`、`113`

## 11. QA / Validation Owner
- 优先工具：`95`、`96`、`107`、`114`
- closeout 前协同：`115`

## 12. SRE / Observability Owner
- 优先工具：`98`、`113`、`112`
- 运行面 gate 协同：`91`、`92`

## 13. Knowledge / Documentation Owner
- 优先工具：`106`、`107`、`116`
- 清零 closeout 前协同：`115`

---

# 五、按问题入口看的工具优先级

## 1. 规则不清 / 口径冲突
```text
70 → 71 → 114 → Product / Business Rules Owner → P9
```

## 2. token / scope / 登录态 / 刷新异常
```text
72 → 74 → 110（必要时）→ Auth / Identity Owner
```

## 3. Console 登录、提权、project context 异常
```text
88 → 89 → 90 → 33A Console Runtime → 12 Auth / 18 Control Plane
```

## 4. 接口联调 / 抓包 / 前后端甩锅
```text
82 → 79 → 112（必要时）→ 32B / 31 / 33A → 20 P9
```

## 5. 页面难用 / Console 管理台不好用
```text
85 → 32A 或 33B → 必要时 32B / 33A
```

## 6. 名额满 / 配额占用争议
```text
77 → 13 Billing / 16 Agent Ops / 17 EndUser Support → 35 / 36
```

## 7. 冻结 / 冲正 / 扣了但没成
```text
78 → 76（必要时）→ 13 Billing → 16 Agent Ops / 31 Backend
```

## 8. 版本组合 / version_min / 升级争议
```text
101 → 14 Release / Config → 37 QA / 38 SRE / 33A / 34
```

## 9. Worker 主体不稳 / 重装迁移 / 重复注册
```text
91 → 19 Execution Plane / 12 Auth / 34 LanrenJingling
```

## 10. 在线/离线争议 / 心跳缺口 / 恢复抖动
```text
92 → 19 Execution Plane / 38 SRE / 34 LanrenJingling
```

## 11. 多系统 trace / request / worker 链路断裂
```text
98 → 113（复杂事故时）→ 38 SRE / 19 Execution Plane
```

## 12. 怎么验 / 回归哪些 / 现在能不能关单
```text
95 → 96 → 107 → 114 → 115 → 37 QA / 20 P9
```

## 13. 这次会了，怎么沉淀成长期方法
```text
106 → 107 → 116（文档状态巡检时）→ 39 Docs
```

## 14. 协议字段缺失 / evidence 悬空 / closeout 断链
```text
107 → 112（必要时）→ 20 P9 / 37 QA / 39 Docs
```

## 15. 自动分流不清 / 怀疑错派 / 漏工具 / 漏验证
```text
108 → 114 → 20 P9
```

## 16. 高风险动作门禁争议
```text
109 → 111（批量或 blast radius 场景）→ 15 Security / Risk
```

## 17. 越权 / 绕过路径争议
```text
110 → 15 Security / Risk → 12 Auth / 31 Backend / 18 Control Plane
```

## 18. 清零循环 / closeout 是否允许
```text
115 → 114 → 20 P9 / 37 QA / 39 Docs
```

## 19. 文档状态漂移 / 正文残留旧版表述
```text
116 → 39 Docs / 20 P9
```

---

# 六、工具组合打法

## 1. Auth / Console 组合
```text
72 + 74 + 88 + 89 + 90 + 110
```

## 2. Billing / Agent / EndUser 组合
```text
76 + 77 + 78 + 106
```

## 3. Frontend / Backend / P9 联调组合
```text
82 + 79 + 107 + 112
```

## 4. 运行面稳定性组合
```text
91 + 92 + 98 + 113
```

## 5. QA / 收口组合
```text
95 + 96 + 107 + 114 + 115
```

## 6. Docs / 沉淀 / 状态巡检组合
```text
106 + 107 + 116
```

## 7. 自动链路治理组合
```text
108 + 107 + 114 + 115
```

## 8. 安全审查组合
```text
109 + 110 + 111
```

---

# 七、哪些场景必须至少调用一个工具

以下场景禁止纯靠口头判断，必须至少调用一个 Tool Skill：

1. 规则冲突  
2. 身份 / token / 刷新链争议  
3. 名额 / 配额 / 点数 / 冻结争议  
4. 接口联调争议  
5. 版本兼容争议  
6. Worker 主体漂移 / 重装迁移 / 重复注册  
7. 在线/离线争议 / 心跳缺口 / 恢复抖动  
8. 跨系统 trace / request / worker 链路断裂  
9. 宣称已验证  
10. 要沉淀成 SOP  
11. 协议字段缺失 / evidence 悬空 / closeout 断链  
12. 自动分流不清 / 怀疑错派 / 漏工具 / 漏验证  
13. 高风险动作门禁争议  
14. 越权 / 绕过路径争议  
15. 清零循环 / closeout 判定  
16. 文档状态漂移 / 装配名单不同步 / 正文残留旧表述  

---

# 八、工具越界红线

1. 工具不能替代真相角色拍板  
2. 工具不能替代 QA / P9 / P10 宣布“已闭环”  
3. `114` 不能替代真相 Owner 或 P10 的最终取舍  
4. `115` 不能替代“问题是否真正解决”的最终裁定  
5. `116` 不能替代 Docs Owner 判断“适用范围和受众”  
6. 工具发现多 owner 冲突、错派、运行链断点或绕过风险时，必须回到 P9 复审，不得直接各修各的。  

---

# 九、结论

到当前阶段，HGS 工具体系已经从“散装分析器”升级为：

- 真相判定工具
- 差异 / 漂移工具
- 运行面工具
- 体验审查工具
- 验证与治理工具
- 安全 / 门禁工具
- 沉淀与文档状态治理工具

本总表的使命只有一个：

**让每个角色知道什么时候该先用哪个工具，工具结果该落到哪，工具不能替代谁。**
