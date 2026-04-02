#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ISSUE_HINTS={
  'auth':['auth','jwt','session','identity','stepup','认证','身份','会话'],
  'billing':['billing','quota','freeze','ledger','usage','计费','配额','账本','冻结'],
  'release':['release','compatibility','config','发布','兼容','配置'],
  'frontend':['frontend','ui','surface','api','前端','界面'],
  'console':['console','context','stepup','auth','控制台','上下文'],
  'worker':['worker','heartbeat','runtime','trace','运行时','心跳'],
  'rule':['rule','state','matrix','规则','状态'],
  'security':['security','guard','audit','bypass','风险','安全','授权','审计'],
  'agent':['agent','智能体'],
  'enduser':['enduser','user','用户'],
  'control_plane':['control','控制平面'],
  'execution_plane':['execution','执行平面'],
  'qa':['test','regression','验证','测试','回归'],
  'sre':['trace','runtime','observability','incident','可观测','事故'],
  'docs':['document','protocol','sop','文档','协议'],
  'mixed':['score','clearance','protocol','audit','评分','清零','协议','审计'],
}


def normalize(path:str)->str:
    return path if path.startswith('Release/') else f'Release/{path}'


def full_text(root:Path, rel:str)->str:
    p=root/normalize(rel)
    return p.read_text(encoding='utf-8') if p.exists() else ''


def collect_source_buckets(root: Path, issue_type: str, owner: str, tools: list[str], examples_dir: Path) -> dict[str, str]:
    example_texts=[]
    for path in sorted(examples_dir.glob('issue_input*.json')):
        data=json.loads(path.read_text(encoding='utf-8'))
        if data.get('issue_type') == issue_type:
            example_texts.append(json.dumps(data, ensure_ascii=False))
    return {
        'owner': full_text(root, owner) if owner else '',
        'tools': '\n'.join(full_text(root, tool) for tool in tools),
        'protocols': '\n'.join(full_text(root, rel) for rel in [
            'protocols/60_HGS_IO_Protocol.md',
            'protocols/61_Automation_Orchestration_Protocol.md',
            'protocols/62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md',
        ]),
        'examples': '\n'.join(example_texts),
    }


def trace_hint_hits(text: str, hints: list[str]) -> list[dict]:
    lines=text.splitlines()
    lowered=[line.lower() for line in lines]
    out=[]
    for hint in hints:
        hit_line=None
        for idx, line in enumerate(lowered, start=1):
            if hint.lower() in line:
                hit_line=idx
                out.append({'hint': hint, 'line': idx, 'snippet': lines[idx-1][:180]})
                break
        if hit_line is None:
            out.append({'hint': hint, 'line': None, 'snippet': ''})
    return out


def explain_bucket(name: str, text: str, hints: list[str]) -> dict:
    hits=trace_hint_hits(text, hints)
    matched=[h for h in hits if h['line'] is not None]
    return {
        'bucket': name,
        'matched_hint_count': len(matched),
        'missing_hint_count': len(hits) - len(matched),
        'coverage_score': len(matched),
        'matched_hints': matched[:8],
        'missing_hints': [h['hint'] for h in hits if h['line'] is None][:8],
        'status': 'covered' if matched else 'weak_or_missing',
    }


def build_issue_alignment_explanation(root: Path, issue_type: str, owner: str, tools: list[str], examples_dir: Path) -> dict:
    hints=ISSUE_HINTS.get(issue_type, ISSUE_HINTS['mixed'])
    buckets=collect_source_buckets(root, issue_type, owner, tools, examples_dir)
    bucket_reports={name: explain_bucket(name, text, hints) for name, text in buckets.items()}
    total=sum(item['coverage_score'] for item in bucket_reports.values())
    strongest=max(bucket_reports.values(), key=lambda item: item['coverage_score']) if bucket_reports else {'bucket':'', 'coverage_score':0}
    weakest=min(bucket_reports.values(), key=lambda item: item['coverage_score']) if bucket_reports else {'bucket':'', 'coverage_score':0}
    return {
        'issue_type': issue_type,
        'hints': hints,
        'total_coverage_score': total,
        'bucket_reports': bucket_reports,
        'strongest_bucket': strongest['bucket'],
        'weakest_bucket': weakest['bucket'],
        'explanation': f"{issue_type} 语义覆盖总分 {total}；最强来源 {strongest['bucket']}；最弱来源 {weakest['bucket']}。",
    }


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root',default='.')
    ap.add_argument('--manifest',default='Release/MANIFEST.json')
    ap.add_argument('--output',default='.hgs/semantic_alignment_report.json')
    ap.add_argument('--strict',action='store_true')
    args=ap.parse_args()
    root=Path(args.repo_root).resolve()
    manifest=json.loads((root/args.manifest).read_text(encoding='utf-8'))
    policy=manifest.get('automation_policy',{}).get('semantic_alignment_policy',{})
    route=manifest.get('automation_policy',{}).get('runtime_route_policy',{})
    supported=set(route.get('supported_issue_types',[]))
    covered=set()
    examples_dir=root/'examples'
    for path in sorted(examples_dir.glob('issue_input*.json')):
        data=json.loads(path.read_text(encoding='utf-8'))
        covered.add(data.get('issue_type','mixed'))
    missing_examples=sorted(supported-covered) if policy.get('require_example_for_every_supported_issue_type',True) else []
    semantic_mismatches=[]
    semantic_scores={}
    semantic_explanations={}
    for issue_type in sorted(supported):
        owner=route.get('owner_by_issue_type',{}).get(issue_type,'')
        tools=route.get('tools_by_issue_type',{}).get(issue_type,[])
        explanation=build_issue_alignment_explanation(root, issue_type, owner, tools, examples_dir)
        score=explanation['total_coverage_score']
        semantic_scores[issue_type]=score
        semantic_explanations[issue_type]=explanation
        if score < policy.get('minimum_semantic_coverage_per_issue_type',1):
            semantic_mismatches.append(f'low_semantic_coverage:{issue_type}:{score}')
    report={
      'semantic_alignment_status':'pass' if not missing_examples and not semantic_mismatches else 'fail',
      'missing_examples_for_supported_issue_types':missing_examples,
      'semantic_mismatches':semantic_mismatches,
      'semantic_scores':semantic_scores,
      'semantic_explanations':semantic_explanations,
      'example_coverage':sorted(covered),
      'supported_issue_types':sorted(supported),
    }
    out=root/args.output
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if args.strict and report['semantic_alignment_status']!='pass' else 0


if __name__=='__main__':
    raise SystemExit(main())
