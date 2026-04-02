import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_cleanliness_report_exposes_scope(tmp_path):
    output = tmp_path / 'runtime_clean.json'
    subprocess.run([
        sys.executable,
        str(ROOT / 'scripts' / 'validate_package_cleanliness.py'),
        '--repo-root', str(ROOT),
        '--output', str(output),
    ], check=True)
    report = json.loads(output.read_text(encoding='utf-8'))
    assert report['cleanliness_scope'] == 'runtime_workspace_after_extraction_or_execution'
    assert 'runtime_workspace_cleanliness_status' in report
