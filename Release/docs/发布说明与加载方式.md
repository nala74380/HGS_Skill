# 发布说明与加载方式

## 本版定位

这是 HGS 的正式发布结构，当前正式运行模型为：

- Manifest 驱动装配
- Master Loader 统一入口
- Roles / Tools / Protocols / Governance Docs 协同生效
- 执行模式固定为 `full_loop`

本版不再使用“单入口大文件”或“多入口并存”的方式。

---

## 推荐仓库布局

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

## 当前正式装配范围

正式装配链当前承认以下四类文件：

1. `roles/`：角色 Skill
2. `tools/`：工具 Skill
3. `protocols/`：协议文件
4. `docs/`：治理文档（角色调用关系 / 工具调用关系 / 基线说明）

说明：

- 并非 `Release/` 下所有文件都会自动生效，只有登记在 `MANIFEST.json` 中的文件才属于正式运行集
- `legacy` / `historical` 文件可保留在仓库中，但不应被当作 active chain 加载

---

## 推荐启动口令

```text
读取 `Release/MANIFEST.json`，并按其中的 `load_order / tool_load_order / documentation_load_order` 装配整个 HGS 正式发布版。
本轮只承认 `Release/` 下且已登记在 `MANIFEST.json` 中的文件为有效 Skill 源。
执行模式：`full_loop`。
我后续上传的文件默认进入：
真相Owner识别 → P9审查派单 → P8执行 → 体验验证 / QA / SRE → P9复审 → P10终审（按需） → Docs沉淀 → Closeout。
命中 `risk_gates` 时显式停下。
```

---

## 当前治理约束

装配时应同时承认以下两份治理文档：

- `docs/角色调用关系总表.md`
- `docs/工具调用关系总表.md`

这两份文档用于约束：

- 谁先看
- 谁能拍板
- 哪些场景必须先跑工具
- 哪些工具不能替代真相 Owner
- 哪些结果必须落到协议字段

---

## 不推荐做法

- 只读 Master Loader，不读 roles / tools / protocols / docs
- 只读角色文件，不读工具与治理文档
- 在仓库里继续把 legacy 文件当 active chain 加载
- 在角色文件内各自维护不同的 Exec Report / Review 格式
- 用 README 代替 Manifest

---

## 当前已降权的典型旧文件

以下文件保留在仓库中仅供历史追溯，不属于正式装配链：

- `roles/32_P8_Frontend_PUA_SKILL.md`
- `roles/33_P8_PCConsole_PUA_SKILL.md`

它们已分别被以下正式角色替代：

- `32A_P8_UI_Surface_Engineer_SKILL.md`
- `32B_P8_Frontend_Logic_Engineer_SKILL.md`
- `33A_P8_Console_Runtime_Engineer_SKILL.md`
- `33B_P8_Console_Management_Experience_Engineer_SKILL.md`
