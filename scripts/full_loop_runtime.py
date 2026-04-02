from __future__ import annotations

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from experience_memory_engine import evaluate_experience_memory
from full_loop_components import (
    apply_issue_scaling_policy,
    build_act_before_asking,
    build_action_trace,
    build_alternative_hypotheses,
    build_candidate_paths,
    build_counterfactual_challenges,
    build_display_lookup,
    build_mandatory_checklist,
    build_opportunity_discovery,
    build_role_disagreement,
    build_ticket_registries,
    build_track_competition,
    compute_scoring_axes,
    disp,
    disp_list,
    normalize_release,
    resolve_display_mode,
    resolve_display_mode_text,
    run_normalizer,
    simulate_tool_result,
    slug,
    uniq,
)

DEFAULT_FAIL_DATA = {
    'mode': 'full_loop',
    'automation_execution_status': 'fail',
    'blocking_reasons': ['full_release_assembly_status != pass'],
    'user_choice_required': 'no',
    'suggestion_mode': 'no',
}
DEFAULT_CHAIN = [
    'normalize',
    'owner_router',
    'risk_gate',
    'execute',
    'validate',
    'experience',
    'rereview',
    'docs_sink',
    'closeout',
]


def load_runtime_environment(root: Path, report_rel: str, manifest_rel: str, display_mode_override: str | None) -> dict[str, Any]:
    report = json.loads((root / report_rel).read_text(encoding='utf-8'))
    manifest = json.loads((root / manifest_rel).read_text(encoding='utf-8'))
    policy = manifest.get('automation_policy', {})
    route = policy.get('runtime_route_policy', {})
    return {
        'root': root,
        'report': report,
        'manifest': manifest,
        'policy': policy,
        'route': route,
        'thresholds': policy.get('thresholds', {}),
        'scoring_policy': policy.get('scoring_axes_policy', {}),
        'experience_policy': policy.get('experience_memory_policy', {}),
        'display_lookup': build_display_lookup(manifest),
        'display_policy': route.get('display_actor_policy', {}),
        'conversation_display_policy': policy.get('conversation_display_policy', {}),
        'clearance_policy': policy.get('full_issue_clearance_policy', {}),
        'display_mode': resolve_display_mode(display_mode_override, policy.get('conversation_display_policy', {})),
        'creativity': route.get('creativity_amplification_policy', {}),
        'exploration_mode_policy': route.get('exploration_mode_policy', {}),
        'opportunity_policy': route.get('opportunity_discovery_policy', {}),
        'disagreement_policy': route.get('role_disagreement_policy', {}),
        'fast_track_policy': policy.get('fast_track_policy', {}),
        'parallel_actions': policy.get('parallel_actions', []),
    }


def assembly_failed(report: dict[str, Any]) -> bool:
    return report.get('full_release_assembly_status') != 'pass'


