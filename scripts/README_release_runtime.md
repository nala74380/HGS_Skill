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
