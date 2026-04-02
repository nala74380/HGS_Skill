#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from full_loop_runtime import run_full_loop


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--report', default='.hgs/assembly_report.json')
    parser.add_argument('--manifest', default='Release/MANIFEST.json')
    parser.add_argument('--issue-input', required=True)
    parser.add_argument('--output', default='.hgs/full_loop_dry_run.json')
    parser.add_argument('--display-mode', choices=['off', 'compact', 'standard', 'forensic'], default=None)
    parser.add_argument('--strict', action='store_true')
    return parser.parse_args()


def write_output(root: Path, output_rel: str, data: dict) -> None:
    output_path = root / output_rel
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def main() -> int:
    args = parse_args()
    root = Path(args.repo_root).resolve()
    data, exit_code = run_full_loop(root, args.report, args.manifest, args.issue_input, args.display_mode)
    write_output(root, args.output, data)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return exit_code if args.strict else 0


if __name__ == '__main__':
    raise SystemExit(main())
