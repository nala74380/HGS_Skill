#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

REQUIRED_TOP_LEVEL = {'package_name':str,'package_version':str,'entrypoint':str,'default_route_mode':str,'load_order':list,'tool_load_order':list,'documentation_load_order':list,'roles':list,'tools':list,'protocols':list,'governance_docs':list,'risk_gates':list,'automation_policy':dict}
REQUIRED_AUTOMATION = {'action_protocol':str,'clearance_protocol':str,'active_actions':list,'active_action_batches':list,'thresholds':dict,'score_decision_rules':dict,'runtime_route_policy':dict,'scoring_axes_policy':dict,'experience_memory_policy':dict,'issue_scaling_policy':dict,'package_cleanliness_policy':dict,'adversarial_review_policy':dict,'conversation_display_policy':dict}
REQUIRED_ROUTE_POLICY = {'owner_by_issue_type':dict,'tools_by_issue_type':dict,'tools_by_risk_flag':dict,'always_include_tools':list,'required_input_fields':list,'recommended_input_fields':list,'supported_issue_types':list,'inferable_input_fields':list,'minimum_user_input_fields':list,'tool_execution_simulation_policy':dict,'issue_type_inference_keywords':dict,'risk_flag_inference_keywords':dict,'simulation_quality_policy':dict,'p8_executor_by_issue_type':dict,'display_actor_policy':dict,'creativity_amplification_policy':dict,'exploration_mode_policy':dict,'opportunity_discovery_policy':dict,'role_disagreement_policy':dict}


def ensure_rel_release(path: str) -> bool:
    return isinstance(path, str) and not path.startswith('Release/') and '/' in path and '..' not in path


def validate_type(name, value, expected, errors):
    if not isinstance(value, expected):
        errors.append(f'{name} must be {expected.__name__}')




def validate_conversation_display_policy(policy, errors):
    required = {
        'status_header_exact_text':str,
        'display_mode_default':str,
        'display_mode_exact_text':str,
        'display_mode_label_map':dict,
        'display_mode_command_keywords':dict,
        'forensic_fields_required':list,
        'show_stage_label':bool,
        'show_ticket_binding':bool,
        'show_root_cause_hints':bool,
    }
    for key, typ in required.items():
        if key not in policy:
            errors.append(f'missing conversation_display_policy key: {key}')
        elif not isinstance(policy.get(key), typ):
            errors.append(f'conversation_display_policy.{key} must be {typ.__name__}')


def validate_full_issue_clearance_policy(policy, errors):
    required_bool_keys = [
        'continuous_dispatch_required',
        'redispatch_after_each_failed_review',
        'redispatch_after_new_findings',
        'continuous_rereview_required',
        'review_loop_until_ticket_reaches_terminal_state',
        'parked_ticket_must_have_reason',
        'parked_ticket_must_have_reactivation_condition',
        'parked_ticket_not_equal_cleared',
        'mainline_ticket_zero_required',
        'parked_ticket_registry_required',
        'closeout_forbidden_if_untracked_parked_tickets_exist',
        'clearance_control_is_primary_theme',
    ]
    for key in required_bool_keys:
        if key not in policy:
            errors.append(f'missing full_issue_clearance_policy key: {key}')
        elif not isinstance(policy.get(key), bool):
            errors.append(f'full_issue_clearance_policy.{key} must be bool')

