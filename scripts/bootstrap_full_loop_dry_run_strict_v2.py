#!/usr/bin/env python3
"""Registry-driven strict v2 full_loop dry-run bootstrap."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

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


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "issue"


def make_registry(ledger: Dict[str, Any], category: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for item in ledger.get("loaded_files", []):
        if item.get("category") == category and item.get("loaded"):
            out[Path(item["path"]).name] = item["path"]
    return out


def resolve_owner(issue_type: str, role_registry: Dict[str, str], route_registry: Dict[str, Any]) -> Tuple[str | None, List[str]]:
    basename = route_registry["owner_basename_map"].get(issue_type, route_registry["owner_basename_map"]["mixed"])
    if basename in role_registry:
        return role_registry[basename], []
    return None, [f"owner_missing_from_registry:{basename}"]


def resolve_tools(issue_type: str, risk_flags: List[str], tool_registry: Dict[str, str], route_registry: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    requested = list(route_registry["tool_basename_map"].get(issue_type, route_registry["tool_basename_map"]["mixed"]))
    for flag in risk_flags:
        requested.extend(route_registry.get("risk_flag_tool_map", {}).get(flag, []))
    requested.extend(route_registry.get("always_include_tools", []))

    resolved: List[str] = []
    errors: List[str] = []
    seen = set()
    for basename in requested:
        if basename in seen:
            continue
        seen.add(basename)
        path = tool_registry.get(basename)
        if path:
            resolved.append(path)
        else:
            errors.append(f"tool_missing_from_registry:{basename}")
    return resolved, errors


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
    owner_confidence = 85 if owner_ok else 25
    route_stability_score = 80 if owner_ok and tools_ok else 35
    tool_coverage_score = 92 if tools_ok else max(0, 92 - 15 * len(blocking_reasons))
    evidence = 40
    for field, delta in [("acceptance_criteria", 15), ("critical_paths", 15), ("source_of_truth", 10), ("max_change_boundary", 10)]:
        if issue_input.get(field):
            evidence += delta
    reopen_risk = 20 if issue_input.get("verification_target") in {"L3", "L4"} else 45
    if blocking_reasons:
        reopen_risk += 20
    closeout = 15 if blocking_reasons else 60
    return {
        "owner_confidence": min(owner_confidence, 100),
        "route_stability_score": min(route_stability_score, 100),
        "tool_coverage_score": min(tool_coverage_score, 100),
        "evidence_completeness_score": min(evidence, 100),
        "reopen_risk_score": min(reopen_risk, 100),
        "closeout_readiness_score": min(closeout, 100),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Registry-driven strict v2 HGS full_loop dry-run bootstrap")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--ledger", default=".hgs/assembly_ledger.json")
    parser.add_argument("--report", default=".hgs/assembly_report.json")
    parser.add_argument("--route-registry", default="scripts/runtime_route_registry.json")
    parser.add_argument("--issue-input", required=True)
    parser.add_argument("--output", default=".hgs/full_loop_dry_run.json")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    ledger = load_json(repo_root / args.ledger)
    report = load_json(repo_root / args.report)
    route_registry = load_json(repo_root / args.route_registry)

    if report.get("full_release_assembly_status") != "pass":
        result = {"mode": "full_loop", "automation_execution_status": "fail", "blocking_reasons": ["full_release_assembly_status != pass"], "user_choice_required": "no", "suggestion_mode": "no"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if args.strict else 0

    role_registry = make_registry(ledger, "role")
    tool_registry = make_registry(ledger, "tool")
    issue_input = load_json(repo_root / args.issue_input)

    issue_type = issue_input.get("issue_type", "mixed")
    risk_flags = list(issue_input.get("risk_flags", []))
    owner_path, owner_errors = resolve_owner(issue_type, role_registry, route_registry)
    required_tools, tool_errors = resolve_tools(issue_type, risk_flags, tool_registry, route_registry)
    blocking_reasons = owner_errors + tool_errors

    user_choice_required = "yes" if any(flag == "user_choice_required" for flag in risk_flags) else "no"
    suggestion_mode = "yes" if owner_path is None and len(required_tools) == 0 else "no"

    issue_stub = build_issue_stub(issue_input, owner_path)
    secondary_findings = list(issue_input.get("secondary_findings", []))
    reopened_findings = list(issue_input.get("reopened_findings", []))
    open_issue_count_initialized = 1 + len(secondary_findings) + len(reopened_findings)

    route_simulation = {
        "simulated_route": [
            {"step": 1, "actor": owner_path or "unresolved_owner", "action": "truth_owner_identification"},
            {"step": 2, "actor": "Release/roles/20_P9_Principal_SKILL.md", "action": "dispatch_review"},
            {"step": 3, "actor": required_tools, "action": "must_run_tools"},
            {"step": 4, "actor": "Release/roles/37_QA_Validation_Owner_SKILL.md", "action": "validation_plan"},
            {"step": 5, "actor": "Release/roles/39_Knowledge_Documentation_Owner_SKILL.md", "action": "docs_sink"}
        ],
        "missing_steps": ["owner_resolution"] if not owner_path else [],
        "route_conflicts": blocking_reasons,
        "must_trigger_tools": required_tools,
        "likely_stop_conditions": blocking_reasons,
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

    validation_plan_created = bool(issue_input.get("critical_paths") or issue_input.get("acceptance_criteria"))
    automation_execution_status = "pass" if all([
        owner_path is not None,
        len(tool_errors) == 0,
        dispatch_decision == "dispatch",
        review_decision == "review",
        validation_plan_created,
        user_choice_required == "no",
        suggestion_mode == "no",
    ]) else "fail"

    next_required_action = "dispatch_issue_to_owner" if automation_execution_status == "pass" else ("user_choice_required" if user_choice_required == "yes" else "resolve_blocking_reasons")

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
        "exec_plan": {"owner": owner_path, "max_change_boundary": issue_input.get("max_change_boundary", "provisional"), "success_definition": issue_input.get("acceptance_criteria", [])},
        "validation_plan_created": "yes" if validation_plan_created else "no",
        "validation_plan": {"required_level": issue_input.get("verification_target", "L3"), "critical_paths": issue_input.get("critical_paths", [])},
        "experience_plan_created": "yes",
        "experience_plan": {"experience_protocols": ["Release/protocols/40_P8_Agent_Experience_Protocol.md", "Release/protocols/41_P8_EndUser_Experience_Protocol.md"], "replay_required_when_real_feedback_missing": True},
        "rereview_path_created": "yes",
        "rereview_path": {"p9_rereview": True, "p10_on_demand": True, "protocol": "Release/protocols/50_RE_REVIEW_PROTOCOL.md"},
        "issue_inventory_created": "yes",
        "issue_inventory": {"open_issue_count_initialized": open_issue_count_initialized, "items": [issue_stub] + secondary_findings + reopened_findings},
        "clearance_gate_created": "yes" if open_issue_count_initialized >= 1 else "no",
        "clearance_loop_created": "yes",
        "clearance_loop": {"controller": "Release/tools/115_Full_Issue_Clearance_Controller_SKILL.md", "rule": "continue until open_issue_count = 0", "next_required_action": next_required_action},
        "route_simulation": route_simulation,
        "score_snapshot": score_snapshot,
        "dispatch_decision": dispatch_decision,
        "review_decision": review_decision,
        "reopen_decision": reopen_decision,
        "done_decision": done_decision,
        "blocking_reasons": blocking_reasons,
        "user_choice_required": user_choice_required,
        "suggestion_mode": suggestion_mode,
        "automation_execution_status": automation_execution_status,
    }

    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dry_run, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dry_run, ensure_ascii=False, indent=2))
    return 1 if args.strict and automation_execution_status != "pass" else 0


if __name__ == "__main__":
    raise SystemExit(main())
