#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

FORBIDDEN_DIR_NAMES = {'.hgs', 'hgs', '.pytest_cache', '__pycache__'}
FORBIDDEN_SUFFIXES = {'.pyc'}
REQUIRED_PATHS = ['.gitignore', '.gitattributes', '.github/workflows/release-runtime-acceptance.yml']


def audit_archive(zip_path: Path) -> dict:
    forbidden: list[str] = []
    with zipfile.ZipFile(zip_path, 'r') as zf:
        names = zf.namelist()
        for name in names:
            parts = Path(name).parts
            if any(part in FORBIDDEN_DIR_NAMES for part in parts):
                forbidden.append(name)
                continue
            if Path(name).suffix in FORBIDDEN_SUFFIXES:
                forbidden.append(name)
    missing = [p for p in REQUIRED_PATHS if p not in names]
    has_dot_hgs = any(Path(n).parts and Path(n).parts[0] == '.hgs' for n in names)
    has_hgs = any(Path(n).parts and Path(n).parts[0] == 'hgs' for n in names)
    duplicated_artifact_roots = ['.hgs', 'hgs'] if has_dot_hgs and has_hgs else []
    status = 'pass' if not forbidden and not missing and not duplicated_artifact_roots else 'fail'
    return {
        'cleanliness_scope': 'clean_release_archive',
        'archive_cleanliness_status': status,
        'zip_path': str(zip_path),
        'entry_count': len(names),
        'forbidden_entries': sorted(forbidden),
        'missing_required_paths': missing,
        'duplicated_artifact_roots': duplicated_artifact_roots,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--zip-path', required=True)
    ap.add_argument('--output', default='archive_cleanliness_report.json')
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()

    report = audit_archive(Path(args.zip_path).resolve())
    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and report['archive_cleanliness_status'] != 'pass' else 0


if __name__ == '__main__':
    raise SystemExit(main())
