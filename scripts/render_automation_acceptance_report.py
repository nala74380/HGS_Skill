#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def yn(v):
    if isinstance(v, str) and v.lower() in {'yes','no'}: return v.lower()
    return 'yes' if bool(v) else 'no'

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',default='.'); ap.add_argument('--input',default='.hgs/full_loop_dry_run.json'); ap.add_argument('--output',default='.hgs/automation_execution_acceptance_report.json'); ap.add_argument('--strict',action='store_true'); args=ap.parse_args()
    root=Path(args.repo_root).resolve(); dry=json.loads((root/args.input).read_text(encoding='utf-8'))
    inv=dry.get('issue_inventory',{}); loop=dry.get('clearance_loop',{})
    p9_dispatch_checklist=dry.get('p9_dispatch_checklist',{})
    report={
      'response_header': dry.get('response_header','自动化链路：已开启'),
      'display_mode': dry.get('display_mode','forensic'),
      'display_mode_text': dry.get('display_mode_text','全审计'),
      'issue_stub_created':yn(dry.get('issue_stub_created')),
      'owner_identified':yn(dry.get('owner_identified')),
      'owner_name':dry.get('owner_name',''),
      'ticket_id': dry.get('ticket_id',''),
      'ticket_priority_rank': dry.get('ticket_priority_rank',''),
      'problem_statement': dry.get('problem_statement',''),
      'p8_executor_skill':dry.get('p8_executor_skill',''),
      'p8_executor_skill_display':dry.get('p8_executor_skill_display') or dry.get('p8_executor_skill',''),
      'required_tools_identified':yn(dry.get('required_tools_identified')),
      'required_tools':dry.get('required_tools',[]),
            'risk_gates_checked':yn(dry.get('risk_gates_checked')),
      'exec_plan_created':yn(dry.get('exec_plan_created')),
      'validation_plan_created':yn(dry.get('validation_plan_created')),
      'experience_plan_created':yn(dry.get('experience_plan_created')),
      'rereview_path_created':yn(dry.get('rereview_path_created')),
      'clearance_loop_created':yn(dry.get('clearance_loop_created')),
      'issue_inventory_created':yn(dry.get('issue_inventory_created')),
      'clearance_gate_created':yn(dry.get('clearance_gate_created')),
      'open_issue_count_initialized':inv.get('open_issue_count_initialized',''),
      'next_required_action':loop.get('next_required_action',''),
      'automation_execution_status':dry.get('automation_execution_status','fail'),
      'judgements':{
        'is_in_automation_chain':'yes' if dry.get('automation_execution_status')=='pass' else 'no',
        'issue_ledger_established':'yes' if inv.get('items') else 'no',
        'owner_established':yn(dry.get('owner_identified')),
        'tool_plan_established':yn(dry.get('required_tools_identified')),
        'gate_plan_established':'yes' if dry.get('risk_gate_plan') else 'no',
        'exec_plan_established':yn(dry.get('exec_plan_created')),
        'validation_experience_rereview_clearance_path_established':'yes' if all([dry.get('validation_plan_created')=='yes',dry.get('experience_plan_created')=='yes',dry.get('rereview_path_created')=='yes',dry.get('clearance_loop_created')=='yes']) else 'no',
        'continue_until_open_issue_zero_default_rule':'yes' if loop.get('rule')=='continue until open_issue_count = 0' else 'no',
        'still_asking_user_to_pick_a_or_b':'yes' if dry.get('user_choice_required')=='yes' else 'no',
        'still_stuck_in_suggestion_mode':'yes' if dry.get('suggestion_mode')=='yes' else 'no'
      },
      'score_snapshot':dry.get('score_snapshot',{}),
      'scoring_axes': dry.get('scoring_axes', {}),
      'overall_quality_score': dry.get('overall_quality_score', 0),
      'score_axis_gaps': dry.get('score_axis_gaps', []),
      'scoring_axis_summary': dry.get('scoring_axis_summary', {}),
      'actor_action_trace':dry.get('action_trace',[]),
      'current_work_display':dry.get('current_work_display',[]),
      'p9_dispatch_checklist':p9_dispatch_checklist,
      'issue_priority_ranking': dry.get('issue_priority_ranking', []),
      'review_result': dry.get('review_result', {}),
      'clearance_loop': dry.get('clearance_loop', {}),
      'clearance_control': dry.get('clearance_control', {}),
      'issue_inventory': dry.get('issue_inventory', {})
    }
    out=root/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(report,ensure_ascii=False,indent=2)); return 1 if args.strict and report['automation_execution_status']!='pass' else 0

if __name__=='__main__': raise SystemExit(main())
