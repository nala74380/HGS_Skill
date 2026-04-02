import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def test_release_runtime_integrity_passes():
    result = subprocess.run([
        sys.executable, str(ROOT/"scripts/validate_release_runtime_integrity.py"),
        "--repo-root", str(ROOT), "--strict"
    ], capture_output=True)
    assert result.returncode == 0