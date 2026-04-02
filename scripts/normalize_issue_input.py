#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "issue"

def ensure_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]

def infer_issue_type_candidates(text: str, route: dict, fallback: str='mixed') -> tuple[list[dict], list[str]]:
    scores=[]; hits=[]; lower=text.lower()
    for issue_type, keywords in route.get('issue_type_inference_keywords', {}).items():
        matched=[kw for kw in keywords if kw.lower() in lower]
        if matched:
            scores.append({'issue_type':issue_type,'score':len(matched),'matched_keywords':matched})
            hits.extend([f'issue_type_keyword:{issue_type}:{kw}' for kw in matched])
    scores.sort(key=lambda x:(-x['score'],x['issue_type']))
    if not scores:
        return [{'issue_type':fallback,'score':0,'matched_keywords':[]}], hits
    maxn=max(1, route.get('execution_style_balance',{}).get('exploration_stage',{}).get('max_parallel_issue_type_candidates',3))
    return scores[:maxn], hits

def infer_risk_flags(text: str, route: dict) -> tuple[list[str], list[str]]:
    lower=text.lower(); out=[]; hits=[]
    for flag, keywords in route.get('risk_flag_inference_keywords', {}).items():
        matched=[kw for kw in keywords if kw.lower() in lower]
        if matched:
            out.append(flag)
            hits.extend([f'risk_keyword:{flag}:{kw}' for kw in matched])
    return out, hits

def infer_acceptance(issue_type: str):
    lib={
        'auth':['身份、会话与授权范围保持一致','失败路径不会越权或丢失上下文'],
        'billing':['账本、配额与展示结果一致','不会遗留陈旧占用或错误可用量'],
        'release':['发布配置与目标环境兼容','升级/回滚路径清晰且可验证'],
        'frontend':['界面状态与后端事实一致','关键交互在异常情况下可恢复'],
        'console':['控制台可见上下文与实际操作目标一致','保护动作不会恢复到错误对象'],
        'worker':['身份链与运行状态可解释','异常窗口与恢复过程可被追溯'],
        'rule':['规则语义在文档、接口、界面间一致'],
        'security':['高风险动作受到约束且审计可追踪'],
        'mixed':['主要风险、对象、边界与验证条件已被明确']
    }
    return lib.get(issue_type, lib['mixed'])

def infer_critical(issue_type: str):
    lib={
        'auth':['登录/鉴权/刷新/恢复主链路','失败后回到安全状态'],
        'billing':['占用变化 -> 配额展示 -> 可用量核对链路'],
        'release':['升级 -> 验证 -> 回滚链路'],
        'frontend':['输入 -> 请求 -> 状态展示 -> 异常恢复链路'],
        'console':['上下文切换 -> 受保护动作 -> 恢复链路'],
        'worker':['身份建立 -> 心跳 -> 异常 -> 恢复链路'],
        'rule':['规则输入 -> 状态迁移 -> 输出语义链路'],
        'security':['高风险动作前置校验 -> 执行 -> 审计链路'],
        'mixed':['主路径 -> 异常路径 -> 恢复路径']
    }
    return lib.get(issue_type, lib['mixed'])

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--manifest', default='Release/MANIFEST.json')
    ap.add_argument('--issue-input', required=True)
    ap.add_argument('--output', default='.hgs/normalized_issue_input.json')
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    manifest = json.loads((root / args.manifest).read_text(encoding='utf-8'))
    route = manifest.get('automation_policy', {}).get('runtime_route_policy', {})
    issue = json.loads((root / args.issue_input).read_text(encoding='utf-8'))

    title = issue.get('title') or issue.get('current_question') or issue.get('summary') or 'unnamed issue'
    current_question = issue.get('current_question') or title
    text_for_inference = ' '.join([title, current_question, ' '.join(ensure_list(issue.get('acceptance_criteria'))), ' '.join(ensure_list(issue.get('critical_paths')))])
    issue_type_candidates, issue_type_hits = infer_issue_type_candidates(text_for_inference, route)
    explicit_issue_type = issue.get('issue_type')
    issue_type = explicit_issue_type or issue_type_candidates[0]['issue_type'] or 'mixed'
    inferred_risks, risk_hits = infer_risk_flags(text_for_inference, route)
    risk_flags = ensure_list(issue.get('risk_flags'))
    for flag in inferred_risks:
        if flag not in risk_flags:
            risk_flags.append(flag)
    source_of_truth = ensure_list(issue.get('source_of_truth')) or ['Release/MANIFEST.json', 'Release/00_HGS_Master_Loader.md']
    critical_paths = ensure_list(issue.get('critical_paths')) or infer_critical(issue_type)
    acceptance_criteria = ensure_list(issue.get('acceptance_criteria')) or infer_acceptance(issue_type)
    verification_target = issue.get('verification_target', 'L3')
    max_change_boundary = issue.get('max_change_boundary') or {
        'mode': 'provisional',
        'policy_source': 'automation_policy.runtime_route_policy',
        'notes': 'No explicit user boundary supplied; use non-destructive provisional boundary until evidence increases.'
    }
    normalized = dict(issue)
    normalized.update({
        'issue_id': issue.get('issue_id') or f"DRYRUN-{slug(title)[:40]}",
        'title': title,
        'current_question': current_question,
        'issue_type': issue_type,
        'candidate_issue_types': issue_type_candidates,
        'source_of_truth': source_of_truth,
        'risk_flags': risk_flags,
        'critical_paths': critical_paths,
        'acceptance_criteria': acceptance_criteria,
        'verification_target': verification_target,
        'max_change_boundary': max_change_boundary,
        'secondary_findings': ensure_list(issue.get('secondary_findings')),
        'reopened_findings': ensure_list(issue.get('reopened_findings')),
        'normalization_metadata': {
            'inferable_input_fields': route.get('inferable_input_fields', []),
            'minimum_user_input_fields': route.get('minimum_user_input_fields', []),
            'issue_type_inferred': not bool(explicit_issue_type),
            'inference_hits': issue_type_hits + risk_hits,
            'ambiguity_present': len(issue_type_candidates) > 1 and issue_type_candidates[0]['score'] == issue_type_candidates[1]['score'] if len(issue_type_candidates)>1 else False,
            'acceptance_inferred': not bool(issue.get('acceptance_criteria')),
            'critical_paths_inferred': not bool(issue.get('critical_paths')),
        },
    })
    missing_minimum = [k for k in route.get('minimum_user_input_fields', []) if not normalized.get(k)]
    user_friendliness_score = 100 - 10 * len(missing_minimum)
    if normalized['normalization_metadata']['issue_type_inferred']:
        user_friendliness_score += 5
    if normalized['normalization_metadata']['ambiguity_present']:
        user_friendliness_score -= 8
    if normalized['normalization_metadata']['acceptance_inferred']:
        user_friendliness_score += 3
    if normalized['normalization_metadata']['critical_paths_inferred']:
        user_friendliness_score += 3
    report = {
        'normalization_status': 'pass' if not missing_minimum else 'fail',
        'missing_minimum_user_input_fields': missing_minimum,
        'user_input_friendliness_score': max(0, min(100, user_friendliness_score)),
        'normalized_issue': normalized
    }
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and missing_minimum else 0

if __name__ == '__main__':
    raise SystemExit(main())
