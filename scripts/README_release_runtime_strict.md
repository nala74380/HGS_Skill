# Release Runtime Scripts (Strict)

This document defines the **strict** repository-side acceptance path for the HGS Release package.

## Canonical scripts

- `scripts/assemble_release_strict.py`
- `scripts/verify_release_strict.py`
- `scripts/bootstrap_full_loop_dry_run_strict.py`
- `scripts/render_automation_acceptance_report_strict.py`

These scripts supersede the earlier draft runtime helpers when you need:
- strict release-source checks
- README baseline checks
- score-based dry-run decisions
- CI/PR gate enforcement

## Canonical local workflow

```bash
python scripts/assemble_release_strict.py --strict
python scripts/verify_release_strict.py --strict
python scripts/bootstrap_full_loop_dry_run_strict.py --issue-input examples/issue_input.json --strict
python scripts/render_automation_acceptance_report_strict.py --strict
```

## Canonical PR workflow

The repository CI workflow is:

- `.github/workflows/release-runtime-acceptance.yml`

It runs the same four strict steps on pull requests touching:
- `Release/**`
- `scripts/**`
- `examples/**`
- `README.md`

## Produced artifacts

- `.hgs/assembly_ledger.json`
- `.hgs/assembly_report.json`
- `.hgs/full_loop_dry_run.json`
- `.hgs/automation_execution_acceptance_report.json`

## Notes

- The strict dry-run still does **not** execute fixes. It only proves whether the full-loop bootstrap can start with sufficient structure and evidence.
- The strict acceptance renderer derives judgement fields from dry-run content instead of hardcoding pass-like answers.
- If you want the PR to fail on assembly or dry-run problems, use the strict scripts and rely on the GitHub Actions workflow.
