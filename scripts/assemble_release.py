#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import dataclass, asdict
from pathlib import Path

README_BASELINE = 'README.md'

@dataclass
class LoadedFile:
    path: str
    category: str
    exists: bool
    loaded: bool
    bytes: int
    sha256: str | None
    error: str | None

def normalize_path(raw: str) -> str:
    raw = raw.strip().lstrip('./')
    return raw if raw.startswith('Release/') else f'Release/{raw}'

def category(path: str) -> str:
    if '/roles/' in path: return 'role'
    if '/tools/' in path: return 'tool'
    if '/protocols/' in path: return 'protocol'
    if '/docs/' in path: return 'doc'
    return 'other'

def sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--manifest', default='Release/MANIFEST.json')
    ap.add_argument('--output', default='.hgs/assembly_ledger.json')
    ap.add_argument('--fail-on-unregistered-release-files', action='store_true')
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    manifest = json.loads((root / args.manifest).read_text(encoding='utf-8'))
    registered = [normalize_path(manifest['entrypoint'])]
    for key in ['load_order', 'tool_load_order', 'documentation_load_order']:
        registered.extend(normalize_path(x) for x in manifest.get(key, []))

    seen, deduped, dup = set(), [], []
    for p in registered:
        if p in seen:
            dup.append(p)
        else:
            seen.add(p); deduped.append(p)

    loaded, missing = [], []
    for p in deduped:
        fp = root / p
        if not fp.exists():
            loaded.append(asdict(LoadedFile(p, category(p), False, False, 0, None, 'file_not_found')))
            missing.append(p)
            continue
        try:
            text = fp.read_text(encoding='utf-8')
            loaded.append(asdict(LoadedFile(p, category(p), True, True, len(text.encode('utf-8')), sha(text), None)))
        except Exception as exc:
            loaded.append(asdict(LoadedFile(p, category(p), True, False, 0, None, str(exc))))
            missing.append(p)

    counts = {'role':0,'tool':0,'protocol':0,'doc':0}
    loaded_counts = {'role':0,'tool':0,'protocol':0,'doc':0}
    for p in deduped:
        c = category(p)
        if c in counts: counts[c]+=1
    for item in loaded:
        c = item['category']
        if c in loaded_counts and item['loaded']: loaded_counts[c]+=1

    release_files = sorted(str(p.as_posix()) for p in (root / 'Release').rglob('*') if p.is_file())
    allowed = set(deduped) | {normalize_path(manifest['entrypoint']), normalize_path(args.manifest)}
    unregistered = sorted([p for p in release_files if p not in allowed])
    release_source_only = all(p.startswith('Release/') for p in deduped) and all(x['path'].startswith('Release/') for x in loaded)
    ok = (not missing) and release_source_only and (not args.fail_on_unregistered_release_files or not unregistered)

    ledger = {
      'package_version': manifest.get('package_version'),
      'entrypoint': manifest.get('entrypoint'),
      'default_route_mode': manifest.get('default_route_mode'),
      'action_protocol': manifest.get('action_protocol'),
      'clearance_protocol': manifest.get('clearance_protocol'),
      'readme_baseline_loaded': (root / README_BASELINE).exists(),
      'release_source_only': release_source_only,
      'roles_expected': counts['role'], 'tools_expected': counts['tool'], 'protocols_expected': counts['protocol'], 'docs_expected': counts['doc'],
      'roles_loaded': loaded_counts['role'], 'tools_loaded': loaded_counts['tool'], 'protocols_loaded': loaded_counts['protocol'], 'docs_loaded': loaded_counts['doc'],
      'active_actions_count': len(manifest.get('active_actions', [])),
      'active_action_batches': list(manifest.get('active_action_batches', [])),
      'risk_gates': list(manifest.get('risk_gates', [])),
      'loaded_files': loaded,
      'missing_files': missing,
      'duplicate_registrations': dup,
      'unregistered_release_files': unregistered,
      'assembly_status': 'pass' if ok else 'fail'
    }
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(ledger, ensure_ascii=False, indent=2))
    return 1 if args.strict and ledger['assembly_status'] != 'pass' else 0

if __name__ == '__main__':
    raise SystemExit(main())
