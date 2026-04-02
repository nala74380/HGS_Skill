# Release Runtime Scripts

正式发布只使用这一条仓库侧运行链：

- `scripts/assemble_release.py`
- `scripts/verify_release.py`
- `scripts/bootstrap_full_loop_dry_run.py`
- `scripts/render_automation_acceptance_report.py`
- `scripts/validate_release_runtime_integrity.py`

本链用于：
- Release 批量装配
- Release 验收
- full_loop dry-run 启动
- 自动化执行验收报告渲染
- 运行链一致性审计

本仓库正式发布面不再区分 draft / strict / v2。

- `scripts/normalize_issue_input.py`
- `scripts/validate_release_semantic_alignment.py`


正式中文显示名已写入 `Release/MANIFEST.json`，正式链会优先显示中文 Skill 名称与派单目标 Skill 名称。


显示策略：正式对话与正式产物中的显示名仅显示中文名，不并列显示英文文件名。


评分轴：正式链现在输出独立评分轴（探索广度、反主假设严格度、先行动后追问严格度、收敛质量、执行就绪度、用户适配度、结果充分性）与 overall_quality_score。


新增正式能力：
- scripts/generate_runtime_route_policy.py：根据角色/工具目录自动生成候选路由策略
- scripts/validate_route_policy_drift.py：检查正式路由策略与自动生成候选之间的漂移
- scripts/tool_reasoning_engine.py：基于工具全文做高保真推理执行
- scripts/validate_release_semantic_alignment.py：基于全文语义做一致性审计


## 经验记忆层

正式链已接入 `scripts/experience_memory_engine.py`，用于输出经验支持轨 / 经验挑战轨 / 经验失效态，作为偏置提示而非裁决。


## Release cleanliness gate

正式发布前必须区分两类检查对象，禁止再混用：

### A. 原始压缩包本体洁净检查
只检查 zip 文件本体，不解包、不执行任何脚本：

```bash
python scripts/validate_archive_cleanliness.py --zip-path HGS_Skill_release_clean.zip --strict
```

### B. 解包后运行环境洁净检查
检查解包后、执行后工作目录是否被产物污染：

```bash
python scripts/validate_package_cleanliness.py --strict
```

### C. 发布前总闸门
如需同时校验运行环境与发布压缩包，执行：

```bash
python scripts/release_cleanliness_gate.py --strict
```

### D. 构建正式净包
```bash
python scripts/build_clean_release_package.py --output-zip HGS_Skill_release_clean.zip
```

- 原始压缩包本体洁净性 ≠ 运行后工作目录洁净性
- 发布包必须只保留一套正式源码与配置
- 不允许包含 `.hgs/`、`hgs/`、`.pytest_cache/`、`__pycache__/`、`*.pyc`
- 必须保留 `.gitignore`、`.gitattributes`、`.github/workflows/`

## Adversarial review gate

正式发布前，必须额外检查：
- 假全绿 pass
- curated override 吞问题
- 显示字段为空
- 产物目录并存
- 启发式 confidence 过高
- dotfile / dotdir 丢失


## 显示颗粒度口令开关

正式链支持显示颗粒度切换：

- `显示：简版` / `display:compact`
- `显示：标准` / `display:standard`
- `显示：全审计` / `display:forensic`
- `显示：关闭` / `display:off`

默认使用 `forensic`，对外显示必须包含：链路阶段、角色中文名、当前单号、问题标题、优先级、阻断点、联动文件、联动记录与复审结论。

## 清零控制主旋律

清零收口不是尾声阶段，而是贯穿执行全程的主控制链。

- 持续审核
- 持续派单
- 持续回单
- 持续挂单治理

只要仍存在未清零主线问题、未解释的复审失败、未登记挂单，就禁止 closeout。


## 固定显示头
- response_header 必须固定为 `自动化链路：已开启`
- forensic 模式对外固定显示 `显示模式：全审计`
- display_mode_text 字段必须输出中文显示值，供对话层与验收层一致使用
