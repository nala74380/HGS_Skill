#!/usr/bin/env python3
"""Batch-assemble the HGS Release package from MANIFEST.json.

This script is designed to make the Release package loadable in one pass:
- reads Release/MANIFEST.json
- validates entrypoint and registered file lists
- loads all registered files under load_order/tool_load_order/documentation_load_order
- emits an assembly ledger JSON file for downstream acceptance and dry-run bootstrap

Usage:
  python scripts/assemble_release.py \
      --repo-root . \
      --manifest Release/MANIFEST.json \
      --output .hgs/assembly_ledger.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


@dataclass
class LoadedFile:
    path: str
    category: str
    exists: bool
    loaded: bool
    bytes: int
    sha256: str | None
    error: str | None


@dataclass
class AssemblyLedger:
    package_version: str
    entrypoint: str
    default_route_mode: str
    action_protocol: str | None
    clearance_protocol: str | None
    release_root: str
    manifest_path: str
    release_source_only: bool
    roles_expected: int
    tools_expected: int
    protocols_expected: int
    docs_expected: int
    roles_loaded: int
    tools_loaded: int
    protocols_loaded: int
    docs_loaded: int
    active_actions_count: int
    active_action_batches: List[str]
    risk_gates: List[str]
    loaded_files: List[Dict[str, Any]]
    missing_files: List[str]
    duplicate_registrations: List[str]
    unregistered_release_files: List[str]
    assembly_status: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_registered_path(raw_path: str) -> str:
    raw_path = raw_path.strip().lstrip("./")
    if raw_path.startswith("Release/"):
        return raw_path
    return f"Release/{raw_path}"


def list_release_files(release_root: Path) -> List[str]:
    return sorted(
        str(p.as_posix())
        for p in release_root.rglob("*")
        if p.is_file()
    )


def categorize_registered_path(path: str) -> str:
    if "/roles/" in path:
        return "role"
    if "/tools/" in path:
        return "tool"
    if "/protocols/" in path:
        return "protocol"
    if "/docs/" in path:
        return "doc"
    if path.endswith("MANIFEST.json") or path.endswith("00_HGS_Master_Loader.md"):
        return "entry"
    return "other"


def load_registered_files(repo_root: Path, registered_paths: List[str]) -> Tuple[List[LoadedFile], List[str]]:
    loaded: List[LoadedFile] = []
    missing: List[str] = []
    for path_str in registered_paths:
        path = repo_root / path_str
        category = categorize_registered_path(path_str)
        if not path.exists():
            loaded.append(LoadedFile(path=path_str, category=category, exists=False, loaded=False, bytes=0, sha256=None, error="file_not_found"))
            missing.append(path_str)
            continue
        try:
            content = read_text(path)
            loaded.append(
                LoadedFile(
                    path=path_str,
                    category=category,
                    exists=True,
                    loaded=True,
                    bytes=len(content.encode("utf-8")),
                    sha256=sha256_text(content),
                    error=None,
                )
            )
        except Exception as exc:  # pragma: no cover
            loaded.append(LoadedFile(path=path_str, category=category, exists=True, loaded=False, bytes=0, sha256=None, error=str(exc)))
            missing.append(path_str)
    return loaded, missing


def parse_manifest(manifest_text: str) -> Dict[str, Any]:
    return json.loads(manifest_text)


def compute_expected_counts(registered_paths: List[str]) -> Dict[str, int]:
    counts = {"role": 0, "tool": 0, "protocol": 0, "doc": 0}
    for p in registered_paths:
        cat = categorize_registered_path(p)
        if cat in counts:
            counts[cat] += 1
    return counts


def find_unregistered_release_files(all_release_files: List[str], registered_paths: List[str], entrypoint: str, manifest_path: str) -> List[str]:
    allowed = set(registered_paths)
    allowed.add(normalize_registered_path(entrypoint))
    allowed.add(normalize_registered_path(manifest_path))
    return sorted([p for p in all_release_files if p.startswith("Release/") and p not in allowed])


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch assemble HGS Release package from MANIFEST.json")
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    parser.add_argument("--manifest", default="Release/MANIFEST.json", help="Manifest path relative to repo root")
    parser.add_argument("--output", default=".hgs/assembly_ledger.json", help="Output ledger JSON path")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if any registered file is missing/unreadable")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest_path = repo_root / args.manifest
    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")

    manifest = parse_manifest(read_text(manifest_path))
    entrypoint = normalize_registered_path(manifest["entrypoint"])
    load_order = [normalize_registered_path(p) for p in manifest.get("load_order", [])]
    tool_load_order = [normalize_registered_path(p) for p in manifest.get("tool_load_order", [])]
    documentation_load_order = [normalize_registered_path(p) for p in manifest.get("documentation_load_order", [])]

    registered_paths = [entrypoint] + load_order + tool_load_order + documentation_load_order

    # preserve order while detecting duplicates
    seen = set()
    deduped: List[str] = []
    duplicates: List[str] = []
    for p in registered_paths:
        if p in seen:
            duplicates.append(p)
            continue
        seen.add(p)
        deduped.append(p)

    loaded_files, missing_files = load_registered_files(repo_root, deduped)
    expected_counts = compute_expected_counts(deduped)

    roles_loaded = sum(1 for x in loaded_files if x.category == "role" and x.loaded)
    tools_loaded = sum(1 for x in loaded_files if x.category == "tool" and x.loaded)
    protocols_loaded = sum(1 for x in loaded_files if x.category == "protocol" and x.loaded)
    docs_loaded = sum(1 for x in loaded_files if x.category == "doc" and x.loaded)

    release_root = repo_root / "Release"
    unregistered_release_files = find_unregistered_release_files(
        all_release_files=list_release_files(release_root),
        registered_paths=deduped,
        entrypoint=manifest["entrypoint"],
        manifest_path=args.manifest,
    )

    release_source_only = True
    assembly_status = "pass" if not missing_files else "fail"

    ledger = AssemblyLedger(
        package_version=manifest.get("package_version", "unknown"),
        entrypoint=manifest.get("entrypoint", ""),
        default_route_mode=manifest.get("default_route_mode", "unknown"),
        action_protocol=manifest.get("action_protocol"),
        clearance_protocol=manifest.get("clearance_protocol"),
        release_root="Release",
        manifest_path=args.manifest,
        release_source_only=release_source_only,
        roles_expected=expected_counts["role"],
        tools_expected=expected_counts["tool"],
        protocols_expected=expected_counts["protocol"],
        docs_expected=expected_counts["doc"],
        roles_loaded=roles_loaded,
        tools_loaded=tools_loaded,
        protocols_loaded=protocols_loaded,
        docs_loaded=docs_loaded,
        active_actions_count=len(manifest.get("active_actions", [])),
        active_action_batches=list(manifest.get("active_action_batches", [])),
        risk_gates=list(manifest.get("risk_gates", [])),
        loaded_files=[asdict(x) for x in loaded_files],
        missing_files=missing_files,
        duplicate_registrations=duplicates,
        unregistered_release_files=unregistered_release_files,
        assembly_status=assembly_status,
    )

    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(asdict(ledger), ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(asdict(ledger), ensure_ascii=False, indent=2))

    if args.strict and assembly_status != "pass":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
