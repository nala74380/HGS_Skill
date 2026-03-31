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

装配时默认承认以下两份治理文档：

- `Release/docs/角色调用关系总表.md`
- `Release/docs/工具调用关系总表.md`

这两份文档用于约束：

- 谁先看
- 谁能拍板
- 哪些场景必须先跑工具
- 哪些工具不能替代真相 Owner
- 哪些输出必须落到协议字段

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

这个仓库当前的唯一正式基线，就是：

```text
Release/MANIFEST.json + Release/00_HGS_Master_Loader.md + 已登记的 roles/tools/protocols/docs
```
