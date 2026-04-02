# HGS 角色整合与最小强运行集方案

## 目标

把 HGS 从 **23 角色全量常驻** 收敛为 **6 常驻 + 4 按需唤起** 的运行时模型，降低 ChatGPT 对话层的上下文压力与伪精确，同时保留旧 23 角色作为角色字典。

## 常驻角色（6）

1. Lead Orchestrator
2. Policy / Domain Owner
3. Identity / Security Owner
4. Platform Owner
5. Execution Lead
6. Validation Owner

## 按需唤起（4）

1. Frontend / Console Specialist
2. Operations / Support Owner
3. Documentation Sink
4. P10 Strategic Escalation

## 23 → 6 / 4 映射

- `20_P9_Principal` → `21_Lead_Orchestrator`
- `10_P10_CTO` → 按需保留为 `P10 Strategic Escalation`
- `11_Product_Business_Rules_Owner` + `13_Billing_Entitlement_Owner` + `14_Release_Config_Owner` → `22_Policy_Domain_Owner`
- `12_Auth_Identity_Owner` + `15_Security_Risk_Owner` → `23_Identity_Security_Owner`
- `18_Control_Plane_Owner` + `19_Execution_Plane_Owner` → `24_Platform_Owner`
- `30_P8_PUA_Enhanced` + `31_P8_Backend_PUA` + `34_P8_LanrenJingling_PUA` + `35_P8_Agent_PUA` + `36_P8_EndUser_PUA` → `25_Execution_Lead`
- `37_QA_Validation_Owner` + `38_SRE_Observability_Owner` → `26_Validation_Owner`
- `32A/32B/33A/33B` → `27_Frontend_Console_Specialist`
- `16_Agent_Operations_Owner` + `17_EndUser_Support_Owner` → `28_Operations_Support_Owner`
- `39_Knowledge_Documentation_Owner` → `29_Documentation_Sink`

## 设计原则

### 1. 角色必须有独特证据面或独特决策权
只靠语气、强调点或写法区分的角色，不应继续常驻。

### 2. P10 不再常驻
P10 只做战略终审，不再成为每次对话的默认参与者。

### 3. 前端/控制台、运营/支持、文档沉淀改为专长 lens
这三类角色在对话里过早常驻，会制造上下文拥堵与重复路由。

### 4. 旧角色继续保留
它们仍可作为：
- 历史治理底册
- 角色边界解释层
- specialist 细分来源
- route policy 追溯对象

## 启用方式

要使用这套运行时，请读取：

- `Release/MANIFEST.runtime6.json`
- `Release/00_HGS_Master_Loader_runtime6.md`

而不是默认旧版：

- `Release/MANIFEST.json`
- `Release/00_HGS_Master_Loader.md`
