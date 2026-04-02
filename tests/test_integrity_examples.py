import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_supported_issue_types_have_examples():
    manifest = json.loads((ROOT/'Release/MANIFEST.json').read_text(encoding='utf-8'))
    supported = set(manifest['automation_policy']['runtime_route_policy']['supported_issue_types'])
    expected = {f'issue_input_{x}.json' for x in supported if x != 'console'} | {'issue_input.json'}
    existing = {p.name for p in (ROOT/'examples').glob('issue_input*.json')}
    assert expected.issubset(existing)
