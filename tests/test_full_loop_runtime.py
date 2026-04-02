import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bootstrap_full_loop_uses_runtime_module_and_emits_report(tmp_path):
    subprocess.run([sys.executable, str(ROOT/'scripts/assemble_release.py'), '--repo-root', str(ROOT)], check=True)
    subprocess.run([sys.executable, str(ROOT/'scripts/verify_release.py'), '--repo-root', str(ROOT)], check=True)
    output = tmp_path / 'full_loop.json'
    subprocess.run([
        sys.executable,
        str(ROOT/'scripts/bootstrap_full_loop_dry_run.py'),
        '--repo-root', str(ROOT),
        '--issue-input', 'examples/issue_input_auth.json',
        '--output', str(output),
    ], check=True)
    report = json.loads(output.read_text(encoding='utf-8'))
    assert report['mode'] == 'full_loop'
    assert 'route_drift_report' in report
    assert 'blocking_reasons' in report