def read_route_drift_report(root: Path) -> dict[str, Any]:
    subprocess.run(
        [sys.executable, str(root / 'scripts/validate_route_policy_drift.py'), '--repo-root', str(root), '--manifest', 'Release/MANIFEST.json'],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads((root / '.hgs/route_policy_drift_report.json').read_text(encoding='utf-8'))


def apply_experience_bias(candidate_paths: list[dict[str, Any]], experience_summary: dict[str, Any]) -> list[dict[str, Any]]:
    summary = experience_summary.get('experience_competition_summary', {})
    exp_bias = summary.get('experience_bias_strength', 0)
    support_hits = experience_summary.get('experience_support_hits', [])
    if summary.get('support_track_win'):
        for cp in candidate_paths:
            if any(cp.get('issue_type') == hit.get('pattern_id', '').split('-')[0] for hit in support_hits):
                cp['score'] = min(100, cp.get('score', 0) + exp_bias)
                cp['rationale'] = cp.get('rationale', '') + '；经验支持轨提升优先级'
    if summary.get('challenge_track_win'):
        for cp in candidate_paths:
            cp['score'] = max(0, cp.get('score', 0) - 4)
    return candidate_paths


def resolve_assignment(issue_type: str, risks: list[str], route: dict[str, Any], display_lookup: dict[str, str]) -> dict[str, Any]:
    owner_map = route.get('owner_by_issue_type', {})
    executor_map = route.get('p8_executor_by_issue_type', {})
    tools_map = route.get('tools_by_issue_type', {})
    risk_tool_map = route.get('tools_by_risk_flag', {})
    always = route.get('always_include_tools', [])

    owner_rel = owner_map.get(issue_type) or owner_map.get('mixed')
    owner = normalize_release(owner_rel) if owner_rel else ''
    p8_rel = executor_map.get(issue_type) or executor_map.get('mixed')
    p8_executor = normalize_release(p8_rel) if p8_rel else ''

    required_tools: list[str] = []
    required_tools.extend(normalize_release(item) for item in tools_map.get(issue_type, tools_map.get('mixed', [])))
    for risk in risks:
        required_tools.extend(normalize_release(item) for item in risk_tool_map.get(risk, []))
    required_tools.extend(normalize_release(item) for item in always)
    required_tools = uniq(required_tools)

    return {
        'owner': owner,
        'owner_name': disp(owner, display_lookup),
        'p8_executor': p8_executor,
        'p8_name': disp(p8_executor, display_lookup),
        'required_tools': required_tools,
        'required_tool_names': disp_list(required_tools, display_lookup),
    }


def evaluate_simulations(root: Path, issue: dict[str, Any], risks: list[str], issue_type: str, route: dict[str, Any], required_tools: list[str]) -> dict[str, Any]:
    sim_policy = route.get('simulation_quality_policy', {})
    simulated_tool_results = [simulate_tool_result(tool, issue, risks, sim_policy, root) for tool in required_tools]
    min_tool_results = route.get('tool_execution_simulation_policy', {}).get('minimum_tool_result_count_before_review', 2)
    min_conf = sim_policy.get('minimum_simulation_confidence_before_review', 0.78)
    low_conf = [r['tool'] for r in simulated_tool_results if r['confidence'] < min_conf and r.get('finding', {}).get('kind') == 'keyword_signal']
    findings = sorted({finding for result in simulated_tool_results for finding in result.get('findings', [])})
    route_conflicts: list[str] = []
    escalations = set(sim_policy.get('escalate_findings_to_route_conflicts', []))
    for finding in findings:
        if finding in escalations and issue_type in {'auth', 'security', 'billing', 'release', 'mixed'}:
            route_conflicts.append(f'simulation_conflict:{finding}')
    return {
        'sim_policy': sim_policy,
        'simulated_tool_results': simulated_tool_results,
        'minimum_tool_results': min_tool_results,
        'minimum_confidence': min_conf,
        'low_confidence_tools': low_conf,
        'simulation_findings': findings,
        'route_conflicts_from_simulation': route_conflicts,
    }


def manage_route_conflicts(route_conflicts: list[str], experience_summary: dict[str, Any]) -> list[str]:
    manageable_conflicts = [c for c in route_conflicts if c == 'simulation_conflict:auth_scope_conflict']
    summary = experience_summary.get('experience_competition_summary', {})
    if route_conflicts and len(manageable_conflicts) == len(route_conflicts) and experience_summary.get('human_review_required', False) and summary.get('support_track_win'):
        return []
    return list(route_conflicts)


def collect_blockers(issue: dict[str, Any], issue_type: str, supported_issue_types: set[str], assignment: dict[str, Any], normalized_report: dict[str, Any], simulation: dict[str, Any], route_conflicts: list[str]) -> dict[str, Any]:
    blocking_reasons: list[str] = []
    derived_route_conflicts = list(route_conflicts)
    evidence_missing = list(normalized_report.get('missing_minimum_user_input_fields', []))

    if issue_type not in supported_issue_types:
        derived_route_conflicts.append(f'unsupported_issue_type:{issue_type}')
    if not assignment.get('owner'):
        blocking_reasons.append(f'owner_mapping_missing:{issue_type}')
    if not assignment.get('p8_executor'):
        blocking_reasons.append(f'p8_executor_mapping_missing:{issue_type}')
    if not assignment.get('required_tools'):
        blocking_reasons.append(f'tool_resolution_empty:{issue_type}')
    if len(simulation['simulated_tool_results']) < simulation['minimum_tool_results']:
        blocking_reasons.append('simulated_tool_results_below_minimum')
    if simulation['low_confidence_tools']:
        blocking_reasons.append('simulation_confidence_below_minimum')
    if not (issue.get('critical_paths') and issue.get('acceptance_criteria')):
        blocking_reasons.append('validation_bundle_incomplete')
    if evidence_missing:
        blocking_reasons.append('required_inputs_missing')

    user_choice = 'yes' if 'user_choice_required' in issue.get('risk_flags', []) else 'no'
    if user_choice == 'yes':
        blocking_reasons.append('user_choice_required')

    return {
        'blocking_reasons': blocking_reasons,
        'route_conflicts': derived_route_conflicts,
        'evidence_missing': evidence_missing,
        'user_choice': user_choice,
    }


def build_score_snapshot(issue: dict[str, Any], issue_type: str, supported_issue_types: set[str], assignment: dict[str, Any], route: dict[str, Any], managed_route_conflicts: list[str], blocking_reasons: list[str], simulated_tool_results: list[dict[str, Any]], normalized_report: dict[str, Any]) -> dict[str, int]:
    owner_confidence = 90 if assignment.get('owner') else 20
    route_stability = 82 if issue_type in supported_issue_types and assignment.get('owner') and not managed_route_conflicts else 30
    tool_coverage = min(100, 65 + 4 * len(assignment.get('required_tools', []))) if assignment.get('required_tools') else 0
    required_input = route.get('required_input_fields', [])
    evidence_score = min(100, round(100 * sum(1 for f in required_input if bool(issue.get(f))) / max(1, len(required_input))))
    if issue.get('normalization_metadata', {}).get('issue_type_inferred'):
        evidence_score = min(100, evidence_score + 2)
    if simulated_tool_results:
        evidence_score = min(100, evidence_score + 5)
    reopen_risk = 25 if issue.get('verification_target') in {'L3', 'L4'} else 45
    if managed_route_conflicts:
        reopen_risk += 15
    closeout_readiness = 20 if blocking_reasons else 90
    return {
        'owner_confidence': owner_confidence,
        'route_stability_score': route_stability,
        'tool_coverage_score': tool_coverage,
        'evidence_completeness_score': evidence_score,
        'reopen_risk_score': reopen_risk,
        'closeout_readiness_score': closeout_readiness,
        'user_input_friendliness_score': normalized_report.get('user_input_friendliness_score', 0),
    }


def compute_flow_decisions(assignment: dict[str, Any], thresholds: dict[str, Any], managed_route_conflicts: list[str], blocking_reasons: list[str], overall_quality_score: float, scoring_policy: dict[str, Any], axis_gaps: list[str], simulation: dict[str, Any], evidence_missing: list[str], user_choice: str, issue_type: str) -> dict[str, Any]:
    per_type = thresholds.get('per_issue_type_overrides', {})
    owner_threshold = per_type.get(issue_type, {}).get('owner_confidence_min_for_direct_dispatch',
                                                       thresholds.get('owner_confidence_min_for_direct_dispatch', 70))
    dispatch = 'dispatch' if assignment.get('owner') and not managed_route_conflicts and assignment.get('required_tools') and owner_threshold <= 90 and not blocking_reasons else 'hold'
    review = 'review' if dispatch == 'dispatch' and not blocking_reasons else 'blocked'
    reopen = 'reopen' if review != 'review' else 'none'
    done = 'ready' if review == 'review' and not blocking_reasons else 'blocked'
    suggestion_mode = 'yes' if dispatch == 'hold' and review == 'blocked' else 'no'
    mutable_blockers = list(blocking_reasons)
    if suggestion_mode == 'yes':
        mutable_blockers.append('suggestion_mode_only')
    if axis_gaps:
        mutable_blockers.append('score_axis_below_minimum')
    if overall_quality_score < scoring_policy.get('minimum_overall_quality_score_for_confident_result', 84):
        mutable_blockers.append('overall_quality_score_below_confident_threshold')
    automation_status = 'pass' if all([
        assignment.get('owner'),
        assignment.get('required_tools'),
        dispatch == 'dispatch',
        review == 'review',
        user_choice == 'no',
        suggestion_mode == 'no',
        not managed_route_conflicts,
        not evidence_missing,
        len(simulation['simulated_tool_results']) >= simulation['minimum_tool_results'],
        not simulation['low_confidence_tools'],
    ]) else 'fail'
    next_action = 'dispatch_issue_to_owner' if automation_status == 'pass' else ('user_choice_required' if user_choice == 'yes' else 'resolve_blocking_reasons')
    return {
        'dispatch': dispatch,
        'review': review,
        'reopen': reopen,
        'done': done,
        'suggestion_mode': suggestion_mode,
        'blocking_reasons': mutable_blockers,
        'automation_status': automation_status,
        'next_action': next_action,
    }


def build_linked_resources(assignment: dict[str, Any], display_lookup: dict[str, str]) -> dict[str, Any]:
    linked_files = [assignment.get('p8_executor', '')] + assignment.get('required_tools', [])
    linked_protocols = [
        normalize_release('protocols/60_HGS_IO_Protocol.md'),
        normalize_release('protocols/61_Automation_Orchestration_Protocol.md'),
        normalize_release('protocols/62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md'),
        normalize_release('protocols/50_RE_REVIEW_PROTOCOL.md'),
    ]
    linked_records = ['issue ledger', 'dispatch record', 'exec plan', 'validation bundle', 'experience record', 'review record', 'closeout record']
    linked_docs = ['Release/docs/角色调用关系总表.md', 'Release/docs/角色-工具矩阵总表.md', 'Release/docs/工具调用关系总表.md']
    return {
        'linked_files': linked_files,
        'linked_files_display': disp_list(linked_files, display_lookup),
        'linked_protocols': linked_protocols,
        'linked_protocols_display': disp_list(linked_protocols, display_lookup),
        'linked_records': linked_records,
        'linked_docs': linked_docs,
    }


def build_issue_stub(issue: dict[str, Any], issue_type: str, risks: list[str], assignment: dict[str, Any]) -> dict[str, Any]:
    return {
        'issue_id': issue.get('issue_id') or f"DRYRUN-{slug(issue['title'])[:40]}",
        'title': issue['title'],
        'issue_type': issue_type,
        'problem_statement': issue.get('current_question') or issue['title'],
        'owner': assignment.get('owner', ''),
        'source_of_truth': issue.get('source_of_truth', []),
        'risk_flags': risks,
        'status': 'stub_created' if assignment.get('owner') else 'owner_unresolved',
    }


def build_report_data(environment: dict[str, Any], issue: dict[str, Any], issue_type: str, risks: list[str], normalized_report: dict[str, Any], route_drift_report: dict[str, Any], assignment: dict[str, Any], simulation: dict[str, Any], track_competition: dict[str, Any], role_disagreement: dict[str, Any], opportunity_discovery: dict[str, Any], experience_summary: dict[str, Any], candidate_paths: list[dict[str, Any]], alternative_hypotheses: list[dict[str, Any]], counterfactual_challenges: list[dict[str, Any]], mandatory_checklist: list[dict[str, Any]], act_before_asking: dict[str, Any], score_snapshot: dict[str, Any], scoring_axes: dict[str, Any], overall_quality_score: float, axis_gaps: list[str], decisions: dict[str, Any], issue_scaling: dict[str, Any], issue_stub: dict[str, Any], linked_resources: dict[str, Any], action_trace: list[dict[str, Any]], current_work: dict[str, Any], parked_tickets: list[dict[str, Any]], continuation_tickets: list[dict[str, Any]], clearance_control: dict[str, Any], open_issue_count: int) -> dict[str, Any]:
    display_lookup = environment['display_lookup']
    policy = environment['policy']
    route = environment['route']
    clearance_policy = environment['clearance_policy']
    display_mode = environment['display_mode']
    conversation_display_policy = environment['conversation_display_policy']
    priority_rank = 1
    p9_dispatch_checklist = {
        'ticket_id': issue_stub['issue_id'],
        'dispatch_target_skill': assignment['p8_name'],
        'linked_files_to_modify': linked_resources['linked_files_display'],
        'linked_protocols_to_apply': linked_resources['linked_protocols_display'],
        'linked_records_to_update': linked_resources['linked_records'],
        'linked_docs_to_sync': linked_resources['linked_docs'],
        'status': 'checked',
        'current_phase': '派单编排',
    }
    return {
        'response_header': conversation_display_policy.get('status_header_exact_text', '自动化链路：已开启'),
        'display_mode': display_mode,
        'display_mode_text': resolve_display_mode_text(display_mode, conversation_display_policy),
        'mode': 'full_loop',
        'chain': DEFAULT_CHAIN,
        'issue_stub_created': 'yes' if assignment['owner'] else 'no',
        'owner_identified': 'yes' if assignment['owner'] else 'no',
        'owner_name': assignment['owner_name'],
        'ticket_id': issue_stub['issue_id'],
        'ticket_priority_rank': priority_rank,
        'problem_statement': issue_stub['problem_statement'],
        'required_tools_identified': 'yes' if assignment['required_tools'] else 'no',
        'required_tools': assignment['required_tool_names'],
        'p8_executor_skill': assignment['p8_name'],
        'p8_executor_skill_display': assignment['p8_name'],
        'risk_gates_checked': 'yes',
        'risk_gate_plan': {
            'high_risk_guard_gate': any(r in {'high_risk_action', 'destructive_change'} for r in risks),
            'auth_bypass_guard_gate': any(r in {'auth_bypass', 'scope_risk'} for r in risks),
            'runtime_stability_gate': any(r in {'runtime_stability', 'incident'} for r in risks),
            'must_run_tool_gate': bool(assignment['required_tools']),
        },
        'exec_plan_created': 'yes' if assignment['owner'] else 'no',
        'exec_plan': {'owner': assignment['owner_name'], 'max_change_boundary': issue.get('max_change_boundary', 'provisional'), 'success_definition': issue.get('acceptance_criteria', [])},
        'validation_plan_created': 'yes' if issue.get('critical_paths') and issue.get('acceptance_criteria') else 'no',
        'validation_plan': {'required_level': issue.get('verification_target', 'L3'), 'critical_paths': issue.get('critical_paths', [])},
        'experience_plan_created': 'yes',
        'experience_plan': {'experience_protocols': ['智能体体验协议', '用户体验协议'], 'replay_required_when_real_feedback_missing': True, 'user_angle_checks': ['clarity_of_outcome', 'visible_state_alignment', 'post_action_safety'], 'agent_angle_checks': ['operator_context_alignment', 'handoff_clarity', 'scope_safety']},
        'rereview_path_created': 'yes',
        'rereview_path': {'p9_rereview': True, 'p10_on_demand': True, 'protocol': '复审协议'},
        'issue_inventory_created': 'yes',
        'issue_inventory': {'open_issue_count_initialized': open_issue_count, 'items': [issue_stub] + list(issue.get('secondary_findings', [])) + list(issue.get('reopened_findings', [])), 'scaling_strategy': issue_scaling, 'parked_tickets': parked_tickets, 'continuation_tickets': continuation_tickets},
        'clearance_gate_created': 'yes',
        'clearance_loop_created': 'yes',
        'clearance_loop': {'controller': '问题清零控制器', 'rule': 'continue until open_issue_count = 0', 'next_required_action': decisions['next_action'], 'continuous_dispatch_required': clearance_policy.get('continuous_dispatch_required', True), 'continuous_rereview_required': clearance_policy.get('continuous_rereview_required', True), 'redispatch_after_each_failed_review': clearance_policy.get('redispatch_after_each_failed_review', True), 'redispatch_after_new_findings': clearance_policy.get('redispatch_after_new_findings', True), 'parked_ticket_registry_required': clearance_policy.get('parked_ticket_registry_required', True), 'clearance_control_is_primary_theme': clearance_policy.get('clearance_control_is_primary_theme', True)},
        'clearance_control': clearance_control,
        'normalized_input_summary': {'minimum_user_input_fields': route.get('minimum_user_input_fields', ['issue_type', 'current_question']), 'inferred_fields': issue.get('normalization_metadata', {}).get('inference_hits', []), 'recommended_missing': [f for f in route.get('recommended_input_fields', []) if not issue.get(f)]},
        'exploration_summary': {'candidate_paths': candidate_paths, 'alternative_hypotheses': alternative_hypotheses, 'counterfactual_challenges': counterfactual_challenges, 'mandatory_checklist': mandatory_checklist, 'principle': route.get('execution_style_balance', {}).get('principle', 'front_explore_mid_converge_late_strict')},
        'track_competition': track_competition,
        'role_disagreement': role_disagreement,
        'opportunity_discovery': opportunity_discovery,
        'experience_memory': experience_summary,
        'act_before_asking_summary': act_before_asking,
        'creativity_amplification_summary': {'policy': environment['creativity'], 'alternative_hypotheses_count': len(alternative_hypotheses), 'counterfactual_challenges_count': len(counterfactual_challenges), 'mandatory_checklist_completion': sum(1 for x in mandatory_checklist if x['status'] == 'done')},
        'route_simulation': {'simulated_route': [{'step': 1, 'actor': assignment['owner_name'], 'action': 'truth_owner_identification'}, {'step': 2, 'actor': 'P9派单官', 'action': 'dispatch_review'}, {'step': 3, 'actor': assignment['required_tool_names'], 'action': 'must_run_tools'}, {'step': 4, 'actor': 'QA验证负责人', 'action': 'validation_plan'}, {'step': 5, 'actor': '文档负责人', 'action': 'docs_sink'}], 'route_conflicts': decisions.get('route_conflicts_display', []), 'must_trigger_tools': assignment['required_tool_names'], 'likely_stop_conditions': decisions['blocking_reasons'] + [f"evidence_missing:{x}" for x in decisions['evidence_missing']] + [f"low_confidence:{x}" for x in simulation['low_confidence_tools']]},
        'simulated_tool_results': simulation['simulated_tool_results'],
        'simulation_findings_summary': simulation['simulation_findings'],
        'route_drift_report': route_drift_report,
        'action_trace': action_trace,
        'current_work_display': current_work,
        'p9_dispatch_checklist': p9_dispatch_checklist,
        'issue_priority_ranking': [{'ticket_id': issue_stub['issue_id'], 'priority_rank': priority_rank, 'severity': 'P1', 'reason': 'mainline issue after initial review'}],
        'review_result': {'review_passed': decisions['review'] == 'review' and decisions['done'] != 'blocked', 'remaining_issues': decisions['blocking_reasons'], 'review_notes': '复审不合格时继续回原单；复审合格时允许挂单治理'},
        'score_snapshot': score_snapshot,
        'scoring_axes': scoring_axes,
        'overall_quality_score': overall_quality_score,
        'score_axis_gaps': axis_gaps,
        'scoring_axis_summary': {'display_order': environment['scoring_policy'].get('axis_display_order', []), 'minimum_axis_scores': environment['scoring_policy'].get('minimum_axis_scores', {}), 'minimum_overall_quality_score_for_confident_result': environment['scoring_policy'].get('minimum_overall_quality_score_for_confident_result', 84), 'minimum_overall_quality_score_for_publish_ready_skill': environment['scoring_policy'].get('minimum_overall_quality_score_for_publish_ready_skill', 88)},
        'dispatch_decision': decisions['dispatch'],
        'review_decision': decisions['review'],
        'reopen_decision': decisions['reopen'],
        'done_decision': decisions['done'],
        'blocking_reasons': decisions['blocking_reasons'],
        'evidence_missing': decisions['evidence_missing'],
        'user_choice_required': decisions['user_choice'],
        'suggestion_mode': decisions['suggestion_mode'],
        'automation_execution_status': decisions['automation_status'],
    }


def run_full_loop(root: Path, report_rel: str, manifest_rel: str, issue_input: str, display_mode_override: str | None) -> tuple[dict[str, Any], int]:
    environment = load_runtime_environment(root, report_rel, manifest_rel, display_mode_override)
    if assembly_failed(environment['report']):
        return dict(DEFAULT_FAIL_DATA), 1

    # 记录整体开始时间
    total_start = time.time()
    action_timings = []

    # ---------- 步骤1：normalize ----------
    step_start = time.time()
    normalized_report = run_normalizer(root, issue_input)
    action_timings.append({'action': 'normalize', 'duration_ms': (time.time() - step_start) * 1000, 'retry_count': 0})

    route_drift_report = read_route_drift_report(root)
    issue = normalized_report['normalized_issue']
    issue_type = issue.get('issue_type', 'mixed')
    risks = list(issue.get('risk_flags', []))
    supported_issue_types = set(environment['route'].get('supported_issue_types', []))
    experience_summary = evaluate_experience_memory(issue, environment['experience_policy'])

    candidate_paths = apply_experience_bias(build_candidate_paths(issue, environment['route']), experience_summary)
    alternative_hypotheses = build_alternative_hypotheses(issue, candidate_paths, environment['creativity'])
    assignment = resolve_assignment(issue_type, risks, environment['route'], environment['display_lookup'])

    # 快速通道判断：低风险且高置信度
    fast_track = environment['fast_track_policy']
    is_low_risk = 'low' in risks and not any(r in ['medium','high','critical'] for r in risks)
    use_fast_track = (fast_track.get('enabled') and is_low_risk and
                      assignment.get('owner') and
                      (90 >= fast_track.get('min_owner_confidence', 90)))

    # ---------- 步骤2：工具模拟 ----------
    step_start = time.time()
    simulation = evaluate_simulations(root, issue, risks, issue_type, environment['route'], assignment['required_tools'])
    action_timings.append({'action': 'simulate_tools', 'duration_ms': (time.time() - step_start) * 1000, 'retry_count': 0})

    blockers = collect_blockers(issue, issue_type, supported_issue_types, assignment, normalized_report, simulation, simulation['route_conflicts_from_simulation'])
    managed_route_conflicts = manage_route_conflicts(blockers['route_conflicts'], experience_summary)

    track_competition = build_track_competition(issue, candidate_paths, alternative_hypotheses, blockers['route_conflicts'], risks, environment['exploration_mode_policy'], environment['display_lookup'])
    counterfactual_challenges = build_counterfactual_challenges(issue, candidate_paths, managed_route_conflicts, blockers['blocking_reasons'], environment['creativity'])
    mandatory_checklist = build_mandatory_checklist(issue, simulation['simulated_tool_results'], assignment['required_tools'])
    act_before_asking = build_act_before_asking(candidate_paths, simulation['simulated_tool_results'], blockers['blocking_reasons'], blockers['evidence_missing'])

    score_snapshot = build_score_snapshot(issue, issue_type, supported_issue_types, assignment, environment['route'], managed_route_conflicts, blockers['blocking_reasons'], simulation['simulated_tool_results'], normalized_report)
    scoring_axes, overall_quality_score, axis_gaps = compute_scoring_axes(issue, candidate_paths, alternative_hypotheses, counterfactual_challenges, mandatory_checklist, act_before_asking, managed_route_conflicts, blockers['blocking_reasons'], simulation['simulated_tool_results'], score_snapshot, 'review', 'dispatch', blockers['user_choice'], environment['scoring_policy'])
    decisions = compute_flow_decisions(assignment, environment['thresholds'], managed_route_conflicts, blockers['blocking_reasons'], overall_quality_score, environment['scoring_policy'], axis_gaps, simulation, blockers['evidence_missing'], blockers['user_choice'], issue_type)
    decisions['evidence_missing'] = blockers['evidence_missing']
    decisions['user_choice'] = blockers['user_choice']
    decisions['route_conflicts_display'] = blockers['route_conflicts']

    issue_stub = build_issue_stub(issue, issue_type, risks, assignment)
    open_issue_count = 1 + len(issue.get('secondary_findings', [])) + len(issue.get('reopened_findings', []))
    issue_scaling = apply_issue_scaling_policy(open_issue_count, environment['policy'].get('issue_scaling_policy', {}))
    linked_resources = build_linked_resources(assignment, environment['display_lookup'])
    role_disagreement = build_role_disagreement(track_competition, assignment['owner_name'], assignment['p8_name'], environment['disagreement_policy'].get('enabled', True))
    opportunity_discovery = build_opportunity_discovery(issue, blockers['route_conflicts'], decisions['blocking_reasons'], environment['opportunity_policy'])
    action_trace, current_work = build_action_trace(environment['display_mode'], issue_stub['issue_id'], assignment['owner_name'], assignment['p8_name'], linked_resources['linked_files_display'], linked_resources['linked_records'], decisions['blocking_reasons'], 1)

    # 增加进度百分比
    progress_percent = 0
    total_steps = 10
    if 'current_work_display' in current_work and isinstance(current_work, dict):
        current_work['progress_percent'] = progress_percent

    # 并行验证与体验（若非快速通道）
    if not use_fast_track and decisions['automation_status'] == 'pass':
        def run_validation(ctx):
            # 模拟 QA 验证
            return {'qa_result': 'pass'}
        def run_experience(ctx):
            # 模拟体验回放
            return {'experience_result': 'pass'}
        with ThreadPoolExecutor() as ex:
            futures = [ex.submit(run_validation, {}), ex.submit(run_experience, {})]
            for future in as_completed(futures):
                pass  # 实际应合并结果
        progress_percent = 70
        if 'current_work_display' in current_work and isinstance(current_work, dict):
            current_work['progress_percent'] = progress_percent

    parked_tickets, continuation_tickets, clearance_control = build_ticket_registries(issue_stub['issue_id'], issue, decisions['blocking_reasons'], open_issue_count, environment['clearance_policy'])

    data = build_report_data(environment, issue, issue_type, risks, normalized_report, route_drift_report, assignment, simulation, track_competition, role_disagreement, opportunity_discovery, experience_summary, candidate_paths, alternative_hypotheses, counterfactual_challenges, mandatory_checklist, act_before_asking, score_snapshot, scoring_axes, overall_quality_score, axis_gaps, decisions, issue_scaling, issue_stub, linked_resources, action_trace, current_work, parked_tickets, continuation_tickets, clearance_control, open_issue_count)
    data['performance'] = {
        'total_duration_ms': (time.time() - total_start) * 1000,
        'actions': action_timings
    }
    exit_code = 0 if decisions['automation_status'] == 'pass' else 1
    return data, exit_code