def validate_experience_memory_policy(policy, errors):
    required = {'enabled':bool,'mode':str,'support_track_name':str,'challenge_track_name':str,'states':list,'auto_bias_downgrade_enabled':bool,'promotion_requires_p10_review':bool,'retirement_requires_p10_review':bool,'human_review_required_for_high_risk_domain':bool,'high_risk_domains':list,'experience_bias_max_influence':int,'candidate_experience_patterns':list,'approved_experience_patterns':list,'failure_mode_catalog':list}
    for key, typ in required.items():
        if key not in policy:
            errors.append(f'missing experience_memory_policy key: {key}')
        elif not isinstance(policy.get(key), typ):
            errors.append(f'experience_memory_policy.{key} must be {typ.__name__}')


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',default='.'); ap.add_argument('--manifest',default='Release/MANIFEST.json'); ap.add_argument('--output',default='.hgs/manifest_schema_report.json'); ap.add_argument('--strict',action='store_true'); args=ap.parse_args()
    root=Path(args.repo_root).resolve(); manifest=json.loads((root/args.manifest).read_text(encoding='utf-8')); errors=[]
    for key, typ in REQUIRED_TOP_LEVEL.items():
        if key not in manifest: errors.append(f'missing top-level key: {key}')
        else: validate_type(key, manifest[key], typ, errors)
    for seq_key in ['load_order','tool_load_order','documentation_load_order']:
        for idx, item in enumerate(manifest.get(seq_key, [])):
            if seq_key == 'load_order' and item in {'MANIFEST.json','00_HGS_Master_Loader.md'}:
                continue
            if not ensure_rel_release(item): errors.append(f'{seq_key}[{idx}] must be a relative Release path token')
    for bucket in ['roles','tools','protocols']:
        for idx, item in enumerate(manifest.get(bucket, [])):
            if not isinstance(item, dict):
                errors.append(f'{bucket}[{idx}] must be object')
                continue
            base_required = ['id','file','display_name'] if bucket == 'protocols' else ['id','file','layer','display_name']
            for req in base_required:
                if req not in item or not item.get(req):
                    errors.append(f'{bucket}[{idx}] missing {req}')
            if bucket in {'roles','tools'}:
                if 'capability_tags' not in item or not isinstance(item.get('capability_tags'), list) or not item.get('capability_tags'):
                    errors.append(f'{bucket}[{idx}] capability_tags missing or empty')
                if 'primary_issue_types' not in item or not isinstance(item.get('primary_issue_types'), list) or not item.get('primary_issue_types'):
                    errors.append(f'{bucket}[{idx}] primary_issue_types missing or empty')
            if bucket=='roles' and ('role_kind' not in item or not isinstance(item.get('role_kind'), str) or not item.get('role_kind')):
                errors.append(f'roles[{idx}] role_kind missing')
    policy=manifest.get('automation_policy', {})
    for key, typ in REQUIRED_AUTOMATION.items():
        if key not in policy:
            errors.append(f'missing automation_policy key: {key}')
        else:
            validate_type(f'automation_policy.{key}', policy[key], typ, errors)
    package_clean = policy.get('package_cleanliness_policy', {})
    required_package_clean = {
        'archive_scope_name': str,
        'runtime_scope_name': str,
        'require_dual_cleanliness_checks': bool,
        'clean_archive_forbidden_paths': list,
        'runtime_workspace_forbidden_paths': list,
        'required_dotfiles': list,
        'require_single_artifact_root': bool,
        'single_artifact_root': str,
        'clean_archive_must_be_verified_before_release': bool,
        'runtime_workspace_must_be_reported_separately': bool,
        'enforce_clean_package_before_release': bool,
    }
    for key, typ in required_package_clean.items():
        if key not in package_clean:
            errors.append(f'missing package_cleanliness_policy key: {key}')
        elif not isinstance(package_clean.get(key), typ):
            errors.append(f'package_cleanliness_policy.{key} must be {typ.__name__}')
    adversarial = policy.get('adversarial_review_policy', {})
    for key, typ in {'enabled':bool,'checklists':list,'require_hostile_review_before_release':bool}.items():
        if key not in adversarial:
            errors.append(f'missing adversarial_review_policy key: {key}')
        elif not isinstance(adversarial.get(key), typ):
            errors.append(f'adversarial_review_policy.{key} must be {typ.__name__}')
    scaling = policy.get('issue_scaling_policy', {})
    required_scaling = {
        'max_open_issues_before_wave_dispatch': int,
        'max_subissues_per_wave': int,
        'require_wave_planning_when_issue_inventory_exceeds_threshold': bool,
        'wave_priority_order': list,
        'require_pause_and_compact_context_every_n_issues': int,
        'require_summary_handoff_between_waves': bool,
        'fallback_mode_when_context_pressure_high': str,
        'forbid_full_parallel_execution_when_context_pressure_high': bool,
    }
    for key, typ in required_scaling.items():
        if key not in scaling:
            errors.append(f'missing issue_scaling_policy key: {key}')
        elif not isinstance(scaling.get(key), typ):
            errors.append(f'issue_scaling_policy.{key} must be {typ.__name__}')
    route=policy.get('runtime_route_policy', {})
    for key, typ in REQUIRED_ROUTE_POLICY.items():
        if key not in route: errors.append(f'missing runtime_route_policy key: {key}')
        else: validate_type(f'runtime_route_policy.{key}', route[key], typ, errors)
    owner_by_issue=route.get('owner_by_issue_type',{}); tools_by_issue=route.get('tools_by_issue_type',{}); tools_by_risk=route.get('tools_by_risk_flag',{})
    supported=set(route.get('supported_issue_types',[]))
    for issue_type in supported:
        if issue_type not in owner_by_issue: errors.append(f'supported issue_type missing owner mapping: {issue_type}')
        if issue_type not in tools_by_issue: errors.append(f'supported issue_type missing tool mapping: {issue_type}')
        if issue_type not in route.get('p8_executor_by_issue_type',{}): errors.append(f'supported issue_type missing p8 executor mapping: {issue_type}')
    for val in owner_by_issue.values():
        if not ensure_rel_release(val): errors.append('owner mapping must be a relative Release path token')
    minimum=set(route.get('minimum_user_input_fields',[])); required=set(route.get('required_input_fields',[])); inferable=set(route.get('inferable_input_fields',[]))
    if not minimum.issubset(required): errors.append('minimum_user_input_fields must be subset of required_input_fields')
    if not inferable.issubset(required): errors.append('inferable_input_fields must be subset of required_input_fields')
    for mapping_name, mapping in [('tools_by_issue_type',tools_by_issue),('tools_by_risk_flag',tools_by_risk)]:
        for map_key, items in mapping.items():
            if not isinstance(items,list) or not items: errors.append(f'{mapping_name}.{map_key} must be non-empty list'); continue
            for item in items:
                if not ensure_rel_release(item): errors.append(f'{mapping_name}.{map_key} values must be relative Release path tokens')
    display=route.get('display_actor_policy',{})
    if not isinstance(display.get('use_skill_display_name_first'), bool): errors.append('display_actor_policy.use_skill_display_name_first must be bool')
    creativity=route.get('creativity_amplification_policy', {})
    req_creativity={'require_min_alternative_hypotheses':int,'require_min_counterfactual_challenges':int,'require_blue_team_challenge':bool,'require_act_before_asking_summary':bool,'mandatory_checklist':list,'exploration_prompts':list,'escalation_levels':dict,'loop_control':dict}
    for key, typ in req_creativity.items():
        if key not in creativity: errors.append(f'missing creativity_amplification_policy key: {key}')
        elif not isinstance(creativity[key], typ): errors.append(f'creativity_amplification_policy.{key} must be {typ.__name__}')
    validate_experience_memory_policy(policy.get('experience_memory_policy', {}), errors)
    schema_file_exists=(root/'scripts/manifest.schema.json').exists()
    if not schema_file_exists: errors.append('scripts/manifest.schema.json is missing')
    report={'manifest_schema_status':'pass' if not errors else 'fail','schema_file_exists':schema_file_exists,'errors':errors}
    out=root/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if args.strict and errors else 0

if __name__=='__main__':
    raise SystemExit(main())
