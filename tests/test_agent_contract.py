"""Pin the MNCDS agent contract to the pressure-semantics ownership."""

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONTRACT = REPO / "AGENTS.md"


def contract_text() -> str:
    assert CONTRACT.is_file(), "AGENTS.md (agent execution contract) is missing"
    return CONTRACT.read_text(encoding="utf-8")


def test_contract_claims_pressure_ownership():
    text = contract_text()
    assert "pressure semantics" in text
    assert "DevelopmentPressure" in text
    assert "mncs-language" in text
    assert "tests/test_agent_contract.py" in text


def test_contract_denies_pressure_as_authorization():
    text = contract_text()
    assert "never authorizes a change" in text
