import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_archive_cleanliness_checks_raw_zip_not_runtime_dir(tmp_path):
    clean_zip = tmp_path / 'clean.zip'
    with zipfile.ZipFile(clean_zip, 'w') as zf:
        zf.writestr('.gitignore', '')
        zf.writestr('.gitattributes', '')
        zf.writestr('.github/workflows/release-runtime-acceptance.yml', 'name: x')
        zf.writestr('README.md', 'ok')
    output = tmp_path / 'archive.json'
    subprocess.run([
        sys.executable,
        str(ROOT / 'scripts' / 'validate_archive_cleanliness.py'),
        '--zip-path', str(clean_zip),
        '--output', str(output),
        '--strict',
    ], check=True)
    report = json.loads(output.read_text(encoding='utf-8'))
    assert report['archive_cleanliness_status'] == 'pass'
    assert report['forbidden_entries'] == []
