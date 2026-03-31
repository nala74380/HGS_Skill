# HGS 全局检查与清理评分报告

> 版本：formal-2026-03-31-audit1  
> 范围：基于 `Release/MANIFEST.json`、`Release/00_HGS_Master_Loader.md`、当前 roles / tools / docs / protocols 结构做静态全局审计。  
> 说明：本报告评估的是**装配设计质量与静态联动完整度**，不是生产环境真实压测报告。

---

# 一、总评

| 维度 | 评分 | 结论 |
|---|---:|---|
| 内部闭环优先型 | **9.6 / 10** | 已稳定成立，且已进入 Manifest + Loader 双重约束 |
| 自动化联动执行 | **8.6 / 10** | 结构上已能联动，但仍偏“规则驱动”，缺少真实运行测试 harness |
| 角色 / 责任 / 能力 / 技能 / 边界 | **9.1 / 10** | 主体结构已成型，边界大体清晰，旧 32/33 已识别为冲突点并降权 |
| 工具体系 | **8.8 / 10** | 高价值工具已成体系，但 Execution Plane / SRE / Security 专属工具仍偏薄 |
| 整体清洁度 | **9.0 / 10** | 主链已明显变干净，但仓库仍保留少量历史文件，需要明确 legacy 身份 |
| 综合评分 | **9.0 / 10** | 已达到“可正式运行并可继续收敛”的质量线 |

---

# 二、检查项逐条结论

## 1. 是否依然保持内部闭环优先型

### 结论
**是，且已落实到 Manifest + Loader 双重层面。**

### 已落实点
- `automation_policy.default_behavior = internal_resolution_first`
- 内部升级链已经明确：当前 owner → 相邻协商 / 拆单 → P9 → P10 → 用户
- `question_policy = forbid_direct_user_confirmation_before_internal_exhaustion`
- `ask_user_only_when` 已限定为硬停机与高风险条件
- Loader 已把“先角色协商、再工具压实、再上级裁决、最后才升级问用户”写入运行约束

### 风险余量
- 仍需在未来的真实运行中观察：角色是否会因为工具不足或 owner 边界不熟而“软性回头问用户”

### 评分
**9.6 / 10**

---

## 2. 自动化联动执行检查测试效果如何

### 结论
**静态联动已经打通，自动化程度明显高于旧链，但还没有形成真正的“可执行测试 harness”。**

### 已经具备的联动能力
- Manifest 已登记 roles / tools / governance docs
- Loader 已规定工具先跑、结果落点、角色 / 工具调用次序
- `risk_gates`、`status_machine`、`automation_policy` 已形成基本自动推进框架
- 角色调用表与工具调用表已经为 Loader 提供治理约束

### 还不够满分的原因
- 当前测试是**静态结构审计**，不是动态运行测试
- 缺少专门的“自动化链路自检工具”或 `simulation / dry-run harness`
- 对“某个场景是否真的先跑了工具、输出是否真的落到了协议字段”的验证，仍主要依赖规则而不是机器校验

### 建议
后续应补一类“联动自检工具/协议检查器”，例如：
- `107_Protocol_Field_Completeness_Checker_SKILL.md`
- `108_Chain_Route_Simulator_SKILL.md`

### 评分
**8.6 / 10**

---

## 3. 角色 / 责任 / 能力 / 技能 / 边界 有没有落实到位

### 结论
**大体落实到位，且已经从“按岗位名堆角色”升级到“按真相 / 审查 / 执行 / 验证 / 运行 / 沉淀分层”。**

### 已落实点
- 真相 Owner 层齐全：Product / Auth / Billing / Release / Security / Control Plane / Execution Plane
- 审查层明确：P9
- 执行层已细分：Backend / UI Surface / Frontend Logic / Console Runtime / Console Mgmt UX / LanrenJingling / Agent / EndUser
- 验证 / 运行 / 沉淀层齐全：QA / SRE / Docs
- Agent / EndUser 已具备 owner 层与执行层分离
- Frontend / Console 已完成关键拆分

