#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

OWNER = {
  'rule':'Release/roles/11_Product_Business_Rules_Owner_SKILL.md',
  'auth':'Release/roles/12_Auth_Identity_Owner_SKILL.md',
  'billing':'Release/roles/13_Billing_Entitlement_Owner_SKILL.md',
  'release':'Release/roles/14_Release_Config_Owner_SKILL.md',
  'security':'Release/roles/15_Security_Risk_Owner_SKILL.md',
  'agent':'Release/roles/16_Agent_Operations_Owner_SKILL.md',
  'enduser':'Release/roles/17_EndUser_Support_Owner_SKILL.md',
  'control_plane':'Release/roles/18_Control_Plane_Owner_SKILL.md',
  'execution_plane':'Release/roles/19_Execution_Plane_Owner_SKILL.md',
  'frontend':'Release/roles/32B_P8_Frontend_Logic_Engineer_SKILL.md',
  'console':'Release/roles/33A_P8_Console_Runtime_Engineer_SKILL.md',
  'worker':'Release/roles/34_P8_LanrenJingling_PUA_SKILL.md',
  'qa':'Release/roles/37_QA_Validation_Owner_SKILL.md',
  'sre':'Release/roles/38_SRE_Observability_Owner_SKILL.md',
  'docs':'Release/roles/39_Knowledge_Documentation_Owner_SKILL.md',
  'mixed':'Release/roles/20_P9_Principal_SKILL.md'
}
TOOLS = {
  'rule':['Release/tools/70_Business_Rule_Matrix_SKILL.md','Release/tools/71_State_Machine_Consistency_SKILL.md'],
  'auth':['Release/tools/72_JWT_Inspector_SKILL.md','Release/tools/74_Session_Refresh_Trace_SKILL.md','Release/tools/110_Authorization_Bypass_Path_Reviewer_SKILL.md'],
  'billing':['Release/tools/76_Billing_Ledger_Reconciler_SKILL.md','Release/tools/77_Quota_Usage_Analyzer_SKILL.md','Release/tools/78_Freeze_Reversal_Diagnoser_SKILL.md'],
  'frontend':['Release/tools/79_API_Contract_Diff_SKILL.md','Release/tools/82_Network_Trace_Reviewer_SKILL.md','Release/tools/85_UI_Surface_Audit_SKILL.md'],
  'console':['Release/tools/88_Console_Auth_Flow_Trace_SKILL.md','Release/tools/89_Project_Context_Drift_SKILL.md','Release/tools/90_StepUp_Resume_Checker_SKILL.md'],
  'worker':['Release/tools/91_Worker_Identity_Stability_SKILL.md','Release/tools/92_Heartbeat_Gap_Analyzer_SKILL.md','Release/tools/98_Trace_Correlation_SKILL.md'],
  'release':['Release/tools/101_Compatibility_Matrix_SKILL.md','Release/tools/109_High_Risk_Action_Guard_Checker_SKILL.md'],
  'qa':['Release/tools/95_Test_Matrix_Builder_SKILL.md','Release/tools/96_Regression_Checklist_SKILL.md'],
  'docs':['Release/tools/106_SOP_Generator_SKILL.md','Release/tools/107_Protocol_Field_Completeness_Checker_SKILL.md'],
  'mixed':['Release/tools/108_Chain_Route_Simulator_SKILL.md','Release/tools/114_Score_Decision_Engine_SKILL.md','Release/tools/115_Full_Issue_Clearance_Controller_SKILL.md']
}
RISK = {
  'high_risk_action':['Release/tools/109_High_Risk_Action_Guard_Checker_SKILL.md'],
  'destructive_change':['Release/tools/109_High_Risk_Action_Guard_Checker_SKILL.md','Release/tools/111_Bulk_Action_Safety_Reviewer_SKILL.md'],
  'auth_bypass':['Release/tools/110_Authorization_Bypass_Path_Reviewer_SKILL.md'],
  'scope_risk':['Release/tools/110_Authorization_Bypass_Path_Reviewer_SKILL.md'],
  'runtime_stability':['Release/tools/113_Runtime_Incident_Replayer_SKILL.md','Release/tools/98_Trace_Correlation_SKILL.md'],
  'incident':['Release/tools/113_Runtime_Incident_Replayer_SKILL.md','Release/tools/98_Trace_Correlation_SKILL.md'],
  'bulk_action':['Release/tools/111_Bulk_Action_Safety_Reviewer_SKILL.md','Release/tools/112_Audit_Log_Consistency_Checker_SKILL.md'],
  'audit_required':['Release/tools/112_Audit_Log_Consistency_Checker_SKILL.md']
}
ALWAYS = ['Release/tools/114_Score_Decision_Engine_SKILL.md','Release/tools/115_Full_Issue_Clearance_Controller_SKILL.md','Release/tools/107_Protocol_Field_Completeness_Checker_SKILL.md']

