import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def test_normalize_issue_input_infers_issue_type(tmp_path):
    issue = {
        "title": "JWT scope lost after refresh",
        "current_question": "token scope missing",
    }
    issue_file = tmp_path / "issue.json"
    issue_file.write_text(json.dumps(issue))
    out = tmp_path / "out.json"
    subprocess.run([
        sys.executable, str(ROOT/"scripts/normalize_issue_input.py"),
        "--repo-root", str(ROOT), "--issue-input", str(issue_file), "--output", str(out)
    ], check=True)
    data = json.loads(out.read_text())
    assert data["normalized_issue"]["issue_type"] == "auth"  # inferred from keywords