### 当前主要问题
- `32_P8_Frontend_PUA` 与 `33_P8_PCConsole_PUA` 旧文件仍在仓库，虽然已不在 Manifest，但语义会误导维护者
- Security / Risk、Execution Plane / SRE 仍缺少专属深工具支持，导致这些角色在复杂场景更多借用他人工具

### 本轮处理
- 已将 `32_P8_Frontend_PUA_SKILL.md` 降权为 legacy stub
- 已将 `33_P8_PCConsole_PUA_SKILL.md` 降权为 legacy stub

### 评分
**9.1 / 10**

---

## 4. 工具上有没有什么问题，对工具本身还需要配置些什么

### 结论
**当前工具体系已经能支撑主链，但“运行面 / 安全面 / 协议校验面”还不够强。**

### 当前主要问题
1. **Execution Plane / SRE 工具偏薄**
   - 还缺心跳 / 运行异常 / trace 相关专属工具
2. **Security / Risk 工具偏薄**
   - 当前更多借用 Auth / Trace / Step-up 工具，没有门禁 / 绕过 / 高风险动作专属分析器
3. **协议字段完整性缺少校验器**
   - 当前 Loader 规定了结果落点，但没有工具检查“字段是否真的落齐”
4. **自动链路缺少 dry-run 模拟器**
   - 还无法机械化验证“这条 issue 会被如何自动分流、会不会漏跑工具”

### 最值得继续配置的工具

#### A. Execution Plane / SRE
- `91_Worker_Identity_Stability_SKILL.md`
- `92_Heartbeat_Gap_Analyzer_SKILL.md`
- `98_Trace_Correlation_SKILL.md`

#### B. Security / Risk
- `109_High_Risk_Action_Guard_Checker_SKILL.md`
- `110_Authorization_Bypass_Path_Reviewer_SKILL.md`

#### C. 协议 / 自动化检查
- `107_Protocol_Field_Completeness_Checker_SKILL.md`
- `108_Chain_Route_Simulator_SKILL.md`

### 评分
**8.8 / 10**

---

## 5. 需要清理 / 降权的是否已处理

### 结论
**本轮已处理最明显的两处冲突面。**

### 已处理
- `Release/roles/32_P8_Frontend_PUA_SKILL.md` → 降权为 `legacy stub`
- `Release/roles/33_P8_PCConsole_PUA_SKILL.md` → 降权为 `legacy stub`
- `README.md` 已同步当前正式运行模型
- `Release/docs/发布说明与加载方式.md` 已同步为 roles + tools + protocols + governance docs 模型

### 后续可继续清理但不必立刻删除
- 历史说明型文档可保留，但必须靠 Manifest 决定是否 active
- 不建议现在删除 legacy stub，保留对迁移路径更安全

### 评分
**9.0 / 10**

---

# 三、哪些场景必须先跑工具

以下场景不得只靠口头判断，必须先跑工具：

1. **规则冲突**
   - 必跑：`70_Business_Rule_Matrix` 或 `71_State_Machine_Consistency`
2. **身份 / token / 刷新链争议**
   - 必跑：`72_JWT_Inspector` / `74_Session_Refresh_Trace` / `88_Console_Auth_Flow_Trace` / `90_StepUp_Resume_Checker` 之一
3. **名额 / 配额 / 点数 / 冻结争议**
   - 必跑：`76_Billing_Ledger_Reconciler` / `77_Quota_Usage_Analyzer` / `78_Freeze_Reversal_Diagnoser` 之一
4. **接口联调 / 抓包争议**
   - 必跑：`79_API_Contract_Diff` 或 `82_Network_Trace_Reviewer`
5. **版本兼容 / 升级门槛争议**
   - 必跑：`101_Compatibility_Matrix`
6. **宣称已验证 / 要 close issue**
   - 必跑：`95_Test_Matrix_Builder` 或 `96_Regression_Checklist`
