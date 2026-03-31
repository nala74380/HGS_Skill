# HGS 角色-工具矩阵总表

> 版本：formal-2026-03-31-r1  
> 目的：把 HGS 各角色在当前 `int11` 口径下的**默认工具、优先工具、必须先跑的场景、必须落点的协议字段** 一次性钉死。  
> 说明：本文件补充《角色调用关系总表》，重点解决“角色知道该干什么，但不知道默认先跑什么工具”的问题。

---

# 一、使用原则

## 1. 角色不是裸跑
每个角色在进入执行前，应先判断：
- 默认优先工具是什么
- 哪些场景必须先跑工具
- 工具结果必须落到哪些协议字段

## 2. 工具优先级顺序
默认顺序：

```text
门禁工具
→ 诊断工具
→ 评分/清零工具
→ 协议落点检查
→ 文档沉淀工具
```

## 3. 工具不替代拍板
工具负责：
- 压实证据
- 判门禁
- 判分数
- 判字段完整度

但工具**不替代**真相 Owner / P9 / P10 的拍板。

---

# 二、角色-工具矩阵

| 角色 | 默认优先工具 | 命中这些场景必须先跑 | 工具结果必须落点 |
|---|---|---|---|
| **10_P10_CTO** | 108 / 114 | 路线冲突、优先级重排、风险容忍度判断 | P10-FINAL-DECISION / strategy notes |
| **11_Product_Business_Rules_Owner** | 70 / 107 / 114 | 规则口径冲突、状态语义不清、产品边界漂移 | Product owner verdict / ISSUE-LEDGER |
| **12_Auth_Identity_Owner** | 72 / 73 / 74 / 88 / 110 | token/session/device/project scope/auth bypass 风险 | Auth verdict / risk notes / ISSUE-LEDGER |
| **13_Billing_Entitlement_Owner** | 76 / 77 / 78 / 107 | 点数、冻结、冲正、权益、配额、账务不一致 | Billing verdict / ledger truth / ISSUE-LEDGER |
| **14_Release_Config_Owner** | 101 / 107 | 版本组合、version_min、灰度、回滚、兼容性 | Release verdict / compatibility notes |
| **15_Security_Risk_Owner** | 109 / 111 / 107 | 高风险动作、批量动作、越权/暴露/绕过 | Security verdict / guard requirements |
| **16_Agent_Operations_Owner** | 106 / 116 | 代理 SOP、代理 owner 层路径不清、文档漂移 | Agent owner policy / SOP draft |
| **17_EndUser_Support_Owner** | 106 / 116 | 用户支持 owner 层路径不清、自助与升级边界漂移 | EndUser support policy / SOP draft |
| **18_Control_Plane_Owner** | 79 / 107 / 108 | 后台真相、归属、授权配置、控制面边界争议 | Control-plane verdict |
| **19_Execution_Plane_Owner** | 91 / 92 / 98 / 113 | 心跳、在线状态、trace 断点、执行门禁异常 | Execution-plane verdict / runtime findings |
| **20_P9_Principal** | 107 / 108 / 114 / 115 / 116 | owner 不清、边界不清、需要拆单/reroute/closeout | ISSUE-LEDGER / P9-REVIEW-VERDICT / FULL-ISSUE-INVENTORY / CLEARANCE-GATE |
| **30_P8_PUA_Enhanced** | 107 / 108 / 114 | 多次失败、owner 不清、复杂兜底接管 | P8-EXEC-REPORT / takeover notes |
| **31_P8_Backend** | 79 / 107 / 108 / 112 / 114 | API/事务/数据库/契约/审计一致性 | P8-EXEC-REPORT / protocol landing / audit consistency notes |
| **32A_P8_UI_Surface_Engineer** | 85 / 95 / 96 | 布局、状态反馈、操作反馈、空态/错态/限制态 | UX evidence / experience notes |
| **32B_P8_Frontend_Logic_Engineer** | 79 / 85 / 95 / 96 | 状态管理、路由上下文、请求编排、竞态 | P8-EXEC-REPORT / regression scope |
| **33A_P8_Console_Runtime_Engineer** | 88 / 90 / 79 / 95 | ConsoleToken、project context、step-up 恢复、管理动作运行逻辑 | Console runtime exec notes |
| **33B_P8_Console_Management_Experience_Engineer** | 85 / 95 / 96 / 116 | Console 管理台信息层级、高风险反馈、文档一致性 | UX evidence / docs feedback |
| **34_P8_LanrenJingling** | 91 / 92 / 98 / 113 | Worker 身份、installation_id、心跳、热更新、执行异常 | Worker exec notes / runtime evidence |
| **35_P8_Agent** | 106 / 95 / 96 | 代理逐单执行、代理体验与闭环 | Agent experience record |
| **36_P8_EndUser** | 106 / 95 / 96 | 用户逐单排查、登录/名额/换机/项目访问 | EndUser experience record |
| **37_QA_Validation_Owner** | 95 / 96 / 107 / 114 | 验证矩阵、回归范围、可信度、验收结论 | QA-VALIDATION-PLAN / QA-VERIFICATION-RESULT |
| **38_SRE_Observability_Owner** | 98 / 113 / 112 / 107 | 日志/指标/trace 缺口、incident replay、运行归因 | runtime findings / observability gaps |
| **39_Knowledge_Documentation_Owner** | 106 / 116 / 107 | FAQ、SOP、错误码解释、知识沉淀、文档状态漂移 | DOCS-KNOWLEDGE-UPDATE / SOP draft |

