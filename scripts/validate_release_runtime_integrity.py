#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

REQ = ['scripts/assemble_release.py','scripts/verify_release.py','scripts/bootstrap_full_loop_dry_run.py','scripts/validate_release_runtime_integrity.py','scripts/README_release_runtime.md']
EX = ['examples/issue_input.json']

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',default='.'); ap.add_argument('--output',default='.hgs/runtime_integrity_report.json'); ap.add_argument('--strict',action='store_true'); args=ap.parse_args()
    root=Path(args.repo_root).resolve()
    missing_required=[p for p in REQ if not (root/p).exists()]
    missing_examples=[p for p in EX if not (root/p).exists()]
    report={'integrity_status':'pass' if not missing_required and not missing_examples else 'fail','missing_required_files':missing_required,'missing_examples':missing_examples}
    out=root/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(report,ensure_ascii=False,indent=2)); return 1 if args.strict and report['integrity_status']!='pass' else 0

if __name__=='__main__': raise SystemExit(main())
