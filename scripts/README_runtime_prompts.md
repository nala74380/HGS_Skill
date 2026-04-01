# Optimized Loading Prompts for HGS Release

## Recommendation
Yes — the loading prompt should be optimized.

Why:
- the Release package is now manifest-driven
- the repository has strict runtime scripts and CI gates
- repeated long prompts are noisier and easier to drift

## Prompt A: canonical full conversational load

```text
读取并加载 HGS GitHub 正式发布版，作为本轮唯一生效装配源：

1. 读取 `Release/MANIFEST.json`
2. 读取 `Release/00_HGS_Master_Loader.md`
3. 按 manifest 的 `load_order`、`tool_load_order`、`documentation_load_order` 全量装配已登记的 `roles/`、`tools/`、`protocols/`、`docs/`
4. 执行模式固定为 `full_loop`
5. 只承认 `Release/` 下且已登记在 `MANIFEST.json` 中的文件为有效 Skill 源
6. 默认链路：真相Owner识别 → P9审查派单 → P8执行 → 用户/代理体验 + QA/SRE验证 → P9复审 → P10终审/按需收口 → Docs沉淀 → Closeout
7. 除非命中 `risk_gates` 或高风险停机条件，否则不要退回建议模式，不要让我手动点名角色，不要让我选方案
```

## Prompt B: shorter operational load

```text
按 `Release/MANIFEST.json` + `Release/00_HGS_Master_Loader.md` 重载 HGS 正式发布链。
要求：
- 只认 `Release/` + manifest 已登记文件
- 全量装配 `roles/tools/protocols/docs`
- 模式固定 `full_loop`
- 默认自动链：真相Owner → P9 → P8 → 体验/QA/SRE → P9复审 → P10按需 → Docs → Closeout
- 非命中 `risk_gates` 不回退建议模式、不让我手动选方案
```

## Prompt C: repository-side strict acceptance mode

Use this when the target environment can run repository-side scripts:

```text
基于仓库 strict 运行链执行 HGS Release 验收：
- `scripts/assemble_release_strict_v2.py`
- `scripts/verify_release_strict.py`
- `scripts/bootstrap_full_loop_dry_run_strict_v2.py`
- `scripts/render_automation_acceptance_report_strict.py`
若脚本产物与对话装配结果冲突，以 strict 产物为准。
```

## Guidance

- Prompt A: best when you need full explicitness in chat.
- Prompt B: best when the environment already understands the Release baseline.
- Prompt C: best when repository-side strict scripts are available and should be treated as source-of-truth for acceptance.
