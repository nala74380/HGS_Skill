#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from tool_reasoning_engine import execute_tool_reasoning

DEFAULT_CHAIN = [
    'truth_owner_identification','p9_dispatch_review','required_tool_identification','risk_gate_check',
    'p8_execution_plan','qa_experience_sre_validation_plan','p9_rereview_path','reopen_or_closeout_condition_check','clearance_loop_bootstrap'
]


def slug(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-') or 'issue'


def normalize_release(path: str) -> str:
    return path if path.startswith('Release/') else f'Release/{path}'


def uniq(seq):
    out=[]
    for item in seq:
        if item not in out:
            out.append(item)
    return out


def ensure_list(v):
    if v is None: return []
    if isinstance(v, list): return v
    return [v]


def build_display_lookup(manifest: dict) -> dict:
    lookup = {}
    for bucket in ['roles','tools','protocols']:
        for item in manifest.get(bucket, []):
            if isinstance(item, dict) and item.get('file'):
                lookup[normalize_release(item['file'])] = item.get('display_name', Path(item['file']).stem)
    return lookup


def disp(path: str, lookup: dict) -> str:
    if not path:
        return ''
    return lookup.get(normalize_release(path), Path(path).stem)


def disp_list(paths, lookup: dict) -> list[str]:
    return [disp(p, lookup) for p in ensure_list(paths)]


def resolve_display_mode(explicit_mode: str | None, display_policy: dict) -> str:
    allowed={'compact','standard','forensic','off'}
    mode=(explicit_mode or display_policy.get('display_mode_default') or 'standard').strip().lower()
    return mode if mode in allowed else 'standard'


def resolve_display_mode_text(display_mode: str, display_policy: dict) -> str:
    label_map = display_policy.get("display_mode_label_map", {}) or {}
    return str(label_map.get(display_mode, display_policy.get("display_mode_exact_text", "全审计" if display_mode == "forensic" else display_mode)))

def build_action_trace(display_mode: str, ticket_id: str, owner_name: str, p8_name: str, linked_files_display: list[str], linked_records: list[str], blocking_reasons: list[str], priority_rank: int) -> tuple[list[dict], list[str]]:
    stages=[
        {'actor':'P10终审官','stage':'输入审查','ticket_id':ticket_id,'action':'逐文件逐行审查输入与上下文，形成问题排序与阻断定位'},
        {'actor':'P9派单官','stage':'派单编排','ticket_id':ticket_id,'action':f'派单给{p8_name}，核查联动文件、协议、记录与挂单策略'},
        {'actor':p8_name,'stage':'执行修改','ticket_id':ticket_id,'action':'执行修改并处理当前主单联动文件'},
        {'actor':'QA验证负责人','stage':'验证与体验','ticket_id':ticket_id,'action':'验证功能、回归风险与主路径正确性'},
        {'actor':'SRE可观测负责人','stage':'验证与体验','ticket_id':ticket_id,'action':'检查运行信号、可观测性与异常暴露'},
        {'actor':'P9派单官','stage':'持续派单/续改单','ticket_id':ticket_id,'action':'根据复审结果继续派单、挂单或回到原单'},
        {'actor':'P10终审官','stage':'P10复审','ticket_id':ticket_id,'action':'复审是否合格，若不合格则明确剩余问题并回单'},
        {'actor':'P10终审官','stage':'清零收口','ticket_id':ticket_id,'action':'检查主线清零、挂单登记、持续审核与持续派单是否仍需继续'},
    ]
    if display_mode == 'off':
        return [], []
    if display_mode == 'compact':
        current=[f"P10终审官｜阶段：输入审查：正在处理单号 {ticket_id}"]
        return stages[:2], current
    if display_mode == 'standard':
        current=[
            f"P10终审官｜阶段：输入审查：正在逐文件逐行审查单号 {ticket_id}",
            f"P9派单官｜阶段：派单编排：正在把单号 {ticket_id} 派给 {p8_name}",
            f"{p8_name}｜阶段：执行修改：正在修改 {'、'.join(linked_files_display)}",
            f"P10终审官｜阶段：P10复审：正在复审单号 {ticket_id}，当前阻断 {len(blocking_reasons)} 项",
        ]
        return stages, current
    current=[
        f"P10终审官｜阶段：输入审查｜单号：{ticket_id}｜优先级：P{priority_rank}：正在逐文件逐行审查输入与上下文，形成问题清单与排序",
        f"P9派单官｜阶段：派单编排｜单号：{ticket_id}：正在派单给 {p8_name}，联动文件 {'、'.join(linked_files_display)}，联动记录 {'、'.join(linked_records)}",
        f"{p8_name}｜阶段：执行修改｜单号：{ticket_id}：正在处理主单修改并同步联动文件",
        f"QA验证负责人 / SRE可观测负责人｜阶段：验证与体验｜单号：{ticket_id}：正在验证功能、回归、体验与运行信号",
        f"P10终审官｜阶段：P10复审｜单号：{ticket_id}：正在判定复审是否合格，当前阻断 {len(blocking_reasons)} 项",
        f"P9派单官｜阶段：持续派单/续改单｜单号：{ticket_id}：若复审不合格则继续回原单或拆子单，若合格则登记挂单与后续单",
        f"P10终审官｜阶段：清零收口｜单号：{ticket_id}：正在检查主线清零、挂单治理与持续审核是否完成",
    ]
    return stages, current


def build_ticket_registries(ticket_id: str, issue: dict, blocking_reasons: list[str], open_issue_count: int, clearance_policy: dict) -> tuple[list[dict], list[dict], dict]:
    parked=[]
    continuation=[]
    for idx, item in enumerate(issue.get('secondary_findings', []), start=1):
        parked.append({
            'ticket_id': f"{ticket_id}-P{idx}",
            'status': 'parked',
            'reason': 'secondary_finding_requires_followup',
            'reactivation_condition': 'mainline_ticket_review_completed',
            'summary': item.get('title') if isinstance(item, dict) else str(item)
        })
    for idx, item in enumerate(issue.get('reopened_findings', []), start=1):
        continuation.append({
            'ticket_id': f"{ticket_id}-R{idx}",
            'status': 'continuation',
            'reason': 'reopened_after_review',
            'summary': item.get('title') if isinstance(item, dict) else str(item)
        })
    control={
        'continuous_dispatch_required': clearance_policy.get('continuous_dispatch_required', True),
        'continuous_rereview_required': clearance_policy.get('continuous_rereview_required', True),
        'redispatch_after_each_failed_review': clearance_policy.get('redispatch_after_each_failed_review', True),
        'redispatch_after_new_findings': clearance_policy.get('redispatch_after_new_findings', True),
        'parked_ticket_registry_required': clearance_policy.get('parked_ticket_registry_required', True),
        'parked_ticket_not_equal_cleared': clearance_policy.get('parked_ticket_not_equal_cleared', True),
        'mainline_ticket_zero_required': clearance_policy.get('mainline_ticket_zero_required', True),
        'clearance_control_is_primary_theme': clearance_policy.get('clearance_control_is_primary_theme', True),
        'remaining_blocking_reasons': blocking_reasons,
        'open_issue_count': open_issue_count,
    }
    return parked, continuation, control


def apply_issue_scaling_policy(open_issue_count:int, scaling_policy:dict)->dict:
    threshold=scaling_policy.get('max_open_issues_before_wave_dispatch',12)
    per_wave=max(1, scaling_policy.get('max_subissues_per_wave',6))
    if open_issue_count <= threshold:
        return {'mode':'full_batch','wave_count':1,'issues_per_wave':open_issue_count,'summary_handoff_required':False}
    wave_count=(open_issue_count + per_wave - 1)//per_wave
    return {
        'mode': scaling_policy.get('fallback_mode_when_context_pressure_high','wave_dispatch_and_compact_state'),
        'wave_count': wave_count,
        'issues_per_wave': per_wave,
        'summary_handoff_required': scaling_policy.get('require_summary_handoff_between_waves', True),
        'pause_every_n_issues': scaling_policy.get('require_pause_and_compact_context_every_n_issues',5)
    }


def simulate_tool_result(tool_path: str, issue: dict, risk_flags: list[str], sim_policy: dict, repo_root: Path) -> dict:
    result = execute_tool_reasoning(repo_root, tool_path, issue, risk_flags)
    result['simulation_policy_snapshot'] = sim_policy
    return result


def run_normalizer(root: Path, issue_input: str) -> dict:
    output=root/'.hgs/normalized_issue_input.json'
    subprocess.run([sys.executable, str(root/'scripts/normalize_issue_input.py'), '--repo-root', str(root), '--issue-input', issue_input, '--output', str(output)], check=True, capture_output=True, text=True)
    return json.loads(output.read_text(encoding='utf-8'))


def build_candidate_paths(issue: dict, route: dict) -> list[dict]:
    owner_map=route.get('owner_by_issue_type',{})
    tools_map=route.get('tools_by_issue_type',{})
    max_candidates=max(1, route.get('execution_style_balance',{}).get('exploration_stage',{}).get('max_parallel_issue_type_candidates',3))
    out=[]
    for candidate in issue.get('candidate_issue_types',[])[:max_candidates]:
        itype=candidate['issue_type']
        owner_rel=owner_map.get(itype) or owner_map.get('mixed')
        tool_rels=tools_map.get(itype, tools_map.get('mixed',[]))
        out.append({'issue_type':itype,'owner_candidate':normalize_release(owner_rel) if owner_rel else '','tool_cluster_candidate':[normalize_release(x) for x in tool_rels],'score':candidate.get('score',0),'matched_keywords':candidate.get('matched_keywords',[]),'rationale':f'candidate issue type {itype} inferred from keywords'})
    return out


def build_alternative_hypotheses(issue: dict, candidate_paths: list[dict], creativity: dict) -> list[dict]:
    out=[]
    for i,c in enumerate(candidate_paths, start=1):
        out.append({'id':f'H{i}','issue_type':c.get('issue_type','mixed'),'claim':f"问题更可能属于 {c.get('issue_type','mixed')} 路线，而不是仅按单一现象解释。",'owner_candidate':c.get('owner_candidate',''),'tool_cluster_candidate':c.get('tool_cluster_candidate',[]),'rationale':c.get('rationale','candidate path')})
    fallbacks=[
        '当前主假设可能只解释了表象，根因可能在更上游的边界/上下文/配置层。',
        '当前现象可能由两个子问题叠加，而不是单一 owner 可以完整解释。',
    ]
    for j, text in enumerate(fallbacks, start=len(out)+1):
        if j > creativity.get('max_alternative_hypotheses', 4):
            break
        out.append({'id':f'H{j}','issue_type':'mixed','claim':text,'owner_candidate':'','tool_cluster_candidate':[],'rationale':'creativity fallback hypothesis'})
    return out


def build_counterfactual_challenges(issue: dict, candidate_paths: list[dict], route_conflicts: list[str], blocking_reasons: list[str], policy: dict) -> list[dict]:
    if not policy.get('enabled', True):
        return []
    challenges=[]
    for idx, candidate in enumerate(candidate_paths[:policy.get('max_counterfactual_challenges', 3)], start=1):
        challenges.append({
            'id': f'C{idx}',
            'challenge': f"如果 {candidate.get('issue_type','mixed')} 不是根因，当前证据是否仍能成立？",
            'expected_disproof_signal': 'tool cluster does not reinforce owner hypothesis',
            'linked_candidate_issue_type': candidate.get('issue_type','mixed'),
        })
    if route_conflicts or blocking_reasons:
        challenges.append({'id': f'C{len(challenges)+1}', 'challenge': '当前阻断项是否意味着需要退回到更高层问题定义？', 'expected_disproof_signal': 'blocking reasons remain after simulation'})
    return challenges[:policy.get('max_counterfactual_challenges', 3)]


def build_track_competition(issue: dict, candidate_paths: list[dict], alternative_hypotheses: list[dict], route_conflicts: list[str], risks: list[str], policy: dict, display_lookup: dict) -> dict:
    ranked=[]
    for idx, candidate in enumerate(candidate_paths, start=1):
        ranked.append({
            'rank': idx,
            'issue_type': candidate.get('issue_type','mixed'),
            'owner_candidate': disp(candidate.get('owner_candidate',''), display_lookup),
            'tool_cluster_candidate': disp_list(candidate.get('tool_cluster_candidate',[]), display_lookup),
            'score': candidate.get('score',0),
            'matched_keywords': candidate.get('matched_keywords',[]),
        })
    winner=ranked[0] if ranked else {'issue_type':'mixed','owner_candidate':'','tool_cluster_candidate':[],'score':0,'matched_keywords':[]}
    return {
        'enabled': policy.get('enabled', True),
        'winner_track': winner,
        'ranked_tracks': ranked,
        'alternative_hypotheses': alternative_hypotheses[:policy.get('max_alternative_hypotheses_to_display', 3)],
        'conflict_pressure': len(route_conflicts),
        'risk_pressure': len(risks),
    }


def build_role_disagreement(track_competition: dict, owner_name: str, p8_name: str, enabled: bool) -> dict:
    ranked=track_competition.get('ranked_tracks',[])
    if not enabled:
        return {'enabled': False, 'disagreement_log': [], 'role_alignment_summary': 'disabled'}
    log=[]
    if len(ranked) >= 2 and ranked[0].get('issue_type') != ranked[1].get('issue_type'):
        log.append({'from':'候选路径一','to':'候选路径二','reason':'candidate issue types differ and require rereview'})
    if owner_name and p8_name and owner_name == p8_name:
        log.append({'from':'owner','to':'executor','reason':'owner and executor collapse into same display role'})
    return {'enabled': True, 'disagreement_log': log, 'role_alignment_summary': '已保留角色分歧，当前以主线解释轨为主线推进'}


def build_opportunity_discovery(issue: dict, route_conflicts: list[str], blocking_reasons: list[str], policy: dict) -> dict:
    requested=issue.get('current_question') or issue.get('title','')
    higher='优先解决导致多条症状同时出现的上游上下文/边界/配置问题，而不是只修表层现象'
    score=78 if policy.get('enabled',True) else 0
    return {
        'requested_problem':requested,
        'observed_problem':'当前问题可能是症状问题与边界问题叠加',
        'discovered_higher_leverage_problem':higher,
        'symptom_vs_root_gap':'用户当前描述更偏症状，系统识别到更高杠杆的上游问题',
        'requested_action':'处理当前显性问题',
        'actually_best_action':'优先检查并修复更高杠杆的上游问题，再回落验证表层现象',
        'opportunity_discovery_score':score,
        'opportunity_priority_reason':'高杠杆问题若先处理，可能连带减少后续 reopen 与重复修补',
        'defer_main_request_reason_if_any':'' if not route_conflicts and not blocking_reasons else '当前仍保留主问题推进，但已记录更高杠杆机会供复审与人工决策'
    }


def compute_scoring_axes(issue: dict, candidate_paths: list, alternative_hypotheses: list, counterfactual_challenges: list, mandatory_checklist: list, act_before_asking: dict, route_conflicts: list, blocking_reasons: list, simulated_tool_results: list, score: dict, review: str, dispatch: str, user_choice: str, policy: dict) -> tuple[dict, float, list]:
    exploration_breadth=min(100, 35 + 12*len(candidate_paths) + 10*len(alternative_hypotheses))
    counterfactual_rigor=min(100, 45 + 22*len(counterfactual_challenges) + 4*sum(1 for x in mandatory_checklist if x.get('status')=='done'))
    act_before_asking_rigor=min(100, 48 + 10*len(act_before_asking.get('actions_taken_before_asking',[])) + (10 if user_choice=='no' else 0) + (8 if not any('required_inputs_missing' in x for x in blocking_reasons) else 0) + (8 if len(simulated_tool_results) >= 2 else 0))
    convergence_quality=max(0, min(100, 78 + (8 if dispatch=='dispatch' else -18) + (8 if review=='review' else -20) - 10*len(route_conflicts)))
    execution_readiness=max(0, min(100, round((score.get('tool_coverage_score',0)*0.45)+(score.get('evidence_completeness_score',0)*0.35)+(score.get('owner_confidence',0)*0.20))))
    user_fit=max(0, min(100, round(30 + (score.get('user_input_friendliness_score',0)*0.45) + (8 if issue.get('current_question') else 0) + (8 if issue.get('acceptance_criteria') else 0) + (8 if issue.get('critical_paths') else 0) + (6 if issue.get('source_of_truth') else 0) + (6 if issue.get('max_change_boundary') else 0))))
    avg_conf=round(sum(r.get('confidence',0) for r in simulated_tool_results)/max(1,len(simulated_tool_results))*100)
    result_adequacy=max(0, min(100, round((score.get('route_stability_score',0)*0.35)+(score.get('closeout_readiness_score',0)*0.25)+(avg_conf*0.20)+((100-len(blocking_reasons)*8)*0.20))))
    axes={
        'exploration_breadth': exploration_breadth,
        'counterfactual_rigor': counterfactual_rigor,
        'act_before_asking_rigor': act_before_asking_rigor,
        'convergence_quality': convergence_quality,
        'execution_readiness': execution_readiness,
        'user_fit': user_fit,
        'result_adequacy': result_adequacy,
    }
    weights=policy.get('axis_weights',{})
    total=0.0
    for k,v in axes.items():
        total += float(weights.get(k,0))*v
    overall=round(total,2)
    mins=policy.get('minimum_axis_scores',{})
    below=[k for k,v in axes.items() if v < mins.get(k,0)]
    return axes, overall, below


def build_mandatory_checklist(issue: dict, simulated_tool_results: list[dict], required_tools: list[str]) -> list[dict]:
    findings={f for result in simulated_tool_results for f in result.get('findings',[])}
    checks=[
        ('error_and_signal_review', bool(issue.get('current_question'))),
        ('environment_and_context_review', bool(issue.get('source_of_truth'))),
        ('dependency_and_contract_review', bool(required_tools)),
        ('alternative_path_search', bool(simulated_tool_results)),
        ('documentation_and_history_review', bool(issue.get('source_of_truth'))),
        ('rollback_and_safety_review', bool(issue.get('max_change_boundary'))),
        ('root_cause_and_verification_review', bool(issue.get('acceptance_criteria')) and bool(issue.get('critical_paths'))),
    ]
    return [{'item':name,'status':'done' if ok else 'missing','evidence':sorted(list(findings))[:3] if findings else []} for name,ok in checks]


def build_act_before_asking(candidate_paths: list[dict], simulated_tool_results: list[dict], blocking_reasons: list[str], evidence_missing: list[str]) -> dict:
    return {'internal_actions_attempted':['候选 issue type 推断','候选 owner/tool 路径收敛','模拟工具结果生成','验证与体验门槛评估','复审与清零条件评估'],'candidate_paths_count':len(candidate_paths),'simulated_tool_results_count':len(simulated_tool_results),'remaining_blockers':blocking_reasons,'remaining_evidence_gaps':evidence_missing,'ask_user_only_if_internal_options_exhausted':True}


# ==================== 快速通道辅助函数 ====================
def should_use_fast_track(issue: dict, score_snapshot: dict, fast_track_policy: dict) -> bool:
    """Determine if fast track should be used (skip validation and experience)."""
    if not fast_track_policy.get('enabled'):
        return False
    risks = issue.get('risk_flags', [])
    # Check if only low risk (no medium/high/critical)
    is_low_risk = 'low' in risks and not any(r in {'medium','high','critical'} for r in risks)
    if not is_low_risk:
        return False
    min_conf = fast_track_policy.get('min_owner_confidence', 90)
    owner_conf = score_snapshot.get('owner_confidence', 0)
    return owner_conf >= min_conf


def build_report_data(environment: dict[str, Any], issue: dict[str, Any], issue_type: str, risks: list[str], normalized_report: dict[str, Any], route_drift_report: dict[str, Any], assignment: dict[str, Any], simulation: dict[str, Any], track_competition: dict[str, Any], role_disagreement: dict[str, Any], opportunity_discovery: dict[str, Any], experience_summary: dict[str, Any], candidate_paths: list[dict[str, Any]], alternative_hypotheses: list[dict[str, Any]], counterfactual_challenges: list[dict[str, Any]], mandatory_checklist: list[dict[str, Any]], act_before_asking: dict[str, Any], score_snapshot: dict[str, Any], scoring_axes: dict[str, Any], overall_quality_score: float, axis_gaps: list[str], decisions: dict[str, Any], issue_scaling: dict[str, Any], issue_stub: dict[str, Any], linked_resources: dict[str, Any], action_trace: list[dict[str, Any]], current_work: dict[str, Any], parked_tickets: list[dict[str, Any]], continuation_tickets: list[dict[str, Any]], clearance_control: dict[str, Any], open_issue_count: int) -> dict[str, Any]:
    display_lookup = environment['display_lookup']
    policy = environment['policy']
    route = environment['route']
    clearance_policy = environment['clearance_policy']
    display_mode = environment['display_mode']
    conversation_display_policy = environment['conversation_display_policy']
    fast_track_policy = environment.get('fast_track_policy', {})
    priority_rank = 1

    # 快速通道判断
    use_fast = should_use_fast_track(issue, score_snapshot, fast_track_policy)

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

    # 根据快速通道决定是否创建验证计划和体验计划
    validation_plan_created = 'yes' if (issue.get('critical_paths') and issue.get('acceptance_criteria') and not use_fast) else 'no'
    experience_plan_created = 'yes' if (not use_fast) else 'no'

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
        'validation_plan_created': validation_plan_created,
        'validation_plan': {'required_level': issue.get('verification_target', 'L3'), 'critical_paths': issue.get('critical_paths', [])},
        'experience_plan_created': experience_plan_created,
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