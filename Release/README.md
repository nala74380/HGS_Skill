# HGS 正式发布版总览（Runtime6 默认）

这是按“**Manifest 驱动、最小强运行集、GitHub/Thinking 场景优先、旧角色保留为字典层**”原则整理后的正式发布仓库。

## 当前默认运行特点

- 只有 **1 个默认正式入口**：`Release/00_HGS_Master_Loader.md`
- 只有 **1 个默认正式装配清单**：`Release/MANIFEST.json`
- 默认运行集从 **23 角色全量常驻** 收敛为 **6 个常驻角色 + 4 个按需唤起角色**
- 旧 23 角色继续保留在仓库中，但**不再作为默认对话 runtime 常驻集**
- 主链路固定为：  
  `Lead Orchestrator → 真相 Owner → Execution Lead → Validation Owner → 按需专家 → Docs Sink → P10终审(按需) → Closeout`

---

## 当前默认运行角色

### 常驻角色（6）

1. Lead Orchestrator  
2. Policy / Domain Owner  
3. Identity / Security Owner  
4. Platform Owner  
5. Execution Lead  
6. Validation Owner  

### 按需唤起角色（4）

1. Frontend / Console Specialist  
2. Operations / Support Owner  
3. Documentation Sink  
4. P10 Strategic Escalation  

---

## 当前正式仓库结构

```text
HGS_Skill/
├─ README.md
└─ Release/
   ├─ MANIFEST.json
   ├─ 00_HGS_Master_Loader.md
   ├─ roles/
   ├─ tools/
   ├─ protocols/
   └─ docs/

##推荐加载方式

只以 Release/ 为正式运行源：

读取 `https://github.com/nala74380/HGS_Skill/blob/main/Release/MANIFEST.json`，并按其中的 `load_order / on_demand_role_load_order / tool_load_order / documentation_load_order` 装配整个 HGS 正式发布版。

本轮只承认 `Release/` 下且已登记在 `MANIFEST.json` 中的文件为有效 Skill 源。

执行模式：`full_loop`。

默认只常驻以下 6 个角色：
- Lead Orchestrator
- Policy / Domain Owner
- Identity / Security Owner
- Platform Owner
- Execution Lead
- Validation Owner

以下角色按需唤起：
- Frontend / Console Specialist
- Operations / Support Owner
- Documentation Sink
- P10 Strategic Escalation

##快速加载口令

把下面整段直接发给对话即可：

读取并加载这个 GitHub 发布版的 HGS Runtime6 正式版，作为本轮唯一生效装配源：

1. 先读取 `https://github.com/nala74380/HGS_Skill/blob/main/Release/MANIFEST.json`
2. 再读取 `https://github.com/nala74380/HGS_Skill/blob/main/Release/00_HGS_Master_Loader.md`
3. 按 `MANIFEST.json` 的 `load_order`、`on_demand_role_load_order`、`tool_load_order`、`documentation_load_order` 继续加载全部已登记的 `roles/`、`tools/`、`protocols/`、`docs/`
4. 执行模式固定为 `full_loop`
5. 默认只常驻以下 6 个角色：
   `Lead Orchestrator → Policy/Domain → Identity/Security → Platform → Execution Lead → Validation`
6. 以下角色按需唤起，不要默认全量常驻：
   `Frontend/Console Specialist / Operations/Support Owner / Documentation Sink / P10 Strategic Escalation`
7. 除非触发 `risk_gates` 或高风险停机条件，否则不要退回旧 23 角色全量常驻模式，也不要再让我手动点名角色或确认下一步

仓库基线：
- `https://github.com/nala74380/HGS_Skill/blob/main/Release/MANIFEST.json`
- `https://github.com/nala74380/HGS_Skill/blob/main/Release/00_HGS_Master_Loader.md`


##快速更新升级口令

当仓库继续升级后，把下面整段直接发给对话即可：

基于当前已加载的 HGS Runtime6 正式发布版，将装配源升级到仓库 `main` 的最新 Release 基线：

1. 重新读取 `https://github.com/nala74380/HGS_Skill/blob/main/Release/MANIFEST.json`
2. 重新读取 `https://github.com/nala74380/HGS_Skill/blob/main/Release/00_HGS_Master_Loader.md`
3. 按最新 `MANIFEST.json` 重新装配新增或更新的 `roles/`、`tools/`、`protocols/`、`docs/`
4. 以最新 `package_version` 为唯一有效版本，覆盖旧装配口径
5. 保留当前 issue inventory / clearance context，但治理规则、动作集、工具集、文档集一律以最新 Release 为准
6. 执行模式继续固定为 `full_loop`
7. 除非命中高风险停机条件，否则继续内部闭环推进，不要退回旧入口、旧角色全量常驻模式或旧工具集

仓库基线：
- `https://github.com/nala74380/HGS_Skill/blob/main/Release/MANIFEST.json`
- `https://github.com/nala74380/HGS_Skill/blob/main/Release/00_HGS_Master_Loader.md`




































