#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

EXCLUDE_PARTS={'.hgs','hgs','.pytest_cache','__pycache__'}
EXCLUDE_FILES={'.DS_Store'}
REQUIRED_ROOT_MARKERS={'Release','scripts','tests','README.md'}


def include(path:Path, root:Path)->bool:
    rel=path.relative_to(root)
    if any(part in EXCLUDE_PARTS for part in rel.parts):
        return False
    if path.name in EXCLUDE_FILES:
        return False
    return True


def validate_repo_root(root: Path) -> list[str]:
    missing=[]
    for marker in REQUIRED_ROOT_MARKERS:
        if not (root/marker).exists():
            missing.append(marker)
    return missing


def audit_zip(out: Path) -> dict:
    forbidden=[]
    with zipfile.ZipFile(out, 'r') as zf:
        members=zf.namelist()
        for name in members:
            parts=Path(name).parts
            if any(part in EXCLUDE_PARTS for part in parts):
                forbidden.append(name)
    return {'entry_count': len(members), 'forbidden_entries': sorted(forbidden)}


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root',default='.')
    ap.add_argument('--output-zip',default='HGS_Skill_release_clean.zip')
    ap.add_argument('--audit-output',default='.hgs/clean_package_build_audit.json')
    args=ap.parse_args()
    root=Path(args.repo_root).resolve()
    out=Path(args.output_zip).resolve()
    missing_markers=validate_repo_root(root)
    if missing_markers:
        raise SystemExit(f'invalid repo root: missing {missing_markers}')
    if out.exists():
        out.unlink()
    included=[]
    excluded=[]
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob('*')):
            if not path.is_file():
                continue
            rel=str(path.relative_to(root))
            if include(path, root):
                zf.write(path, path.relative_to(root))
                included.append(rel)
            else:
                excluded.append(rel)
    zip_audit=audit_zip(out)
    audit={
        'repo_root': str(root),
        'output_zip': str(out),
        'missing_root_markers': missing_markers,
        'included_file_count': len(included),
        'excluded_file_count': len(excluded),
        'excluded_examples': excluded[:50],
        'zip_audit': zip_audit,
    }
    audit_path=root/args.audit_output
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    print(str(out))
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return 1 if zip_audit['forbidden_entries'] else 0


if __name__=='__main__':
    raise SystemExit(main())
