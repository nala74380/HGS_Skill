#!/usr/bin/env python3
"""Strict full_loop dry-run bootstrap.

This version reduces pre-filled assumptions by:
- validating owner/tool availability against the assembly ledger
- producing route simulation and score snapshot artifacts
- failing when key bootstrap conditions are not met
- supporting secondary findings and reopen-derived findings
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

OWNER_BASENAME_MAP = {
    "rule": "11_Product_Business_Rules_Owner_SKILL.md",
    "auth": "12_Auth_Identity_Owner_SKILL.md",
    "billing": "13_Billing_Entitlement_Owner_SKILL.md",
    "release": "14_Release_Config_Owner_SKILL.md",
    "security": "15_Security_Risk_Owner_SKILL.md",
    "agent": "16_Agent_Operations_Owner_SKILL.md",
    "enduser": "17_EndUser_Support_Owner_SKILL.md",
    "control_plane": "18_Control_Plane_Owner_SKILL.md",
    "execution_plane": "19_Execution_Plane_Owner_SKILL.md",
    "frontend": "32B_P8_Frontend_Logic_Engineer_SKILL.md",
    "console": "33A_P8_Console_Runtime_Engineer_SKILL.md",
    "worker": "34_P8_LanrenJingling_PUA_SKILL.md",
    "qa": "37_QA_Validation_Owner_SKILL.md",
    "sre": "38_SRE_Observability_Owner_SKILL.md",
    "docs": "39_Knowledge_Documentation_Owner_SKILL.md",
    "mixed": "20_P9_Principal_SKILL.md",
}

TOOL_BASENAME_MAP = {
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


def make_registry(ledger: Dict[str, Any], category: str) -> Dict[str, str]:
    registry: Dict[str, str] = {}
    for item in ledger.get("loaded_files", []):
        if item.get("category") == category and item.get("loaded"):
            path = item["path"]
            registry[Path(path).name] = path
    return registry


def resolve_owner(issue_type: str, role_registry: Dict[str, str]) -> tuple[str | None, List[str]]:
    basename = OWNER_BASENAME_MAP.get(issue_type, OWNER_BASENAME_MAP["mixed"])
    if basename in role_registry:
        return role_registry[basename], []
    return None, [f"owner_missing_from_registry:{basename}"]


def resolve_tools(issue_type: str, risk_flags: List[str], tool_registry: Dict[str, str]) -> tuple[List[str], List[str]]:
    requested = list(TOOL_BASENAME_MAP.get(issue_type, TOOL_BASENAME_MAP["mixed"]))
    if any(flag in {"high_risk_action", "destructive_change"} for flag in risk_flags):
        requested.append("109_High_Risk_Action_Guard_Checker_SKILL.md")
    if any(flag in {"auth_bypass", "scope_risk"} for flag in risk_flags):
        requested.append("110_Authorization_Bypass_Path_Reviewer_SKILL.md")
    if any(flag in {"runtime_stability", "incident"} for flag in risk_flags):
        requested.append("113_Runtime_Incident_Replayer_SKILL.md")
    requested.extend(["114_Score_Decision_Engine_SKILL.md", "115_Full_Issue_Clearance_Controller_SKILL.md"])

    deduped, missing, resolved = [], [], []
    seen = set()
    for basename in requested:
        if basename in seen:
            continue
        seen.add(basename)
        if basename in tool_registry:
            resolved.append(tool_registry[basename])
            deduped.append(basename)
        else:
            missing.append(f"tool_missing_from_registry:{basename}")
    return resolved, missing


def build_issue_stub(issue_input: Dict[str, Any], owner_path: str | None) -> Dict[str, Any]:
    title = issue_input.get("title") or issue_input.get("current_question") or issue_input.get("summary") or "unnamed issue"
    issue_id = issue_input.get("issue_id") or f"DRYRUN-{slugify(title)[:40]}"
    return {
        "issue_id": issue_id,
        "title": title,
        "issue_type": issue_input.get("issue_type", "mixed"),
        "problem_statement": issue_input.get("current_question") or title,
        "owner": owner_path,
        "source_of_truth": issue_input.get("source_of_truth", []),
        "risk_flags": issue_input.get("risk_flags", []),
        "status": "stub_created" if owner_path else "owner_unresolved",
    }


def compute_score_snapshot(owner_ok: bool, tools_ok: bool, issue_input: Dict[str, Any], blocking_reasons: List[str]) -> Dict[str, int]:
    owner_confidence = 85 if owner_ok else 30
    route_stability_score = 80 if owner_ok and tools_ok else 40
    tool_coverage_score = 90 if tools_ok else max(0, 90 - 15 * len(blocking_reasons))
    evidence_completeness_score = 50
    if issue_input.get("acceptance_criteria"):
        evidence_completeness_score += 15
    if issue_input.get("critical_paths"):
        evidence_completeness_score += 15
    if issue_input.get("source_of_truth"):
        evidence_completeness_score += 10
    if issue_input.get("max_change_boundary"):
        evidence_completeness_score += 10
    reopen_risk_score = 25 if issue_input.get("verification_target") in {"L3", "L4"} else 45
    if blocking_reasons:
        reopen_risk_score += 20
    closeout_readiness_score = 20 if blocking_reasons else 55
    return {
        "owner_confidence": owner_confidence,
        "route_stability_score": route_stability_score,
        "tool_coverage_score": tool_coverage_score,
        "evidence_completeness_score": min(evidence_completeness_score, 100),
        "reopen_risk_score": min(reopen_risk_score, 100),
        "closeout_readiness_score": closeout_readiness_score,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Strict HGS full_loop dry-run bootstrap")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--ledger", default=".hgs/assembly_ledger.json")
    parser.add_argument("--report", default=".hgs/assembly_report.json")
    parser.add_argument("--issue-input", required=True)
    parser.add_argument("--output", default=".hgs/full_loop_dry_run.json")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    ledger = load_json(repo_root / args.ledger)
    report = load_json(repo_root / args.report)

    if report.get("full_release_assembly_status") != "pass":
        result = {
            "mode": "full_loop",
            "automation_execution_status": "fail",
            "blocking_reasons": ["full_release_assembly_status != pass"],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.strict:
            return 1
        return 0

    issue_input = load_json(repo_root / args.issue_input)
    role_registry = make_registry(ledger, "role")
    tool_registry = make_registry(ledger, "tool")

    issue_type = issue_input.get("issue_type", "mixed")
    risk_flags = list(issue_input.get("risk_flags", []))
    owner_path, owner_errors = resolve_owner(issue_type, role_registry)
    required_tools, tool_errors = resolve_tools(issue_type, risk_flags, tool_registry)
    blocking_reasons = owner_errors + tool_errors

    issue_stub = build_issue_stub(issue_input, owner_path)

    secondary_findings = list(issue_input.get("secondary_findings", []))
    reopened_findings = list(issue_input.get("reopened_findings", []))
    open_issue_count_initialized = 1 + len(secondary_findings) + len(reopened_findings)

    route_simulation = {
        "simulated_route": [
            {"step": 1, "actor": owner_path or "unresolved_owner", "action": "truth_owner_identification"},
            {"step": 2, "actor": "20_P9_Principal_SKILL.md", "action": "dispatch_review"},
            {"step": 3, "actor": required_tools, "action": "must_run_tools"},
            {"step": 4, "actor": "37_QA_Validation_Owner_SKILL.md", "action": "validation_plan"},
            {"step": 5, "actor": "39_Knowledge_Documentation_Owner_SKILL.md", "action": "docs_sink"},
        ],
        "missing_steps": ["owner_resolution"] if not owner_path else [],
        "route_conflicts": blocking_reasons,
        "must_trigger_tools": required_tools,
        "likely_stop_conditions": [reason for reason in blocking_reasons if reason],
    }

    score_snapshot = compute_score_snapshot(bool(owner_path), len(tool_errors) == 0, issue_input, blocking_reasons)
    dispatch_decision = "dispatch" if score_snapshot["owner_confidence"] >= 70 and score_snapshot["tool_coverage_score"] >= 85 else "hold"
    review_decision = "review" if dispatch_decision == "dispatch" else "blocked"
    reopen_decision = "reopen_possible" if score_snapshot["reopen_risk_score"] >= 60 else "reopen_unlikely"
    done_decision = "not_done" if open_issue_count_initialized > 0 else "done"

    gate_plan = {
        "high_risk_guard_gate": any(flag in {"high_risk_action", "destructive_change"} for flag in risk_flags),
        "auth_bypass_guard_gate": any(flag in {"auth_bypass", "scope_risk"} for flag in risk_flags),
        "runtime_stability_gate": any(flag in {"runtime_stability", "incident"} for flag in risk_flags),
        "must_run_tool_gate": len(required_tools) > 0,
    }

    automation_execution_status = "pass" if all([
        owner_path is not None,
        len(tool_errors) == 0,
        dispatch_decision == "dispatch",
        review_decision == "review",
    ]) else "fail"

    dry_run = {
        "mode": "full_loop",
        "chain": DEFAULT_CHAIN,
        "issue_stub_created": "yes" if owner_path else "no",
        "owner_identified": "yes" if owner_path else "no",
        "owner_name": owner_path or "",
        "required_tools_identified": "yes" if len(required_tools) > 0 else "no",
        "required_tools": required_tools,
        "risk_gates_checked": "yes",
        "risk_gate_plan": gate_plan,
        "exec_plan_created": "yes" if owner_path else "no",
        "exec_plan": {
            "owner": owner_path,
            "max_change_boundary": issue_input.get("max_change_boundary", "provisional"),
            "success_definition": issue_input.get("acceptance_criteria", []),
        },
        "validation_plan_created": "yes" if issue_input.get("critical_paths") or issue_input.get("acceptance_criteria") else "no",
        "validation_plan": {
            "required_level": issue_input.get("verification_target", "L3"),
            "critical_paths": issue_input.get("critical_paths", []),
        },
        "experience_plan_created": "yes",
        "experience_plan": {
            "experience_protocols": [
                "Release/protocols/40_P8_Agent_Experience_Protocol.md",
                "Release/protocols/41_P8_EndUser_Experience_Protocol.md",
            ],
            "replay_required_when_real_feedback_missing": True,
        },
        "rereview_path_created": "yes",
        "rereview_path": {
            "p9_rereview": True,
            "p10_on_demand": True,
            "protocol": "Release/protocols/50_RE_REVIEW_PROTOCOL.md",
        },
        "issue_inventory_created": "yes",
        "issue_inventory": {
            "open_issue_count_initialized": open_issue_count_initialized,
            "items": [issue_stub] + secondary_findings + reopened_findings,
        },
        "clearance_gate_created": "yes" if open_issue_count_initialized >= 1 else "no",
        "clearance_loop_created": "yes",
        "clearance_loop": {
            "controller": "Release/tools/115_Full_Issue_Clearance_Controller_SKILL.md",
            "rule": "continue until open_issue_count = 0",
            "next_required_action": "dispatch_issue_to_owner" if automation_execution_status == "pass" else "resolve_blocking_reasons",
        },
        "route_simulation": route_simulation,
        "score_snapshot": score_snapshot,
        "dispatch_decision": dispatch_decision,
        "review_decision": review_decision,
        "reopen_decision": reopen_decision,
        "done_decision": done_decision,
        "blocking_reasons": blocking_reasons,
        "automation_execution_status": automation_execution_status,
    }

    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dry_run, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dry_run, ensure_ascii=False, indent=2))

    if args.strict and automation_execution_status != "pass":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
