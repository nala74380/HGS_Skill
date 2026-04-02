import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_route_drift_status_is_explained(tmp_path):
    output = tmp_path / 'drift.json'
    subprocess.run([sys.executable, str(ROOT/'scripts/validate_route_policy_drift.py'), '--repo-root', str(ROOT), '--output', str(output)], check=True)
    report = json.loads(output.read_text(encoding='utf-8'))
    assert report['route_policy_drift_status'] in {'pass', 'pass_with_curated_override', 'fail'}
    if report['route_policy_drift_status'] == 'pass_with_curated_override':
        review = report['curated_override_review']
        assert review['reviewed_by']
        assert review['rationale']
