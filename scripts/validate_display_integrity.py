#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

EXPECTED_HEADER = "自动化链路：已开启"
EXPECTED_FORENSIC_TEXT = "全审计"
REQUIRED_NONEMPTY_KEYS = [
    "response_header",
    "owner_name",
    "p8_executor_skill",
    "ticket_id",
    "problem_statement",
    "display_mode_text",
]


def check_payload(name: str, payload: dict, errors: list[str]) -> None:
    if payload.get("response_header") != EXPECTED_HEADER:
        errors.append(f"{name}.response_header must equal 自动化链路：已开启")
    for key in REQUIRED_NONEMPTY_KEYS:
        if not str(payload.get(key, "")).strip():
            errors.append(f"{name}.{key} must be non-empty")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--dryrun', default='.hgs/full_loop_dry_run.json')
    ap.add_argument('--acceptance', default='.hgs/automation_execution_acceptance_report.json')
    ap.add_argument('--output', default='.hgs/display_integrity_report.json')
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    dry = json.loads((root / args.dryrun).read_text(encoding='utf-8'))
    acc = json.loads((root / args.acceptance).read_text(encoding='utf-8'))

    errors: list[str] = []
    check_payload('dryrun', dry, errors)
    check_payload('acceptance', acc, errors)

    if not dry.get('current_work_display'):
        errors.append('dryrun.current_work_display must be non-empty')
    if not acc.get('actor_action_trace'):
        errors.append('acceptance.actor_action_trace must be non-empty')
    if dry.get('display_mode') == 'forensic':
        if dry.get('display_mode_text') != EXPECTED_FORENSIC_TEXT:
            errors.append('forensic display mode must expose display_mode_text=全审计')
        if not dry.get('p9_dispatch_checklist', {}).get('linked_files_to_modify', []):
            errors.append('forensic display mode requires linked files')
        if not dry.get('issue_priority_ranking', []):
            errors.append('forensic display mode requires issue ranking')
        if 'remaining_issues' not in dry.get('review_result', {}):
            errors.append('forensic display mode requires review remaining issues key')

    status = 'pass' if not errors else 'fail'
    report = {'display_integrity_status': status, 'errors': errors}
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and status != 'pass' else 0


if __name__ == '__main__':
    raise SystemExit(main())