---

# 三、必须先跑工具的场景总表

## 1. 高风险动作
必须先跑：
- `109_High_Risk_Action_Guard_Checker`
- 必要时 `111_Bulk_Action_Safety_Reviewer`

## 2. 越权 / Auth bypass 风险
必须先跑：
- `110_Authorization_Bypass_Path_Reviewer`
- 必要时 `72/73/74/88`

## 3. 运行面不稳定
必须先跑：
- `91_Worker_Identity_Stability`
- `92_Heartbeat_Gap_Analyzer`
- `98_Trace_Correlation`
- 必要时 `113_Runtime_Incident_Replayer`

## 4. dispatch / review / reopen / done 决策
必须先跑：
- `114_Score_Decision_Engine`

## 5. 清零循环 / closeout 前
必须先跑：
- `115_Full_Issue_Clearance_Controller`
- `107_Protocol_Field_Completeness_Checker`

## 6. 文档/审计状态巡检
必须先跑：
- `116_Document_State_Consistency_Sentinel`
- 必要时 `112_Audit_Log_Consistency_Checker`

---

# 四、工具结果必须落到哪些字段

| 工具 | 必须落点 |
|---|---|
| 107_Protocol_Field_Completeness_Checker | protocol landing result / missing fields |
| 108_Chain_Route_Simulator | simulated route / route conflicts / reroute notes |
| 109_High_Risk_Action_Guard_Checker | guard result / missing guards |
| 110_Authorization_Bypass_Path_Reviewer | bypass review result / risky vectors |
| 111_Bulk_Action_Safety_Reviewer | blast radius / rollback readiness / audit requirements |
| 112_Audit_Log_Consistency_Checker | consistency result / missing audit events / mismatched fields |
| 113_Runtime_Incident_Replayer | replay timeline / suspected breakpoints / evidence gaps |
| 114_Score_Decision_Engine | score snapshot / dispatch decision / review decision / reopen decision / done decision |
| 115_Full_Issue_Clearance_Controller | FULL-ISSUE-INVENTORY / CLEARANCE-CYCLE-REPORT / CLEARANCE-GATE |
| 116_Document_State_Consistency_Sentinel | stale body claims / missing doc registrations / required doc sync actions |

---

# 五、结论

本矩阵的作用只有一个：

**让每个角色在进入处理前，不只知道“该谁干”，还知道“默认先跑什么工具、哪些场景必须先跑工具、结果必须落到哪些字段”。**
