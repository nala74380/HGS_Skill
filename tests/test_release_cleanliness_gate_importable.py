import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_cleanliness_gate_importable():
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'release_cleanliness_gate.py'), '--help'], check=True)
