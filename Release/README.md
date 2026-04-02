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
