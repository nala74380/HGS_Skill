#!/usr/bin/env python3
"""Strict Release acceptance verification.

Outputs a machine-readable report aligned to the fixed assembly acceptance report shape.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_ROLE_GOVERNANCE_DOCS = [
    "Release/docs/角色调用关系总表.md",
    "Release/docs/角色-工具矩阵总表.md",
    "Release/docs/角色边界验证台账.md",
]
REQUIRED_TOOL_GOVERNANCE_DOCS = ["Release/docs/工具调用关系总表.md"]
REQUIRED_CLEARANCE_DOCS = [
    "Release/protocols/61_Automation_Orchestration_Protocol.md",
    "Release/protocols/62_Full_Issue_Discovery_Dispatch_and_Clearance_Protocol.md",
]
REQUIRED_SCORING_DOCS = ["Release/docs/HGS_全局检查与清理评分报告.md"]
REQUIRED_LEDGER_DOCS = ["Release/docs/HGS_全局扣分点问题清单与派单台账.md"]
README_BASELINE = "README.md"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def loaded_path_set(ledger: Dict[str, Any]) -> set[str]:
    return {item["path"] for item in ledger.get("loaded_files", []) if item.get("loaded")}


def contains_all(loaded: set[str], expected: List[str]) -> bool:
    return all(path in loaded for path in expected)


def main() -> int:
    parser = argparse.ArgumentParser(description="Strict HGS Release acceptance verification")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--ledger", default=".hgs/assembly_ledger.json")
    parser.add_argument("--output", default=".hgs/assembly_report.json")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    ledger = load_json(repo_root / args.ledger)
    loaded = loaded_path_set(ledger)

    entrypoint_value = ledger.get("entrypoint", "")
    entrypoint_path = entrypoint_value if str(entrypoint_value).startswith("Release/") else f"Release/{entrypoint_value}"
    entrypoint_ok = entrypoint_path in loaded

    roles_ok = ledger.get("roles_loaded") == ledger.get("roles_expected")
    tools_ok = ledger.get("tools_loaded") == ledger.get("tools_expected")
    protocols_ok = ledger.get("protocols_loaded") == ledger.get("protocols_expected")
    docs_ok = ledger.get("docs_loaded") == ledger.get("docs_expected")

    role_governance_docs_loaded = contains_all(loaded, REQUIRED_ROLE_GOVERNANCE_DOCS)
    tool_governance_docs_loaded = contains_all(loaded, REQUIRED_TOOL_GOVERNANCE_DOCS)
    clearance_docs_loaded = contains_all(loaded, REQUIRED_CLEARANCE_DOCS)
    scoring_docs_loaded = contains_all(loaded, REQUIRED_SCORING_DOCS)
    deduction_ledger_loaded = contains_all(loaded, REQUIRED_LEDGER_DOCS)
    readme_release_baseline_loaded = (repo_root / README_BASELINE).exists()

    full_release_assembly_status = "pass" if all([
        ledger.get("assembly_status") == "pass",
        entrypoint_ok,
        roles_ok,
        tools_ok,
        protocols_ok,
        docs_ok,
        role_governance_docs_loaded,
        tool_governance_docs_loaded,
        clearance_docs_loaded,
        scoring_docs_loaded,
        deduction_ledger_loaded,
        readme_release_baseline_loaded,
        ledger.get("release_source_only") is True,
    ]) else "fail"

    report = {
        "package_version": ledger.get("package_version"),
        "entrypoint": ledger.get("entrypoint"),
        "default_route_mode": ledger.get("default_route_mode"),
        "action_protocol": ledger.get("action_protocol"),
        "clearance_protocol": ledger.get("clearance_protocol"),
        "roles_loaded_count": f"{ledger.get('roles_loaded')} / {ledger.get('roles_expected')}",
        "tools_loaded_count": f"{ledger.get('tools_loaded')} / {ledger.get('tools_expected')}",
        "protocols_loaded_count": f"{ledger.get('protocols_loaded')} / {ledger.get('protocols_expected')}",
        "docs_loaded_count": f"{ledger.get('docs_loaded')} / {ledger.get('docs_expected')}",
        "active_actions_count": ledger.get("active_actions_count"),
        "active_action_batches": ledger.get("active_action_batches", []),
        "risk_gates": ledger.get("risk_gates", []),
        "role_governance_docs_loaded": "yes" if role_governance_docs_loaded else "no",
        "tool_governance_docs_loaded": "yes" if tool_governance_docs_loaded else "no",
        "clearance_docs_loaded": "yes" if clearance_docs_loaded else "no",
        "deduction_ledger_loaded": "yes" if deduction_ledger_loaded else "no",
        "readme_release_baseline_loaded": "yes" if readme_release_baseline_loaded else "no",
        "release_source_only": "yes" if ledger.get("release_source_only") else "no",
        "full_release_assembly_status": full_release_assembly_status,
        "missing_files": ledger.get("missing_files", []),
        "duplicate_registrations": ledger.get("duplicate_registrations", []),
        "unregistered_release_files": ledger.get("unregistered_release_files", []),
        "out_of_release_registered_paths": ledger.get("out_of_release_registered_paths", []),
        "registered_paths_all_within_release": ledger.get("registered_paths_all_within_release"),
        "loaded_paths_all_within_release": ledger.get("loaded_paths_all_within_release"),
        "scoring_docs_loaded": "yes" if scoring_docs_loaded else "no",
    }

    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if args.strict and full_release_assembly_status != "pass":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
