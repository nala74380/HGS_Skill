from pathlib import Path
from scripts.tool_reasoning_engine import execute_tool_reasoning

ROOT = Path(__file__).resolve().parents[1]

def test_tool_reasoning_is_conservative_and_has_trace():
    issue = {'issue_type':'auth','risk_flags':['auth_bypass']}
    result = execute_tool_reasoning(ROOT, 'Release/tools/72_JWT_Inspector_SKILL.md', issue, issue['risk_flags'])
    assert result['confidence'] <= 0.60
    assert 'evidence_trace' in result
    assert 'capability_trace' in result
    assert 'rule_trace' in result
    assert result['status'] == 'structured_capability_signal'
    assert result['finding']['kind'] in {'capability_signal', 'weak_signal', 'no_signal'}
