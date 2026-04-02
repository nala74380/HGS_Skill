#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

REQ = [
    'scripts/assemble_release.py','scripts/verify_release.py','scripts/bootstrap_full_loop_dry_run.py',
    'scripts/render_automation_acceptance_report.py','scripts/validate_release_runtime_integrity.py',
    'scripts/validate_manifest_schema.py','scripts/normalize_issue_input.py','scripts/manifest.schema.json',
    'scripts/README_release_runtime.md','scripts/validate_release_semantic_alignment.py',
    'scripts/experience_memory_engine.py','scripts/validate_route_policy_drift.py','scripts/generate_runtime_route_policy.py','scripts/tool_reasoning_engine.py',
    'scripts/validate_package_cleanliness.py','scripts/validate_display_integrity.py','scripts/build_clean_release_package.py','scripts/dryrun_scoring.py'
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--manifest', default='Release/MANIFEST.json')
    ap.add_argument('--output', default='.hgs/runtime_integrity_report.json')
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    manifest = json.loads((root / args.manifest).read_text(encoding='utf-8'))
    route = manifest.get('automation_policy', {}).get('runtime_route_policy', {})

    role_files = {item['file'] for item in manifest.get('roles', []) if isinstance(item, dict) and 'file' in item}
    tool_files = {item['file'] for item in manifest.get('tools', []) if isinstance(item, dict) and 'file' in item}

    missing_required = [p for p in REQ if not (root / p).exists()]

    supported_issue_types = set(route.get('supported_issue_types', []))
    expected_examples = {f'examples/issue_input_{x}.json' for x in supported_issue_types if x != 'console'} | {'examples/issue_input.json'}
    missing_examples = sorted([p for p in expected_examples if not (root / p).exists()])
    invalid_examples = []
    for p in sorted(expected_examples):
        fp=root/p
        if not fp.exists():
            continue
        try:
            data=json.loads(fp.read_text(encoding='utf-8'))
        except Exception:
            invalid_examples.append({'path': p, 'reason': 'invalid_json'})
            continue
        expected_issue_type = 'console' if p.endswith('issue_input.json') else Path(p).stem.replace('issue_input_', '')
        if data.get('issue_type') != expected_issue_type:
            invalid_examples.append({'path': p, 'reason': 'issue_type_mismatch', 'expected': expected_issue_type, 'actual': data.get('issue_type')})

    missing_owner_refs=[]
    for issue_type, path in route.get('owner_by_issue_type', {}).items():
        if path not in role_files:
            missing_owner_refs.append({'issue_type': issue_type, 'path': path})
    missing_tool_refs=[]
    for bucket_name in ['tools_by_issue_type','tools_by_risk_flag']:
        for bucket, items in route.get(bucket_name, {}).items():
            for path in items:
                if path not in tool_files:
                    missing_tool_refs.append({'bucket_name': bucket_name, 'bucket': bucket, 'path': path})
    for path in route.get('always_include_tools', []):
        if path not in tool_files:
            missing_tool_refs.append({'bucket_name':'always_include_tools','bucket':'always','path': path})
    missing_role_display_names=[item.get('file') for item in manifest.get('roles', []) if isinstance(item, dict) and not item.get('display_name')]
    missing_tool_display_names=[item.get('file') for item in manifest.get('tools', []) if isinstance(item, dict) and not item.get('display_name')]
    missing_protocol_display_names=[item.get('file') for item in manifest.get('protocols', []) if isinstance(item, dict) and not item.get('display_name')]
    missing_role_capability_tags=[item.get('file') for item in manifest.get('roles', []) if isinstance(item, dict) and not item.get('capability_tags')]
    missing_tool_capability_tags=[item.get('file') for item in manifest.get('tools', []) if isinstance(item, dict) and not item.get('capability_tags')]
    report={
        'integrity_status':'pass' if not any([missing_required, missing_examples, invalid_examples, missing_owner_refs, missing_tool_refs, missing_role_display_names, missing_tool_display_names, missing_protocol_display_names, missing_role_capability_tags, missing_tool_capability_tags]) else 'fail',
        'missing_required_files':missing_required,
        'missing_examples':missing_examples,
        'invalid_examples': invalid_examples,
        'missing_owner_refs':missing_owner_refs,
        'missing_tool_refs':missing_tool_refs,
        'missing_role_display_names':missing_role_display_names,
        'missing_tool_display_names':missing_tool_display_names,
        'missing_protocol_display_names':missing_protocol_display_names,
        'missing_role_capability_tags':missing_role_capability_tags,
        'missing_tool_capability_tags':missing_tool_capability_tags,
    }
    out=root/args.output; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if args.strict and report['integrity_status']!='pass' else 0

if __name__ == '__main__':
    raise SystemExit(main())
