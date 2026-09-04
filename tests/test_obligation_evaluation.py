# SPDX-License-Identifier: Apache-2.0

"""Owner-native obligation evaluation: lifecycle and adversarial rules.

Implements docs/mncds-check-catalog.md (mncds-obligations) at the unit
level: open required obligations stay UNKNOWN, authoritative rejections
stay FAIL, and malformed or contradictory input establishes no claim
(ObligationNoClaimError -- never UNKNOWN, never PASS).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from mncds_validator.obligations import (
    ObligationNoClaimError,
    evaluate_obligations,
)

ROOT = Path(__file__).resolve().parents[1]
OPEN_EXAMPLE = ROOT / "examples/mncds-obligations/open-required-obligation.json"
RESOLVED_EXAMPLE = ROOT / "examples/mncds-obligations/resolved-obligation.json"

REPO = "epi13/mncs-language"
COMMIT = "cdee9783bd9a8e05e487fb0146515aa670000000"


def _open() -> dict[str, Any]:
    return json.loads(OPEN_EXAMPLE.read_text(encoding="utf-8"))


def _resolved() -> dict[str, Any]:
    return json.loads(RESOLVED_EXAMPLE.read_text(encoding="utf-8"))


def _evaluate(records: list[dict[str, Any]], **overrides: Any):
    params = {"subject_repository": REPO, "subject_commit": COMMIT}
    params.update(overrides)
    return evaluate_obligations(records, **params)


def test_open_required_obligation_is_unknown_with_key() -> None:
    evaluation = _evaluate([_open()])
    assert evaluation.verdict == "UNKNOWN"
    assert evaluation.unresolved == ["pressure.mncs-language.span-fix.unknown-backend"]
    assert evaluation.as_dict()["verdict"] == "UNKNOWN"


def test_resolved_obligation_is_pass() -> None:
    evaluation = _evaluate([_resolved()])
    assert evaluation.verdict == "PASS"
    assert evaluation.resolved == ["pressure.mncs-language.span-fix.unknown-backend"]


def test_empty_set_is_pass() -> None:
    evaluation = _evaluate([])
    assert evaluation.verdict == "PASS"


def test_optional_open_never_decides_alone() -> None:
    record = _open()
    record["required"] = False
    evaluation = _evaluate([record])
    assert evaluation.verdict == "PASS"
    assert record["obligation_key"] in evaluation.unresolved


def test_rejected_required_obligation_is_fail() -> None:
    record = _resolved()
    record["status"] = "rejected"
    record["resolution"] = {
        "resolution": "rejected",
        "evidence_refs": ["sha256:" + "c" * 64],
        "resolved_by": "epi13/mncs-language",
        "resolved_at": "2026-08-21T00:00:00Z",
    }
    evaluation = _evaluate([record])
    assert evaluation.verdict == "FAIL"
    assert evaluation.rejected == [record["obligation_key"]]


def test_rejected_required_beats_open_required() -> None:
    rejected = _resolved()
    rejected["obligation_key"] = "pressure.a"
    rejected["status"] = "rejected"
    rejected["resolution"] = {
        "resolution": "rejected",
        "evidence_refs": ["sha256:" + "c" * 64],
        "resolved_by": "epi13/mncs-language",
        "resolved_at": "2026-08-21T00:00:00Z",
    }
    opened = _open()
    opened["obligation_key"] = "pressure.b"
    evaluation = _evaluate([rejected, opened])
    assert evaluation.verdict == "FAIL"


def test_duplicate_key_is_no_claim() -> None:
    with pytest.raises(ObligationNoClaimError):
        _evaluate([_resolved(), _resolved()])


def test_wrong_subject_is_no_claim() -> None:
    with pytest.raises(ObligationNoClaimError):
        _evaluate([_resolved()], subject_commit="d" * 40)


def test_wrong_repository_is_no_claim() -> None:
    with pytest.raises(ObligationNoClaimError):
        _evaluate([_resolved()], subject_repository="epi13/other")


def test_moving_subject_is_no_claim() -> None:
    with pytest.raises(ObligationNoClaimError):
        _evaluate([_resolved()], subject_commit="main")


def test_malformed_record_is_no_claim() -> None:
    record = _resolved()
    del record["obligation_key"]
    with pytest.raises(ObligationNoClaimError):
        _evaluate([record])


def test_mixed_subjects_are_no_claim() -> None:
    first = _resolved()
    second = _resolved()
    second["obligation_key"] = "pressure.other-subject"
    second["subject"] = {"repository": REPO, "commit": "d" * 40}
    with pytest.raises(ObligationNoClaimError):
        _evaluate([first, second])


def test_anonymous_resolution_is_no_claim() -> None:
    record = _resolved()
    del record["resolution"]["resolved_by"]
    with pytest.raises(ObligationNoClaimError):
        _evaluate([record])


def test_resolution_without_evidence_is_no_claim() -> None:
    record = _resolved()
    record["resolution"]["evidence_refs"] = []
    with pytest.raises(ObligationNoClaimError):
        _evaluate([record])


def test_tolerated_self_resolution_is_no_claim() -> None:
    record = _resolved()
    record["resolution"]["resolution"] = "tolerated"
    with pytest.raises(ObligationNoClaimError):
        _evaluate([record])


def test_open_with_resolution_block_is_no_claim() -> None:
    record = _open()
    record["resolution"] = _resolved()["resolution"]
    with pytest.raises(ObligationNoClaimError):
        _evaluate([record])


def test_resolved_without_resolution_block_is_no_claim() -> None:
    record = _resolved()
    del record["resolution"]
    with pytest.raises(ObligationNoClaimError):
        _evaluate([record])


def test_unbound_evaluation_subject_is_no_claim() -> None:
    with pytest.raises(ObligationNoClaimError):
        _evaluate([], subject_commit="not-a-sha")
