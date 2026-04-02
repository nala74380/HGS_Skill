import json, shutil, subprocess, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_clean_package_builder_excludes_artifacts_and_audits(tmp_path):
    work = tmp_path / 'pkg'
    shutil.copytree(ROOT, work, dirs_exist_ok=True)
    for rel in ['.hgs','hgs','.pytest_cache','scripts/__pycache__']:
        p = work / rel
        p.mkdir(parents=True, exist_ok=True)
        (p/'x.txt').write_text('x', encoding='utf-8')
    out = tmp_path/'clean.zip'
    audit_name = 'build_audit.json'
    subprocess.run([sys.executable, str(work/'scripts/build_clean_release_package.py'), '--repo-root', str(work), '--output-zip', str(out), '--audit-output', audit_name], check=True)
    assert out.exists()
    with zipfile.ZipFile(out, 'r') as zf:
        members = zf.namelist()
    assert not any('.hgs/' in name or '.pytest_cache/' in name or '__pycache__/' in name for name in members)
    report = json.loads((work / audit_name).read_text(encoding='utf-8'))
    assert report['zip_audit']['forbidden_entries'] == []
