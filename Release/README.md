# HGS 正式发布版

这是把“纯净包”重构为 **Master Loader + Roles + Manifest** 的正式发布结构。

## 目录

- `MANIFEST.json`：唯一装配清单与加载顺序
- `00_HGS_Master_Loader.md`：唯一启动入口
- `roles/`：角色 Skill
- `protocols/`：体验 / 再审 / I/O 协议
- `docs/`：审查报告与发布说明

## 使用原则

1. 运行时不是只读一个入口，而是**按 Manifest 装配全角色**
2. 角色文件保留独立职责，避免被主入口吞没
3. 所有产物格式以 `protocols/60_HGS_IO_Protocol.md` 为准
4. 主装配器只负责流程、路由、停机条件与状态机，不替代角色本体

## 建议加载口令

```text
读取 MANIFEST.json，并按其中 load_order 装配 HGS 正式发布版：
- 入口：00_HGS_Master_Loader.md
- 角色：roles/ 下全部文件
- 协议：protocols/ 下全部文件
执行模式：full_loop
后续我上传的文件默认进入全链路自动处理，命中停机条件时显式停下。
```

## 包内角色

- P10：战略裁剪
- P9：审查 / 派单 / 复审
- P8 Enhanced：兜底接管
- P8 Backend / Frontend / PCConsole / LanrenJingling / Agent / EndUser：专项执行
- Agent / EndUser Experience：体验证据采集
- Re-Review：收口前再审
- HGS I/O Protocol：统一产物协议
