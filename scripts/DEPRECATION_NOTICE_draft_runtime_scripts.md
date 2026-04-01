# Deprecation Notice: Draft Runtime Scripts

The following draft runtime helpers remain in the repository for historical comparison only:

- `scripts/assemble_release.py`
- `scripts/verify_release.py`
- `scripts/bootstrap_full_loop_dry_run.py`
- `scripts/render_automation_acceptance_report.py`

## Status

These files are **deprecated for acceptance-critical use**.

## Canonical replacements

Use these strict/canonical files instead:

- `scripts/assemble_release_strict_v2.py`
- `scripts/verify_release_strict.py`
- `scripts/bootstrap_full_loop_dry_run_strict_v2.py`
- `scripts/render_automation_acceptance_report_strict.py`

## Reason

The strict/canonical chain adds:
- factual `release_source_only` checks
- README baseline enforcement
- external routing registry support
- scenario-matrix CI coverage
- explicit `user_choice_required` / `suggestion_mode` fields
- stronger score/routing/blocking outputs for automation acceptance

## Policy

For PR gate, release acceptance, and dry-run acceptance, treat the strict/canonical chain as source-of-truth.
