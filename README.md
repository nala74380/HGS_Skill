# HGS 正式发布版总览

这是按“**Manifest 驱动、多角色、多工具、治理文档约束、只保留正式运行集**”原则整理后的正式发布仓库。

## 当前正式运行特点

- 只有 **1 个正式入口**：`Release/00_HGS_Master_Loader.md`
- 只有 **1 个正式装配清单**：`Release/MANIFEST.json`
- 角色、工具、协议、治理文档都以 Manifest 登记为准
- 旧版 legacy 文件允许保留追溯，但**不进入正式装配链**
- 主链路固定为：
  `真相Owner → P9审查派单 → P8执行 → 体验/QA/SRE → P9复审 → P10终审(按需) → Docs沉淀 → Closeout`

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
```

---

## 推荐加载方式

只以 `Release/` 为正式运行源：

```text
读取 `Release/MANIFEST.json`，并按其中的 `load_order / tool_load_order / documentation_load_order` 装配整个 HGS 正式发布版。
本轮只承认 `Release/` 下且已登记在 `MANIFEST.json` 中的文件为有效 Skill 源。
执行模式：`full_loop`。
我后续上传的文件默认进入：
真相Owner识别 → P9审查派单 → P8执行 → 体验验证 / QA / SRE → P9复审 → P10终审（按需） → Docs沉淀 → Closeout。
命中 `risk_gates` 时显式停下。
```

---

## 快速加载口令

把下面整段直接发给对话即可：

```text
读取并加载这个 GitHub 发布版的 HGS 全角色 Skill 组，作为本轮唯一生效装配源：

1. 先读取 `Release/MANIFEST.json`
2. 再读取 `Release/00_HGS_Master_Loader.md`
3. 按 `MANIFEST.json` 的 `load_order`、`tool_load_order`、`documentation_load_order` 继续加载全部已登记的 `roles/`、`tools/`、`protocols/`、`docs/`
4. 执行模式固定为 `full_loop`
5. 我后续上传的文件默认进入这条链路：
   `真相Owner识别 → P9审查派单 → P8执行 → 用户/代理体验 + QA/SRE验证 → P9复审 → P10终审/按需收口 → Docs沉淀 → Closeout`
6. 除非触发 `risk_gates` 或高风险停机条件，否则不要再让我手动点名角色或确认下一步

仓库基线：
- `Release/MANIFEST.json`
- `Release/00_HGS_Master_Loader.md`
```

---

## 快速更新升级口令

当仓库继续升级后，把下面整段直接发给对话即可：

```text
基于当前已加载的 HGS 正式发布版，将装配源升级到仓库 `main` 的最新 Release 基线：

1. 重新读取 `Release/MANIFEST.json`
2. 重新读取 `Release/00_HGS_Master_Loader.md`
3. 按最新 `MANIFEST.json` 重新装配新增或更新的 `roles/`、`tools/`、`protocols/`、`docs/`
4. 以最新 `package_version` 为唯一有效版本，覆盖旧装配口径
5. 保留当前 issue inventory / clearance context，但治理规则、动作集、工具集、文档集一律以最新 Release 为准
6. 执行模式继续固定为 `full_loop`
7. 除非命中高风险停机条件，否则继续内部闭环推进，不要退回旧入口、旧角色集或旧工具集

仓库基线：
- `Release/MANIFEST.json`
- `Release/00_HGS_Master_Loader.md`
```

---

## 当前正式装配范围

### 1. Roles
以 `Release/MANIFEST.json` 的 `roles` 与 `load_order` 为准。

### 2. Tools
以 `Release/MANIFEST.json` 的 `tools` 与 `tool_load_order` 为准。

### 3. Protocols
以 `Release/MANIFEST.json` 的 `protocols` 为准。

### 4. Governance Docs
以 `Release/MANIFEST.json` 的 `governance_docs` 与 `documentation_load_order` 为准。

---

## 当前治理约束

装配时默认承认以下治理文档：

- `Release/docs/角色调用关系总表.md`
- `Release/docs/角色-工具矩阵总表.md`
- `Release/docs/角色边界验证台账.md`
- `Release/docs/工具调用关系总表.md`
- `Release/docs/HGS_自动化联动动作总表（正式版）.md`
- `Release/docs/HGS_全局检查与清理评分报告.md`

这些文档用于约束：

- 谁先看
- 谁能拍板
- 谁不能越界
- 哪些场景必须先跑工具
- 哪些工具不能替代真相 Owner
- 哪些输出必须落到协议字段
- 哪些问题未清零不得收口

---

## 当前已降权的旧文件

以下文件保留在仓库中仅供历史追溯，不属于正式装配链：

- `Release/roles/32_P8_Frontend_PUA_SKILL.md`
- `Release/roles/33_P8_PCConsole_PUA_SKILL.md`

它们已分别被以下正式角色替代：

- `Release/roles/32A_P8_UI_Surface_Engineer_SKILL.md`
- `Release/roles/32B_P8_Frontend_Logic_Engineer_SKILL.md`
- `Release/roles/33A_P8_Console_Runtime_Engineer_SKILL.md`
- `Release/roles/33B_P8_Console_Management_Experience_Engineer_SKILL.md`

---

## 使用结论

从现在开始：

- 不要再混用旧入口文件
- 不要把未登记在 Manifest 的文件当 active chain 加载
- 不要跳过 tools / docs 直接宣称“正式发布链已完整生效”
- 升级仓库后，优先使用 README 中的“快速更新升级口令”重载最新 Release 基线

这个仓库当前的唯一正式基线，就是：

```text
Release/MANIFEST.json + Release/00_HGS_Master_Loader.md + 已登记的 roles/tools/protocols/docs
```
