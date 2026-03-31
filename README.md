# HGS 纯净联动版总包

这是按“**直接删除废弃、取消兼容、只保留正式版本**”原则重做的总包。

## 本包特点

- 只有 **1 个总入口**：`HGS_AutoLoop_Master_SKILL.md`
- 不保留任何兼容包装文件
- 不保留任何废弃入口
- 不保留重复版本号文件名
- 角色文件全部收敛为单一正式版
- 对 P9 / P8 Enhanced / 各专项 P8 做了逐份审查后合并，避免“新版有协议、旧版有细节”的断层
- P10/P9审查 → P9派单 → P8执行 → 用户/代理体验 → P9复审 → P10终审（按需） → 收口 ✅

## 建议加载方式

只手动加载：
`HGS_AutoLoop_Master_SKILL.md`

## 本包文件

1. `HGS_AutoLoop_Master_SKILL.md`：唯一主入口
2. `P10_CTO_SKILL.md`：战略裁剪
3. `P9_Principal_SKILL.md`：审查、派单、复审
4. `P8_PUA_Enhanced_SKILL.md`：通用深化执行兜底
5. `P8_Backend_PUA_SKILL.md`
6. `P8_Frontend_PUA_SKILL.md`
7. `P8_LanrenJingling_PUA_SKILL.md`
8. `P8_PCConsole_PUA_SKILL.md`
9. `P8_Agent_PUA_SKILL.md`
10. `P8_EndUser_PUA_SKILL.md`
11. `P8_Agent_Review_Protocol.md`
12. `P8_EndUser_Review_Protocol.md`
13. `RE_REVIEW_PROTOCOL.md`
14. `00_全局严审与清理报告.md`

## 加载口令

读取并加载这个 GitHub 发布版的 HGS 全角色 Skill 组，作为本轮唯一生效装配源：

1. 先读取 `https://github.com/nala74380/HGS_Skill/blob/main/Release/MANIFEST.json`
2. 再读取 `https://github.com/nala74380/HGS_Skill/blob/main/Release/00_HGS_Master_Loader.md`
3. 按 `MANIFEST.json` 的 `load_order` 继续加载 `Release/roles/` 与 `Release/protocols/` 下全部必需文件
4. 执行模式固定为 `full_loop`
5. 我后续上传的文件默认进入这条链路：
   `P10/P9审查 → P9派单 → P8执行 → 用户/代理体验 → P9复审 → P10终审/收口`
6. 除非触发高风险停机条件，否则不要再让我手动点名角色或确认下一步
7. 本轮以 `MANIFEST.json + Master Loader + Roles + Protocols` 为唯一有效装配源，禁止混用其他旧入口或旧版本 Skill

## 使用结论

从现在开始，**不要再混用旧入口文件**。
这个总包就是新的唯一基线。
