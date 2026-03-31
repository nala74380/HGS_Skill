# HGS 纯净联动版总包

这是按“**直接删除废弃、取消兼容、只保留正式版本**”原则重做的总包。

## 本包特点

- 只有 **1 个总入口**：`HGS_AutoLoop_Master_SKILL.md`
- 不保留任何兼容包装文件
- 不保留任何废弃入口
- 不保留重复版本号文件名
- 角色文件全部收敛为单一正式版
- 对 P9 / P8 Enhanced / 各专项 P8 做了逐份审查后合并，避免“新版有协议、旧版有细节”的断层

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

## 删除原则

原附件中的以下类型已全部删除，不进入本包：

- 重复总入口
- 兼容层 / 跳转层
- 废弃分析稿 / 合并说明稿
- 同名多版本并存文件
- 只描述“怎么替换旧包”的过渡材料

## 使用结论

从现在开始，**不要再混用旧入口文件**。
这个总包就是新的唯一基线。