7. **要沉淀为 SOP**
   - 必跑：`106_SOP_Generator`

---

# 四、哪些角色默认优先用哪些工具

## Product / Business Rules Owner
- `70_Business_Rule_Matrix`
- `71_State_Machine_Consistency`

## Auth / Identity Owner
- `72_JWT_Inspector`
- `73_Device_Identity_Diff`
- `74_Session_Refresh_Trace`
- `88_Console_Auth_Flow_Trace`
- `90_StepUp_Resume_Checker`

## Billing / Entitlement Owner
- `76_Billing_Ledger_Reconciler`
- `77_Quota_Usage_Analyzer`
- `78_Freeze_Reversal_Diagnoser`

## Release / Config Owner
- `101_Compatibility_Matrix`

## Control Plane Owner
- `89_Project_Context_Drift`
- `71_State_Machine_Consistency`

## P9 Principal
- `71_State_Machine_Consistency`
- `79_API_Contract_Diff`
- `82_Network_Trace_Reviewer`
- `95_Test_Matrix_Builder`
- `96_Regression_Checklist`

## Frontend Logic Engineer
- `79_API_Contract_Diff`
- `82_Network_Trace_Reviewer`
- `74_Session_Refresh_Trace`
- `89_Project_Context_Drift`
- `90_StepUp_Resume_Checker`

## Console Runtime Engineer
- `88_Console_Auth_Flow_Trace`
- `74_Session_Refresh_Trace`
- `89_Project_Context_Drift`
- `90_StepUp_Resume_Checker`
- `82_Network_Trace_Reviewer`

## UI Surface / Console Mgmt UX
- `85_UI_Surface_Audit`

## QA
- `95_Test_Matrix_Builder`
- `96_Regression_Checklist`

## Docs / Agent Ops / EndUser Support
- `106_SOP_Generator`
- 视场景借用 `77 / 78 / 85 / 96`

---

# 五、哪些输出必须落到哪些协议字段

## 真相类工具输出
应落到：
- `ISSUE-LEDGER.evidence`
- 对应 Owner verdict 的 evidence / findings 区

### 对应关系
- 规则类工具 → `BUSINESS-RULE-DECISION`
- 身份类工具 → `IDENTITY-DECISION`
- 账务类工具 → `BILLING-VERDICT`
- 版本兼容类工具 → `RELEASE-CONFIG-VERDICT`
- 安全借用类工具 → `SECURITY-RISK-VERDICT`
- 控制/执行平面工具 → `CONTROL-PLANE-VERDICT` / `EXECUTION-PLANE-VERDICT`

## 执行类工具输出
应落到：
- `P8-EXEC-REPORT`
- 必要时同步 `ISSUE-LEDGER`

## 验证类工具输出
应落到：
- `QA-VALIDATION-PLAN`
- `QA-VERIFICATION-RESULT`
- 必要时同步 `P9-REVIEW-VERDICT`

## 沉淀类工具输出
应落到：
- `DOCS-KNOWLEDGE-UPDATE.normalized_content`
- 或 SOP 附件文档

---

# 六、最终建议

## 建议立刻继续做的事
1. 为 `Execution Plane / SRE` 补专属工具
2. 为 `Security / Risk` 补专属工具
3. 为协议落点补完整性检查工具
4. 为自动链路补 dry-run 模拟器

## 当前可以停止继续拆角色
角色层已经足够完整，接下来不宜继续无节制细分。

## 当前可以进入的阶段
当前 HGS 已从“搭骨架”进入：

**治理收敛 + 自动装配完善 + 工具深化**

---

# 七、结论

当前 HGS 正式发布版已经具备：

- 内部闭环优先
- 角色 / 工具 / 文档协同装配
- 基本自动推进能力
- 明确的降权与 legacy 管理
- 明确的工具先跑场景与输出落点

本轮最重要的动作不是再堆文件，而是：

**继续补运行面 / 安全面 / 协议校验面的专属工具，让静态治理进一步变成可验证的自动治理。**
