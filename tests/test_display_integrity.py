import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_display_integrity_passes_on_generated_reports(tmp_path):
    subprocess.run([sys.executable, str(ROOT/'scripts/validate_manifest_schema.py'), '--repo-root', str(ROOT), '--strict'], check=True)
    subprocess.run([sys.executable, str(ROOT/'scripts/assemble_release.py'), '--repo-root', str(ROOT), '--strict'], check=True)
    subprocess.run([sys.executable, str(ROOT/'scripts/verify_release.py'), '--repo-root', str(ROOT), '--strict'], check=True)
    subprocess.run([sys.executable, str(ROOT/'scripts/bootstrap_full_loop_dry_run.py'), '--repo-root', str(ROOT), '--issue-input', str(ROOT/'examples/issue_input.json'), '--strict'], check=True)
    subprocess.run([sys.executable, str(ROOT/'scripts/render_automation_acceptance_report.py'), '--repo-root', str(ROOT), '--strict'], check=True)
    output = tmp_path/'display.json'
    subprocess.run([sys.executable, str(ROOT/'scripts/validate_display_integrity.py'), '--repo-root', str(ROOT), '--output', str(output), '--strict'], check=True)
    report = json.loads(output.read_text(encoding='utf-8'))
    assert report['display_integrity_status'] == 'pass'
