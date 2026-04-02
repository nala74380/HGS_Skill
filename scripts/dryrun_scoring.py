from __future__ import annotations
from typing import Any

def compute_scoring_axes(issue, candidate_paths, alternative_hypotheses, counterfactual_challenges, mandatory_checklist, managed_route_conflicts, blocking_reasons, simulated_tool_results, score, review, dispatch, user_choice, scoring_policy):
    axes={
        'exploration_breadth': min(100, 40 + len(candidate_paths)*8 + len(alternative_hypotheses)*6),
        'counterfactual_rigor': min(100, 40 + len(counterfactual_challenges)*18),
        'convergence_quality': min(100, score.get('route_stability_score',0) + (8 if dispatch=='dispatch' else -12)),
        'execution_readiness': min(100, score.get('tool_coverage_score',0) - (18 if review!='review' else 0)),
        'user_fit': min(100, 70 + (8 if issue.get('current_question') else 0) - (8 if user_choice=='yes' else 0)),
        'result_adequacy': min(100, score.get('evidence_completeness_score',0) - len(blocking_reasons)*6 - len(managed_route_conflicts)*4),
    }
    weights=scoring_policy.get('axis_weights',{})
    overall=round(sum(axes.get(k,0)*weights.get(k,0) for k in axes),2)
    gaps=[k for k,v in scoring_policy.get('minimum_axis_scores',{}).items() if axes.get(k,0)<v]
    return axes, overall, gaps
