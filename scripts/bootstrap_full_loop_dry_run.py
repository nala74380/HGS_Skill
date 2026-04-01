#!/usr/bin/env python3
"""Bootstrap a full_loop dry-run from a verified Release assembly.

This script does not execute fixes. It produces the automation bootstrap artifacts
needed to prove the chain can start automatically after assembly passes.

Usage:
  python scripts/bootstrap_full_loop_dry_run.py \
      --repo-root . \
      --report .hgs/assembly_report.json \
      --issue-input examples/issue_input.json \
      --output .hgs/full_loop_dry_run.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_CHAIN = [
    "truth_owner_identification",
    "p9_dispatch_review",
    "required_tool_identification",
    "risk_gate_check",
    "p8_execution_plan",
    "qa_experience_sre_validation_plan",
    "p9_rereview_path",
    "reopen_or_closeout_condition_check",
    "clearance_loop_bootstrap",
]

ISSUE_TYPE_OWNER_MAP = {
    "rule": "11_Product_Business_Rules_Owner",
    "auth": "12_Auth_Identity_Owner",
    "billing": "13_Billing_Entitlement_Owner",
    "release": "14_Release_Config_Owner",
    "security": "15_Security_Risk_Owner",
    "agent": "16_Agent_Operations_Owner",
    "enduser": "17_EndUser_Support_Owner",
    "control_plane": "18_Control_Plane_Owner",
    "execution_plane": "19_Execution_Plane_Owner",
    "frontend": "32B_P8_Frontend_Logic_Engineer",
    "console": "33A_P8_Console_Runtime_Engineer",
    "worker": "34_P8_LanrenJingling_PUA",
    "qa": "37_QA_Validation_Owner",
    "sre": "38_SRE_Observability_Owner",
    "docs": "39_Knowledge_Documentation_Owner",
    "mixed": "20_P9_Principal",
}

KEYWORD_TOOL_MAP = {
    "rule": ["70_Business_Rule_Matrix_SKILL.md", "71_State_Machine_Consistency_SKILL.md"],
    "auth": ["72_JWT_Inspector_SKILL.md", "74_Session_Refresh_Trace_SKILL.md", "110_Authorization_Bypass_Path_Reviewer_SKILL.md"],
    "billing": ["76_Billing_Ledger_Reconciler_SKILL.md", "77_Quota_Usage_Analyzer_SKILL.md", "78_Freeze_Reversal_Diagnoser_SKILL.md"],
    "frontend": ["79_API_Contract_Diff_SKILL.md", "82_Network_Trace_Reviewer_SKILL.md", "85_UI_Surface_Audit_SKILL.md"],
    "console": ["88_Console_Auth_Flow_Trace_SKILL.md", "89_Project_Context_Drift_SKILL.md", "90_StepUp_Resume_Checker_SKILL.md"],
    "worker": ["91_Worker_Identity_Stability_SKILL.md", "92_Heartbeat_Gap_Analyzer_SKILL.md", "98_Trace_Correlation_SKILL.md"],
    "release": ["101_Compatibility_Matrix_SKILL.md", "109_High_Risk_Action_Guard_Checker_SKILL.md"],
    "qa": ["95_Test_Matrix_Builder_SKILL.md", "96_Regression_Checklist_SKILL.md"],
    "docs": ["106_SOP_Generator_SKILL.md", "107_Protocol_Field_Completeness_Checker_SKILL.md"],
    "mixed": ["108_Chain_Route_Simulator_SKILL.md", "114_Score_Decision_Engine_SKILL.md", "115_Full_Issue_Clearance_Controller_SKILL.md"],
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "issue"


def infer_owner(issue_input: Dict[str, Any]) -> str:
    issue_type = issue_input.get("issue_type", "mixed")
    return ISSUE_TYPE_OWNER_MAP.get(issue_type, "20_P9_Principal")


def infer_required_tools(issue_input: Dict[str, Any]) -> List[str]:
    issue_type = issue_input.get("issue_type", "mixed")
    tools = list(KEYWORD_TOOL_MAP.get(issue_type, []))
    for flag in issue_input.get("risk_flags", []):
        if flag in {"high_risk_action", "destructive_change"} and "109_High_Risk_Action_Guard_Checker_SKILL.md" not in tools:
            tools.append("109_High_Risk_Action_Guard_Checker_SKILL.md")
        if flag in {"auth_bypass", "scope_risk"} and "110_Authorization_Bypass_Path_Reviewer_SKILL.md" not in tools:
            tools.append("110_Authorization_Bypass_Path_Reviewer_SKILL.md")
        if flag in {"runtime_stability", "incident"} and "113_Runtime_Incident_Replayer_SKILL.md" not in tools:
            tools.append("113_Runtime_Incident_Replayer_SKILL.md")
    if "114_Score_Decision_Engine_SKILL.md" not in tools:
        tools.append("114_Score_Decision_Engine_SKILL.md")
    if "115_Full_Issue_Clearance_Controller_SKILL.md" not in tools:
        tools.append("115_Full_Issue_Clearance_Controller_SKILL.md")
    return tools


def build_issue_stub(issue_input: Dict[str, Any], owner_name: str) -> Dict[str, Any]:
    title = issue_input.get("title") or issue_input.get("current_question") or issue_input.get("summary") or "unnamed issue"
    issue_id = issue_input.get("issue_id") or f"DRYRUN-{slugify(title)[:40]}"
    return {
        "issue_id": issue_id,
        "title": title,
        "issue_type": issue_input.get("issue_type", "mixed"),
        "problem_statement": issue_input.get("current_question") or title,
        "owner": owner_name,
        "source_of_truth": issue_input.get("source_of_truth", []),
        "risk_flags": issue_input.get("risk_flags", []),
        "status": "stub_created",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap HGS full_loop dry-run from verified Release assembly")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--report", default=".hgs/assembly_report.json", help="Verified assembly report path")
    parser.add_argument("--issue-input", required=True, help="Issue input JSON path")
    parser.add_argument("--output", default=".hgs/full_loop_dry_run.json", help="Dry-run output path")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if assembly has not passed")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = load_json(repo_root / args.report)
    if report.get("full_release_assembly_status") != "pass":
        print(json.dumps({
            "automation_execution_status": "fail",
            "reason": "full_release_assembly_status != pass",
        }, ensure_ascii=False, indent=2))
        return 1 if args.strict else 0

    issue_input = load_json(repo_root / args.issue_input)
    owner_name = infer_owner(issue_input)
    required_tools = infer_required_tools(issue_input)
    issue_stub = build_issue_stub(issue_input, owner_name)

    risk_flags = issue_input.get("risk_flags", [])
    gate_plan = {
        "high_risk_guard_gate": any(flag in {"high_risk_action", "destructive_change"} for flag in risk_flags),
        "auth_bypass_guard_gate": any(flag in {"auth_bypass", "scope_risk"} for flag in risk_flags),
        "runtime_stability_gate": any(flag in {"runtime_stability", "incident"} for flag in risk_flags),
        "must_run_tool_gate": True,
    }

    dry_run = {
        "mode": "full_loop",
        "chain": DEFAULT_CHAIN,
        "issue_stub_created": "yes",
        "owner_identified": "yes",
        "owner_name": owner_name,
        "required_tools_identified": "yes",
        "required_tools": required_tools,
        "risk_gates_checked": "yes",
        "risk_gate_plan": gate_plan,
        "exec_plan_created": "yes",
        "exec_plan": {
            "owner": owner_name,
            "max_change_boundary": issue_input.get("max_change_boundary", "provisional"),
            "success_definition": issue_input.get("acceptance_criteria", ["acceptance criteria not yet supplied"]),
        },
        "validation_plan_created": "yes",
        "validation_plan": {
            "required_level": issue_input.get("verification_target", "L3"),
            "critical_paths": issue_input.get("critical_paths", []),
        },
        "experience_plan_created": "yes",
        "experience_plan": {
            "experience_protocols": [
                "40_P8_Agent_Experience_Protocol.md",
                "41_P8_EndUser_Experience_Protocol.md",
            ],
            "replay_required_when_real_feedback_missing": True,
        },
        "rereview_path_created": "yes",
        "rereview_path": {
            "p9_rereview": True,
            "p10_on_demand": True,
            "protocol": "50_RE_REVIEW_PROTOCOL.md",
        },
        "issue_inventory_created": "yes",
        "issue_inventory": {
            "open_issue_count_initialized": 1,
            "items": [issue_stub],
        },
        "clearance_gate_created": "yes",
        "clearance_loop_created": "yes",
        "clearance_loop": {
            "controller": "115_Full_Issue_Clearance_Controller_SKILL.md",
            "rule": "continue until open_issue_count = 0",
            "next_required_action": "dispatch_issue_to_owner",
        },
        "automation_execution_status": "pass",
    }

    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dry_run, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dry_run, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
