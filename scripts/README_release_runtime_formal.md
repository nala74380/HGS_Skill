# Release Runtime Scripts (Formal)

This document defines the **formal** repository-side acceptance chain for the HGS Release package.

## Formal canonical chain

- `scripts/assemble_release.py` ← formal role: Release assembly
- `scripts/verify_release.py` ← formal role: Release acceptance verification
- `scripts/bootstrap_full_loop_dry_run.py` ← formal role: full_loop dry-run bootstrap
- `scripts/render_automation_acceptance_report.py` ← formal role: automation acceptance report rendering

## Current repository note

During transition, stricter implementation files may still exist in the branch history or working branch.
For formal release semantics, treat the following functional responsibilities as canonical:

- assembly
- verification
- full_loop dry-run bootstrap
- automation acceptance rendering
- runtime integrity audit
- matrix CI acceptance

## Canonical local workflow

```bash
python scripts/assemble_release.py --strict
python scripts/verify_release.py --strict
python scripts/bootstrap_full_loop_dry_run.py --issue-input examples/issue_input.json --strict
python scripts/render_automation_acceptance_report.py --strict
```

## Canonical PR workflow

The formal repository acceptance path must include:
- runtime integrity audit
- strict release assembly
- release acceptance verification
- scenario-matrix dry-run bootstrap
- automation acceptance report rendering

## Formal policy

- Do not treat draft helpers as formal release chain.
- Do not introduce `v2 / v3 / enhanced / stronger / strict-plus` naming into formal release surfaces.
- If implementation names temporarily differ in a transition branch, formal docs and CI should still converge to one canonical chain before release.
