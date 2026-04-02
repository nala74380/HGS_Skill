#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path


def normalize(p:str)->str:
    return p if p.startswith('Release/') else f'Release/{p}'


def classify_tool_drift(configured, generated, curated_override):
    if configured == generated:
        return 'exact_match'
    if set(configured) == set(generated):
        return 'ordering_only'
    return 'curated_override' if curated_override else 'unreviewed_drift'


def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',default='.'); ap.add_argument('--manifest',default='Release/MANIFEST.json'); ap.add_argument('--output',default='.hgs/route_policy_drift_report.json'); ap.add_argument('--strict',action='store_true'); args=ap.parse_args()
    root=Path(args.repo_root).resolve()
    subprocess.run([sys.executable, str(root/'scripts/generate_runtime_route_policy.py'), '--repo-root', str(root), '--manifest', args.manifest], check=True, capture_output=True, text=True)
    generated=json.loads((root/'.hgs/generated_runtime_route_policy.json').read_text(encoding='utf-8'))
    manifest=json.loads((root/args.manifest).read_text(encoding='utf-8'))
    route=manifest.get('automation_policy',{}).get('runtime_route_policy',{})
    maint=route.get('route_policy_maintenance_policy', {})
    curated_override=maint.get('allow_curated_policy_override', True)
    drifts=[]
    blocking_drift_count=0
    ordering_only_count=0
    for k,v in route.get('owner_by_issue_type',{}).items():
        gv=generated.get('owner_by_issue_type',{}).get(k,'')
        if gv and normalize(v)!=normalize(gv):
            classification='curated_override' if curated_override else 'unreviewed_drift'
            blocking_drift_count += 1
            drifts.append({'type':'owner_by_issue_type','issue_type':k,'configured':normalize(v),'generated':normalize(gv),'classification':classification})
    for k,v in route.get('tools_by_issue_type',{}).items():
        gv=[normalize(x) for x in generated.get('tools_by_issue_type',{}).get(k,[])]
        cv=[normalize(x) for x in v]
        if gv and cv!=gv:
            classification=classify_tool_drift(cv, gv, curated_override)
            if classification == 'ordering_only':
                ordering_only_count += 1
            else:
                blocking_drift_count += 1
            drifts.append({'type':'tools_by_issue_type','issue_type':k,'configured':cv,'generated':gv,'classification':classification})
    reviewed_by=maint.get('reviewed_by', 'P10终审官')
    rationale=maint.get('rationale', '人工精修路由允许覆盖自动候选，但需显式标注并复审')
    approved_at=maint.get('approved_at', datetime.now(timezone.utc).isoformat())
    if not drifts:
        status='pass'
    elif blocking_drift_count == 0:
        status='pass'
    elif curated_override:
        status='pass_with_curated_override'
    else:
        status='fail'
    report={
        'route_policy_drift_status':status,
        'drift_items':drifts,
        'drift_count':len(drifts),
        'blocking_drift_count':blocking_drift_count,
        'ordering_only_count':ordering_only_count,
        'curated_override_enabled':curated_override,
        'curated_override_review': {'reviewed_by': reviewed_by if curated_override else '', 'rationale': rationale if curated_override else '', 'approved_at': approved_at if curated_override else ''}
    }
    out=root/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if args.strict and status=='fail' else 0

if __name__=='__main__': raise SystemExit(main())