def slug(t:str)->str: return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-') or 'issue'

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',default='.'); ap.add_argument('--report',default='.hgs/assembly_report.json'); ap.add_argument('--issue-input',required=True); ap.add_argument('--output',default='.hgs/full_loop_dry_run.json'); ap.add_argument('--strict',action='store_true'); args=ap.parse_args()
    root=Path(args.repo_root).resolve(); report=json.loads((root/args.report).read_text(encoding='utf-8'))
    if report.get('full_release_assembly_status')!='pass':
        data={'mode':'full_loop','automation_execution_status':'fail','blocking_reasons':['full_release_assembly_status != pass'],'user_choice_required':'no','suggestion_mode':'no'}
        print(json.dumps(data,ensure_ascii=False,indent=2)); return 1 if args.strict else 0
    issue=json.loads((root/args.issue_input).read_text(encoding='utf-8'))
    t=issue.get('issue_type','mixed'); risks=list(issue.get('risk_flags',[])); owner=OWNER.get(t,OWNER['mixed'])
    req=[]
    for x in TOOLS.get(t,TOOLS['mixed'])+sum((RISK.get(r,[]) for r in risks),[])+ALWAYS:
        if x not in req: req.append(x)
    score={'owner_confidence':85 if owner else 25,'route_stability_score':80 if owner else 35,'tool_coverage_score':92 if req else 40,'evidence_completeness_score':min(100,40+(15 if issue.get('acceptance_criteria') else 0)+(15 if issue.get('critical_paths') else 0)+(10 if issue.get('source_of_truth') else 0)+(10 if issue.get('max_change_boundary') else 0)),'reopen_risk_score':20 if issue.get('verification_target') in {'L3','L4'} else 45,'closeout_readiness_score':15}
    dispatch='dispatch' if score['owner_confidence']>=70 and score['tool_coverage_score']>=85 else 'hold'
    validation = bool(issue.get('critical_paths') or issue.get('acceptance_criteria'))
    user_choice='yes' if 'user_choice_required' in risks else 'no'; suggestion='no'
    status='pass' if owner and req and dispatch=='dispatch' and validation and user_choice=='no' else 'fail'
    title=issue.get('title') or issue.get('current_question') or issue.get('summary') or 'unnamed issue'
    stub={'issue_id':issue.get('issue_id') or f"DRYRUN-{slug(title)[:40]}",'title':title,'issue_type':t,'problem_statement':issue.get('current_question') or title,'owner':owner,'source_of_truth':issue.get('source_of_truth',[]),'risk_flags':risks,'status':'stub_created'}
    secondary=list(issue.get('secondary_findings',[])); reopened=list(issue.get('reopened_findings',[])); open_n=1+len(secondary)+len(reopened)
    data={
      'mode':'full_loop','chain':['truth_owner_identification','p9_dispatch_review','required_tool_identification','risk_gate_check','p8_execution_plan','qa_experience_sre_validation_plan','p9_rereview_path','reopen_or_closeout_condition_check','clearance_loop_bootstrap'],
      'issue_stub_created':'yes','owner_identified':'yes','owner_name':owner,'required_tools_identified':'yes','required_tools':req,'risk_gates_checked':'yes',
      'risk_gate_plan':{'high_risk_guard_gate':any(r in {'high_risk_action','destructive_change'} for r in risks),'auth_bypass_guard_gate':any(r in {'auth_bypass','scope_risk'} for r in risks),'runtime_stability_gate':any(r in {'runtime_stability','incident'} for r in risks),'must_run_tool_gate':bool(req)},
      'exec_plan_created':'yes','exec_plan':{'owner':owner,'max_change_boundary':issue.get('max_change_boundary','provisional'),'success_definition':issue.get('acceptance_criteria',[])},
      'validation_plan_created':'yes' if validation else 'no','validation_plan':{'required_level':issue.get('verification_target','L3'),'critical_paths':issue.get('critical_paths',[])},
      'experience_plan_created':'yes','experience_plan':{'experience_protocols':['Release/protocols/40_P8_Agent_Experience_Protocol.md','Release/protocols/41_P8_EndUser_Experience_Protocol.md'],'replay_required_when_real_feedback_missing':True},
      'rereview_path_created':'yes','rereview_path':{'p9_rereview':True,'p10_on_demand':True,'protocol':'Release/protocols/50_RE_REVIEW_PROTOCOL.md'},
      'issue_inventory_created':'yes','issue_inventory':{'open_issue_count_initialized':open_n,'items':[stub]+secondary+reopened},'clearance_gate_created':'yes','clearance_loop_created':'yes',
      'clearance_loop':{'controller':'Release/tools/115_Full_Issue_Clearance_Controller_SKILL.md','rule':'continue until open_issue_count = 0','next_required_action':'dispatch_issue_to_owner' if status=='pass' else ('user_choice_required' if user_choice=='yes' else 'resolve_blocking_reasons')},
      'route_simulation':{'simulated_route':[{'step':1,'actor':owner,'action':'truth_owner_identification'},{'step':2,'actor':'Release/roles/20_P9_Principal_SKILL.md','action':'dispatch_review'},{'step':3,'actor':req,'action':'must_run_tools'},{'step':4,'actor':'Release/roles/37_QA_Validation_Owner_SKILL.md','action':'validation_plan'},{'step':5,'actor':'Release/roles/39_Knowledge_Documentation_Owner_SKILL.md','action':'docs_sink'}],'route_conflicts':[],'must_trigger_tools':req,'likely_stop_conditions':[]},
      'score_snapshot':score,'dispatch_decision':dispatch,'review_decision':'review' if dispatch=='dispatch' else 'blocked','reopen_decision':'reopen_unlikely','done_decision':'not_done','blocking_reasons':[],'user_choice_required':user_choice,'suggestion_mode':suggestion,'automation_execution_status':status
    }
    out=root/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(data,ensure_ascii=False,indent=2)); return 1 if args.strict and status!='pass' else 0

if __name__=='__main__': raise SystemExit(main())
