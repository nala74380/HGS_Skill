#!/usr/bin/env python3
from __future__ import annotations
from typing import Any

def _norm(text: str) -> str:
    return (text or "").lower()

def _score_pattern(issue: dict, pattern: dict) -> tuple[int,list[str]]:
    reasons=[]
    score=0
    issue_type=issue.get('issue_type','')
    if issue_type in pattern.get('issue_types',[]):
        score += 30
        reasons.append(f'issue_type命中:{issue_type}')
    risk_flags=set(issue.get('risk_flags',[]))
    hit_risks=sorted(risk_flags.intersection(set(pattern.get('risk_flags',[]))))
    if hit_risks:
        score += min(25, 10*len(hit_risks))
        reasons.append('risk_flags命中:' + '、'.join(hit_risks))
    haystack=' '.join([_norm(issue.get('title','')),_norm(issue.get('current_question','')),' '.join(_norm(x) for x in issue.get('critical_paths',[]))])
    hit_keywords=[kw for kw in pattern.get('keywords',[]) if _norm(kw) in haystack]
    if hit_keywords:
        score += min(35, 7*len(hit_keywords))
        reasons.append('keywords命中:' + '、'.join(hit_keywords[:5]))
    if issue.get('verification_target') in {'L3','L4'}:
        score += 5
    return score, reasons

def evaluate_experience_memory(issue: dict, policy: dict) -> dict:
    enabled = policy.get('enabled', False)
    if not enabled:
        return {'enabled': False}
    support_hits=[]
    challenge_hits=[]
    invalidation_hits=[]
    all_patterns = [('candidate', p) for p in policy.get('candidate_experience_patterns',[])] + [('approved', p) for p in policy.get('approved_experience_patterns',[])]
    for status, pattern in all_patterns:
        score, reasons = _score_pattern(issue, pattern)
        if score >= 45:
            support_hits.append({'pattern_id': pattern.get('id'), 'catalog': status, 'score': score, 'reasons': reasons, 'bias_hint': pattern.get('bias_hint','')})
        elif 25 <= score < 45:
            challenge_hits.append({'pattern_id': pattern.get('id'), 'catalog': status, 'score': score, 'reasons': reasons, 'challenge_reason': '命中不足或当前上下文不完全同构，仅作为弱提示'})
    # invalidation: if issue says new version / migrated / rewritten, mark stale bias
    haystack=' '.join([_norm(issue.get('title','')),_norm(issue.get('current_question',''))])
    if any(sig in haystack for sig in ['migrat','rewrite','新版本','改版','重构','升级']):
        invalidation_hits.append({'pattern_id':'stale-experience-bias','score':60,'reason':'检测到版本/架构变动信号，旧经验影响应降权'})
    support_hits=sorted(support_hits, key=lambda x: x['score'], reverse=True)
    challenge_hits=sorted(challenge_hits, key=lambda x: x['score'], reverse=True)
    support_wins = len(support_hits) > 0 and (len(invalidation_hits)==0)
    challenge_wins = (len(challenge_hits) > 0 and len(support_hits)==0) or len(invalidation_hits)>0
    bias_influence=min(policy.get('experience_bias_max_influence',12), 4*len(support_hits))
    summary = {
        'enabled': True,
        'mode': policy.get('mode','dual_track'),
        'support_track_name': policy.get('support_track_name','经验支持轨'),
        'challenge_track_name': policy.get('challenge_track_name','经验挑战轨'),
        'experience_support_hits': support_hits,
        'experience_challenge_hits': challenge_hits,
        'experience_invalidation_hits': invalidation_hits,
        'experience_competition_summary': {
            'support_track_win': support_wins,
            'challenge_track_win': challenge_wins,
            'invalidation_present': len(invalidation_hits) > 0,
            'experience_bias_strength': bias_influence,
            'principle': policy.get('principle','experience_is_bias_not_verdict')
        },
        'suggested_bias_downgrade': bool(challenge_wins and support_hits),
        'suggested_freeze': bool(len(invalidation_hits) > 0 and any(hit.get('catalog') == 'approved' for hit in support_hits)),
        'suggested_retire': bool(len(invalidation_hits) > 0 and len(support_hits) == 0),
        'human_review_required': bool(policy.get('human_review_required_for_high_risk_domain',True) and issue.get('issue_type') in set(policy.get('high_risk_domains',[])))
    }
    return summary
