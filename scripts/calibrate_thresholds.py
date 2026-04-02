#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
from collections import defaultdict

def calibrate_thresholds(history_dir: Path) -> dict:
    """Load historical issue results and compute optimal thresholds per issue_type."""
    # 这里简化实现：从 .hgs/assembly_ledger.json 或单独的历史记录读取
    # 实际应用中需要解析所有已关闭 issue 的 final_review_result 和 owner_confidence
    # 示例：返回静态覆盖（实际应动态计算）
    return {
        "auth": {"owner_confidence_min_for_direct_dispatch": 80},
        "docs": {"owner_confidence_min_for_direct_dispatch": 60}
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--output', default='.hgs/calibrated_thresholds.json')
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    thresholds = calibrate_thresholds(root / '.hgs')
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(thresholds, indent=2))
    print(json.dumps(thresholds, indent=2))

if __name__ == '__main__':
    main()