#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

FORBIDDEN_DIR_NAMES = {'.hgs', 'hgs', '.pytest_cache', '__pycache__'}
FORBIDDEN_SUFFIXES = {'.pyc'}
REQUIRED_PATHS = ['.gitignore', '.gitattributes', '.github/workflows/release-runtime-acceptance.yml']


def audit_runtime_workspace(root: Path) -> dict:
    forbidden: list[str] = []
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(part in FORBIDDEN_DIR_NAMES for part in rel.parts):
            forbidden.append(str(rel))
            continue
        if path.is_file() and path.suffix in FORBIDDEN_SUFFIXES:
            forbidden.append(str(rel))
    missing = [p for p in REQUIRED_PATHS if not (root / p).exists()]
    duplicated_artifact_roots = ['.hgs', 'hgs'] if (root / '.hgs').exists() and (root / 'hgs').exists() else []
    status = 'pass' if not forbidden and not missing and not duplicated_artifact_roots else 'fail'
    return {
        'cleanliness_scope': 'runtime_workspace_after_extraction_or_execution',
        'runtime_workspace_cleanliness_status': status,
        'package_cleanliness_status': status,
        'forbidden_paths': sorted(forbidden),
        'missing_required_paths': missing,
        'duplicated_artifact_roots': duplicated_artifact_roots,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--output', default='package_cleanliness_report.json')
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    report = audit_runtime_workspace(root)
    out = Path(args.output)
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and report['runtime_workspace_cleanliness_status'] != 'pass' else 0


if __name__ == '__main__':
    raise SystemExit(main())
