#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from validate_archive_cleanliness import audit_archive
from validate_package_cleanliness import audit_runtime_workspace


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--zip-path', default='')
    ap.add_argument('--output', default='release_cleanliness_gate_report.json')
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    runtime_report = audit_runtime_workspace(root)

    if args.zip_path:
        archive_report = audit_archive(Path(args.zip_path).resolve())
        archive_source = str(Path(args.zip_path).resolve())
    else:
        with tempfile.TemporaryDirectory() as td:
            built = Path(td) / 'HGS_Skill_release_clean_gate.zip'
            subprocess.run([
                sys.executable,
                str(root / 'scripts' / 'build_clean_release_package.py'),
                '--repo-root', str(root),
                '--output-zip', str(built),
                '--audit-output', 'build/clean_package_build_audit.json',
            ], check=True)
            archive_report = audit_archive(built)
            archive_source = 'built_from_repo_root'

    status = 'pass' if runtime_report['runtime_workspace_cleanliness_status'] == 'pass' and archive_report['archive_cleanliness_status'] == 'pass' else 'fail'
    report = {
        'release_cleanliness_gate_status': status,
        'runtime_workspace_report': runtime_report,
        'archive_report': archive_report,
        'archive_source': archive_source,
    }
    out = Path(args.output)
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and status != 'pass' else 0


if __name__ == '__main__':
    raise SystemExit(main())
