#!/usr/bin/env python3
"""Strict v2 batch assembly for the HGS Release package."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

README_BASELINE = "README.md"

@dataclass
class LoadedFile:
    path: str
    category: str
    exists: bool
    loaded: bool
    bytes: int
    sha256: str | None
    error: str | None

@dataclass
class AssemblyLedger:
    package_version: str
    entrypoint: str
    default_route_mode: str
    action_protocol: str | None
    clearance_protocol: str | None
    manifest_path: str
    readme_baseline_loaded: bool
    registered_paths_all_within_release: bool
    loaded_paths_all_within_release: bool
    release_source_only: bool
    fail_on_unregistered_release_files: bool
    roles_expected: int
    tools_expected: int
    protocols_expected: int
    docs_expected: int
    roles_loaded: int
    tools_loaded: int
    protocols_loaded: int
    docs_loaded: int
    active_actions_count: int
    active_action_batches: List[str]
    risk_gates: List[str]
    loaded_files: List[Dict[str, Any]]
    missing_files: List[str]
    duplicate_registrations: List[str]
    out_of_release_registered_paths: List[str]
    unregistered_release_files: List[str]
    assembly_status: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def normalize_registered_path(raw_path: str) -> str:
    raw_path = raw_path.strip().lstrip('./')
    return raw_path if raw_path.startswith('Release/') else f'Release/{raw_path}'


def categorize_registered_path(path: str) -> str:
    if '/roles/' in path: return 'role'
    if '/tools/' in path: return 'tool'
    if '/protocols/' in path: return 'protocol'
    if '/docs/' in path: return 'doc'
    if path.endswith('MANIFEST.json') or path.endswith('00_HGS_Master_Loader.md'): return 'entry'
    return 'other'


def list_release_files(release_root: Path) -> List[str]:
    return sorted(str(p.as_posix()) for p in release_root.rglob('*') if p.is_file())


def load_registered_files(repo_root: Path, registered_paths: List[str]) -> Tuple[List[LoadedFile], List[str]]:
    loaded, missing = [], []
    for path_str in registered_paths:
        path = repo_root / path_str
        category = categorize_registered_path(path_str)
        if not path.exists():
            loaded.append(LoadedFile(path_str, category, False, False, 0, None, 'file_not_found'))
            missing.append(path_str)
            continue
        try:
            content = read_text(path)
            loaded.append(LoadedFile(path_str, category, True, True, len(content.encode('utf-8')), sha256_text(content), None))
        except Exception as exc:
            loaded.append(LoadedFile(path_str, category, True, False, 0, None, str(exc)))
            missing.append(path_str)
    return loaded, missing


def compute_expected_counts(registered_paths: List[str]) -> Dict[str, int]:
    counts = {'role': 0, 'tool': 0, 'protocol': 0, 'doc': 0}
    for p in registered_paths:
        cat = categorize_registered_path(p)
        if cat in counts:
            counts[cat] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description='Strict v2 HGS Release assembly')
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--manifest', default='Release/MANIFEST.json')
    parser.add_argument('--output', default='.hgs/assembly_ledger.json')
    parser.add_argument('--fail-on-unregistered-release-files', action='store_true')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest_path = repo_root / args.manifest
    manifest = json.loads(read_text(manifest_path))

    entrypoint = normalize_registered_path(manifest['entrypoint'])
    load_order = [normalize_registered_path(p) for p in manifest.get('load_order', [])]
    tool_load_order = [normalize_registered_path(p) for p in manifest.get('tool_load_order', [])]
    documentation_load_order = [normalize_registered_path(p) for p in manifest.get('documentation_load_order', [])]
    registered_paths = [entrypoint] + load_order + tool_load_order + documentation_load_order

    seen, deduped, duplicates = set(), [], []
    for p in registered_paths:
        if p in seen:
            duplicates.append(p)
            continue
        seen.add(p)
        deduped.append(p)

    out_of_release_registered_paths = [p for p in deduped if not p.startswith('Release/')]
    registered_paths_all_within_release = not out_of_release_registered_paths
    loaded_files, missing_files = load_registered_files(repo_root, deduped)
    counts = compute_expected_counts(deduped)
    loaded_paths_all_within_release = all(item.path.startswith('Release/') for item in loaded_files)
    all_release_files = list_release_files(repo_root / 'Release')
    allowed = set(deduped) | {normalize_registered_path(manifest['entrypoint']), normalize_registered_path(args.manifest)}
    unregistered_release_files = sorted([p for p in all_release_files if p not in allowed])
    release_source_only = registered_paths_all_within_release and loaded_paths_all_within_release

    assembly_ok = not missing_files and release_source_only and (not args.fail_on_unregistered_release_files or not unregistered_release_files)
    ledger = AssemblyLedger(
        package_version=manifest.get('package_version', 'unknown'),
        entrypoint=manifest.get('entrypoint', ''),
        default_route_mode=manifest.get('default_route_mode', 'unknown'),
        action_protocol=manifest.get('action_protocol'),
        clearance_protocol=manifest.get('clearance_protocol'),
        manifest_path=args.manifest,
        readme_baseline_loaded=(repo_root / README_BASELINE).exists(),
        registered_paths_all_within_release=registered_paths_all_within_release,
        loaded_paths_all_within_release=loaded_paths_all_within_release,
        release_source_only=release_source_only,
        fail_on_unregistered_release_files=args.fail_on_unregistered_release_files,
        roles_expected=counts['role'], tools_expected=counts['tool'], protocols_expected=counts['protocol'], docs_expected=counts['doc'],
        roles_loaded=sum(1 for x in loaded_files if x.category == 'role' and x.loaded),
        tools_loaded=sum(1 for x in loaded_files if x.category == 'tool' and x.loaded),
        protocols_loaded=sum(1 for x in loaded_files if x.category == 'protocol' and x.loaded),
        docs_loaded=sum(1 for x in loaded_files if x.category == 'doc' and x.loaded),
        active_actions_count=len(manifest.get('active_actions', [])),
        active_action_batches=list(manifest.get('active_action_batches', [])),
        risk_gates=list(manifest.get('risk_gates', [])),
        loaded_files=[asdict(x) for x in loaded_files],
        missing_files=missing_files,
        duplicate_registrations=duplicates,
        out_of_release_registered_paths=out_of_release_registered_paths,
        unregistered_release_files=unregistered_release_files,
        assembly_status='pass' if assembly_ok else 'fail',
    )

    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(asdict(ledger), ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(asdict(ledger), ensure_ascii=False, indent=2))
    return 1 if args.strict and ledger.assembly_status != 'pass' else 0

if __name__ == '__main__':
    raise SystemExit(main())
