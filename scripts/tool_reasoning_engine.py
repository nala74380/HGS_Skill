#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any

CAPABILITY_RULES = {
    'auth': {
        'capabilities': ['identity', 'session', 'jwt', 'step_up_auth'],
        'tokens': {
            'identity': ['identity', '身份', 'auth'],
            'session': ['session', '会话', 'refresh'],
            'jwt': ['jwt', 'token'],
            'step_up_auth': ['stepup', 'step-up', '二次验证'],
        },
    },
    'billing': {
        'capabilities': ['ledger', 'quota', 'usage'],
        'tokens': {
            'ledger': ['ledger', '账本'],
            'quota': ['quota', '配额'],
            'usage': ['usage', '计费'],
        },
    },
    'console': {
        'capabilities': ['console_auth', 'project_context'],
        'tokens': {
            'console_auth': ['console', '控制台', 'auth'],
            'project_context': ['context', '上下文', 'project'],
        },
    },
    'worker': {
        'capabilities': ['runtime_trace', 'heartbeat'],
        'tokens': {
            'runtime_trace': ['runtime', 'trace', '运行时'],
            'heartbeat': ['heartbeat', '心跳'],
        },
    },
    'security': {
        'capabilities': ['guard', 'audit', 'bypass_review'],
        'tokens': {
            'guard': ['guard', '安全'],
            'audit': ['audit', '审计'],
            'bypass_review': ['bypass', '绕过', '授权'],
        },
    },
    'rule': {
        'capabilities': ['state_machine', 'rule_matrix'],
        'tokens': {
            'state_machine': ['state', '状态'],
            'rule_matrix': ['rule', 'matrix', '规则'],
        },
    },
    'release': {
        'capabilities': ['compatibility', 'release_config'],
        'tokens': {
            'compatibility': ['compatibility', '兼容'],
            'release_config': ['release', 'config', '发布', '配置'],
        },
    },
    'frontend': {
        'capabilities': ['ui_surface', 'api_contract'],
        'tokens': {
            'ui_surface': ['ui', 'surface', '界面', '前端'],
            'api_contract': ['api', 'contract'],
        },
    },
    'mixed': {
        'capabilities': ['governance', 'clearance'],
        'tokens': {
            'governance': ['protocol', 'audit', '协议', '审计'],
            'clearance': ['score', 'clearance', '评分', '清零'],
        },
    },
}

RISK_RULES = {
    'high_risk_action': 'high_risk_guard_required',
    'auth_bypass': 'auth_scope_conflict',
    'destructive_change': 'high_risk_guard_required',
    'scope_risk': 'governance_conflict',
}


def _match_lines(text: str, token: str) -> list[dict[str, Any]]:
    out=[]
    lines=text.splitlines()
    token_lower=token.lower()
    for idx, line in enumerate(lines, start=1):
        if token_lower in line.lower():
            out.append({'token': token, 'line': idx, 'snippet': line[:180]})
    return out


def build_capability_trace(issue_type: str, text: str) -> list[dict[str, Any]]:
    config = CAPABILITY_RULES.get(issue_type, CAPABILITY_RULES['mixed'])
    trace=[]
    for capability in config['capabilities']:
        matches=[]
        matched_tokens=[]
        for token in config['tokens'].get(capability, []):
            token_matches=_match_lines(text, token)
            if token_matches:
                matched_tokens.append(token)
                matches.extend(token_matches[:2])
        trace.append({
            'capability': capability,
            'matched_tokens': matched_tokens,
            'evidence': matches[:4],
            'status': 'matched' if matches else 'not_matched',
            'rule': f'{capability}: requires one or more capability tokens in tool text',
        })
    return trace


def build_rule_trace(issue_type: str, capability_trace: list[dict[str, Any]], risk_flags: list[str]) -> list[dict[str, Any]]:
    matched_capabilities=[item['capability'] for item in capability_trace if item['status']=='matched']
    trace=[{
        'rule_id': 'issue_capability_alignment',
        'input': issue_type,
        'status': 'matched' if matched_capabilities else 'weak_signal',
        'matched_capabilities': matched_capabilities,
        'reason': 'tool text contains structured capability evidence' if matched_capabilities else 'no capability-level evidence found',
    }]
    for risk in risk_flags:
        trace.append({
            'rule_id': f'risk_flag::{risk}',
            'input': risk,
            'status': 'matched' if risk in RISK_RULES else 'ignored',
            'derived_finding': RISK_RULES.get(risk, ''),
            'reason': 'risk flag escalates review obligation' if risk in RISK_RULES else 'risk flag not mapped to explicit rule',
        })
    return trace


def execute_tool_reasoning(repo_root: Path, tool_path: str, issue: dict[str, Any], risk_flags: list[str]) -> dict[str, Any]:
    path=repo_root/tool_path
    try:
        text=path.read_text(encoding='utf-8')
    except Exception:
        return {'tool': tool_path, 'status': 'heuristic_full_text_signal', 'confidence': 0.12, 'findings': [], 'evidence_trace': [], 'capability_trace': [], 'rule_trace': []}
    issue_type=issue.get('issue_type','mixed')
    capability_trace=build_capability_trace(issue_type, text)
    evidence=[e for cap in capability_trace for e in cap.get('evidence', [])]
    matched_caps=[cap['capability'] for cap in capability_trace if cap['status']=='matched']
    rule_trace=build_rule_trace(issue_type, capability_trace, risk_flags)
    findings=[]
    if matched_caps:
        findings.append(f'{issue_type}_signal_detected')
    for risk in risk_flags:
        finding=RISK_RULES.get(risk)
        if finding and finding not in findings:
            findings.append(finding)
    confidence=min(0.60, 0.16 + 0.08*len(matched_caps) + 0.02*sum(1 for item in rule_trace if item['status']=='matched'))
    finding_kind = 'capability_signal' if matched_caps else ('weak_signal' if evidence else 'no_signal')
    return {
        'tool': tool_path,
        'status': 'structured_capability_signal',
        'confidence': round(confidence,2),
        'findings': findings,
        'evidence_trace': evidence[:8],
        'capability_trace': capability_trace,
        'rule_trace': rule_trace,
        'finding': {
            'type': issue_type,
            'kind': finding_kind,
            'severity': 'medium' if len(matched_caps) >= 2 else ('low' if matched_caps else 'none'),
            'evidence_count': len(evidence),
            'matched_capabilities': matched_caps,
        },
    }


def run_reasoning(issue: dict[str, Any], tool_paths: list[str], repo_root: Path, risk_flags: list[str] | None = None):
    risk_flags = risk_flags or list(issue.get('risk_flags', []))
    results = [execute_tool_reasoning(repo_root, tool_path, issue, risk_flags) for tool_path in tool_paths]
    summary = {
        'tool_count': len(results),
        'max_confidence': max((item.get('confidence', 0.0) for item in results), default=0.0),
        'matched_capability_count': sum(len(item.get('finding', {}).get('matched_capabilities', [])) for item in results),
    }
    return results, summary


if __name__ == '__main__':
    raise SystemExit('Import only')
