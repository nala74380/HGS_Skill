#!/usr/bin/env python3
"""Render strict automation acceptance report from strict dry-run output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def yes_no(value: Any) -> str:
    if isinstance(value, str) and value.lower() in {"yes", "no"}:
        return value.lower()
    return "yes" if bool(value) else "no"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render strict automation execution acceptance report")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--input", default=".hgs/full_loop_dry_run.json")
    parser.add_argument("--output", default=".hgs/automation_execution_acceptance_report.json")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    dry_run = load_json(repo_root / args.input)

    issue_inventory = dry_run.get("issue_inventory", {})
    clearance_loop = dry_run.get("clearance_loop", {})
    route_conflicts = dry_run.get("route_simulation", {}).get("route_conflicts", [])
    blocking_reasons = dry_run.get("blocking_reasons", [])

    report = {
        "issue_stub_created": yes_no(dry_run.get("issue_stub_created")),
        "owner_identified": yes_no(dry_run.get("owner_identified")),
        "owner_name": dry_run.get("owner_name", ""),
        "required_tools_identified": yes_no(dry_run.get("required_tools_identified")),
        "required_tools": dry_run.get("required_tools", []),
        "risk_gates_checked": yes_no(dry_run.get("risk_gates_checked")),
        "exec_plan_created": yes_no(dry_run.get("exec_plan_created")),
        "validation_plan_created": yes_no(dry_run.get("validation_plan_created")),
        "experience_plan_created": yes_no(dry_run.get("experience_plan_created")),
        "rereview_path_created": yes_no(dry_run.get("rereview_path_created")),
        "clearance_loop_created": yes_no(dry_run.get("clearance_loop_created")),
        "issue_inventory_created": yes_no(dry_run.get("issue_inventory_created")),
        "clearance_gate_created": yes_no(dry_run.get("clearance_gate_created")),
        "open_issue_count_initialized": issue_inventory.get("open_issue_count_initialized", ""),
        "next_required_action": clearance_loop.get("next_required_action", ""),
        "automation_execution_status": dry_run.get("automation_execution_status", "fail"),
        "judgements": {
            "is_in_automation_chain": "yes" if dry_run.get("automation_execution_status") == "pass" else "no",
            "issue_ledger_established": "yes" if issue_inventory.get("items") else "no",
            "owner_established": yes_no(dry_run.get("owner_identified")),
            "tool_plan_established": yes_no(dry_run.get("required_tools_identified")),
            "gate_plan_established": "yes" if dry_run.get("risk_gate_plan") else "no",
            "exec_plan_established": yes_no(dry_run.get("exec_plan_created")),
            "validation_experience_rereview_clearance_path_established": "yes" if all([
                dry_run.get("validation_plan_created") == "yes",
                dry_run.get("experience_plan_created") == "yes",
                dry_run.get("rereview_path_created") == "yes",
                dry_run.get("clearance_loop_created") == "yes",
            ]) else "no",
            "continue_until_open_issue_zero_default_rule": "yes" if clearance_loop.get("rule") == "continue until open_issue_count = 0" else "no",
            "still_asking_user_to_pick_a_or_b": "yes" if any("user_choice_required" in x for x in blocking_reasons + route_conflicts) else "no",
            "still_stuck_in_suggestion_mode": "yes" if dry_run.get("automation_execution_status") != "pass" and dry_run.get("next_required_action") == "suggest_next_steps" else "no",
        },
        "route_conflicts": route_conflicts,
        "blocking_reasons": blocking_reasons,
        "score_snapshot": dry_run.get("score_snapshot", {}),
    }

    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if args.strict and report["automation_execution_status"] != "pass":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
