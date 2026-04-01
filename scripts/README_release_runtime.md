# Release Runtime Scripts

This folder contains repository-side runtime helpers for the HGS Release package.

## Scripts

### 1. `assemble_release.py`
Batch-loads the Release package from `Release/MANIFEST.json`.

What it does:
- reads `Release/MANIFEST.json`
- expands `load_order`, `tool_load_order`, `documentation_load_order`
- loads all registered files in one pass
- emits `.hgs/assembly_ledger.json`

Run:
```bash
python scripts/assemble_release.py --strict
```

### 2. `verify_release.py`
Verifies assembly acceptance from the ledger.

What it does:
- checks loaded counts for roles / tools / protocols / docs
- checks required governance docs and clearance docs
- checks scoring report and deduction ledger
- emits `.hgs/assembly_report.json`

Run:
```bash
python scripts/verify_release.py --strict
```

### 3. `bootstrap_full_loop_dry_run.py`
Bootstraps a full-loop dry-run once release assembly is verified.

What it does:
- requires `full_release_assembly_status = pass`
- reads an issue input JSON
- creates issue stub / owner / required tools / gate plan / exec plan / validation plan / clearance loop
- emits `.hgs/full_loop_dry_run.json`

Run:
```bash
python scripts/bootstrap_full_loop_dry_run.py --issue-input examples/issue_input.json --strict
```

### 4. `render_automation_acceptance_report.py`
Renders a fixed-format automation acceptance report from the dry-run output.

What it does:
- reads `.hgs/full_loop_dry_run.json`
- emits `.hgs/automation_execution_acceptance_report.json`
- aligns output fields with the acceptance format used in HGS dry-run checks

Run:
```bash
python scripts/render_automation_acceptance_report.py --strict
```

## Intended end-to-end workflow

```bash
python scripts/assemble_release.py --strict
python scripts/verify_release.py --strict
python scripts/bootstrap_full_loop_dry_run.py --issue-input examples/issue_input.json --strict
python scripts/render_automation_acceptance_report.py --strict
```

## Expected outputs

- `.hgs/assembly_ledger.json`
- `.hgs/assembly_report.json`
- `.hgs/full_loop_dry_run.json`
- `.hgs/automation_execution_acceptance_report.json`

## Notes

- These scripts are repository-side runtime helpers, not replacements for role / tool / protocol content.
- `bootstrap_full_loop_dry_run.py` is a **dry-run** only. It does not execute fixes.
- `render_automation_acceptance_report.py` converts dry-run artifacts into a structured acceptance-report shape.
