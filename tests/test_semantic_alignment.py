import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_semantic_alignment_report_contains_explanations(tmp_path):
    output = tmp_path / 'semantic.json'
    subprocess.run([sys.executable, str(ROOT/'scripts/validate_release_semantic_alignment.py'), '--repo-root', str(ROOT), '--output', str(output)], check=True)
    report = json.loads(output.read_text(encoding='utf-8'))
    assert 'semantic_explanations' in report
    auth = report['semantic_explanations']['auth']
    assert 'bucket_reports' in auth
    assert 'explanation' in auth
    assert 'owner' in auth['bucket_reports']
