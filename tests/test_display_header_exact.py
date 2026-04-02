from pathlib import Path
import json, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]

def run(cmd):
    return subprocess.run([sys.executable, *cmd], cwd=ROOT, check=True, capture_output=True, text=True)

def test_display_header_and_mode_are_exact():
    run(["scripts/bootstrap_full_loop_dry_run.py","--issue-input","examples/issue_input.json","--strict"])
    data = json.loads((ROOT/".hgs/full_loop_dry_run.json").read_text(encoding="utf-8"))
    assert data["response_header"] == "自动化链路：已开启"
    assert data["display_mode"] == "forensic"
    assert data["display_mode_text"] == "全审计"
