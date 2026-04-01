#!/usr/bin/env python3
"""Validate Release runtime integrity across manifest, route registry, and strict scripts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_STRICT_FILES = [
    'scripts/assemble_release_strict_v2.py',
    'scripts/verify_release_strict.py',
    'scripts/bootstrap_full_loop_dry_run_strict_v2.py',
    'scripts/render_automation_acceptance_report_strict.py',
    'scripts/runtime_route_registry.json',
]

EXAMPLE_SCENARIOS = [
    'examples/issue_input.json',
    'examples/issue_input_rule.json',
    'examples/issue_input_billing.json',
    'examples/issue_input_worker_incident.json',
    'examples/issue_input_mixed.json',
]


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate Release runtime integrity')
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--manifest', default='Release/MANIFEST.json')
    parser.add_argument('--route-registry', default='scripts/runtime_route_registry.json')
    parser.add_argument('--output', default='.hgs/runtime_integrity_report.json')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest = load_json(repo_root / args.manifest)
    route_registry = load_json(repo_root / args.route_registry)

    load_order = set(('Release/' + p.lstrip('./').removeprefix('Release/')) for p in manifest.get('load_order', []))
    tool_load_order = set(('Release/' + p.lstrip('./').removeprefix('Release/')) for p in manifest.get('tool_load_order', []))

    role_basenames = {Path(p).name for p in load_order if '/roles/' in p}
    tool_basenames = {Path(p).name for p in tool_load_order if '/tools/' in p}

    owner_registry_values = set(route_registry.get('owner_basename_map', {}).values())
    tool_registry_values = set()
    for items in route_registry.get('tool_basename_map', {}).values():
        tool_registry_values.update(items)
    for items in route_registry.get('risk_flag_tool_map', {}).values():
        tool_registry_values.update(items)
    tool_registry_values.update(route_registry.get('always_include_tools', []))

    missing_owner_refs = sorted(owner_registry_values - role_basenames)
    missing_tool_refs = sorted(tool_registry_values - tool_basenames)

    missing_required_files = sorted([p for p in REQUIRED_STRICT_FILES if not (repo_root / p).exists()])
    missing_examples = sorted([p for p in EXAMPLE_SCENARIOS if not (repo_root / p).exists()])

    report = {
        'manifest_package_version': manifest.get('package_version'),
        'route_registry_version': route_registry.get('registry_version'),
        'missing_owner_refs': missing_owner_refs,
        'missing_tool_refs': missing_tool_refs,
        'missing_required_files': missing_required_files,
        'missing_examples': missing_examples,
        'integrity_status': 'pass' if not any([missing_owner_refs, missing_tool_refs, missing_required_files, missing_examples]) else 'fail'
    }

    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and report['integrity_status'] != 'pass' else 0

if __name__ == '__main__':
    raise SystemExit(main())
