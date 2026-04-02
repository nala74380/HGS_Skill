#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

ROLE_DOCS = ['Release/docs/角色调用关系总表.md','Release/docs/角色-工具矩阵总表.md','Release/docs/角色边界验证台账.md']
TOOL_DOCS = ['Release/docs/工具调用关系总表.md']
CLEARANCE_DOCS = ['Release/protocols/61_Automation_Orchestration_Protocol.md','Release/protocols/62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md']
SCORING_DOCS = ['Release/docs/HGS_全局检查与清理评分报告.md']
LEDGER_DOCS = ['Release/docs/HGS_全局扣分点问题清单与派单台账.md']

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--ledger', default='.hgs/assembly_ledger.json')
    ap.add_argument('--output', default='.hgs/assembly_report.json')
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    ledger = json.loads((root / args.ledger).read_text(encoding='utf-8'))
    loaded = {x['path'] for x in ledger.get('loaded_files', []) if x.get('loaded')}
    entry = ledger.get('entrypoint','')
    entry = entry if str(entry).startswith('Release/') else f'Release/{entry}'

    def has_all(paths):
        return all(p in loaded for p in paths)

    status = 'pass' if all([
        ledger.get('assembly_status') == 'pass',
        'Release/MANIFEST.json' in loaded,
        entry in loaded,
        ledger.get('roles_loaded') == ledger.get('roles_expected'),
        ledger.get('tools_loaded') == ledger.get('tools_expected'),
        ledger.get('protocols_loaded') == ledger.get('protocols_expected'),
        ledger.get('docs_loaded') == ledger.get('docs_expected'),
        has_all(ROLE_DOCS), has_all(TOOL_DOCS), has_all(CLEARANCE_DOCS), has_all(SCORING_DOCS), has_all(LEDGER_DOCS),
        ledger.get('release_source_only') is True,
        ledger.get('readme_baseline_loaded') is True,
    ]) else 'fail'

    report = {
      'package_version': ledger.get('package_version'),
      'entrypoint': ledger.get('entrypoint'),
      'default_route_mode': ledger.get('default_route_mode'),
      'action_protocol': ledger.get('action_protocol'),
      'clearance_protocol': ledger.get('clearance_protocol'),
      'roles_loaded_count': f"{ledger.get('roles_loaded')} / {ledger.get('roles_expected')}",
      'tools_loaded_count': f"{ledger.get('tools_loaded')} / {ledger.get('tools_expected')}",
      'protocols_loaded_count': f"{ledger.get('protocols_loaded')} / {ledger.get('protocols_expected')}",
      'docs_loaded_count': f"{ledger.get('docs_loaded')} / {ledger.get('docs_expected')}",
      'active_actions_count': ledger.get('active_actions_count'),
      'active_action_batches': ledger.get('active_action_batches', []),
      'risk_gates': ledger.get('risk_gates', []),
      'role_governance_docs_loaded': 'yes' if has_all(ROLE_DOCS) else 'no',
      'tool_governance_docs_loaded': 'yes' if has_all(TOOL_DOCS) else 'no',
      'clearance_docs_loaded': 'yes' if has_all(CLEARANCE_DOCS) else 'no',
      'deduction_ledger_loaded': 'yes' if has_all(LEDGER_DOCS) else 'no',
      'readme_release_baseline_loaded': 'yes' if ledger.get('readme_baseline_loaded') else 'no',
      'release_source_only': 'yes' if ledger.get('release_source_only') else 'no',
      'full_release_assembly_status': status,
      'missing_files': ledger.get('missing_files', []),
      'duplicate_registrations': ledger.get('duplicate_registrations', []),
      'unregistered_release_files': ledger.get('unregistered_release_files', [])
    }
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and status != 'pass' else 0

if __name__ == '__main__':
    raise SystemExit(main())
