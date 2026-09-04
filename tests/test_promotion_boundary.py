# SPDX-License-Identifier: Apache-2.0

"""Repository-owned promotion boundary coherence (offline).

Pins the relationships between the files MNCDS owns for promotion: the
candidate revision, the boundary's required evidence, the authority map,
the obligation set, and the development record. Cross-repository behavior
(pinned evaluator, transport claim) is covered by
scripts/assert-promotion-vectors.sh in CI.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from mncds_validator.obligations import evaluate_obligations
from mncds_validator.schemas import schema_errors

ROOT = Path(__file__).resolve().parents[1]
PROMOTION = ROOT / "promotion"
HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")

REPO = "epi13/machine-native-complexity-development-specification"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_candidate_is_exactly_bound() -> None:
    candidate = _load(PROMOTION / "candidate.json")
    assert candidate["repository"] == REPO
    assert HEX40.match(candidate["commit"]), "candidate must be an immutable revision"
    assert (ROOT / candidate["record"]).is_file()
    for obligation in candidate["obligations"]:
        assert (ROOT / obligation).is_file()


def test_boundary_requires_owner_evidence_only() -> None:
    boundary = _load(PROMOTION / "mncds-promotion.boundary.json")
    assert boundary["schema_version"] == "mncs-promotion-boundary/0.1"
    assert boundary["boundary_id"] == "mncds-promotion"
    assert boundary["subject_repository"] == REPO
    assert boundary["require_subject_binding"] is True
    required = {entry["check_id"]: entry for entry in boundary["required_evidence"]}
    assert set(required) == {"mncds-development-record", "mncds-obligations"}
    for entry in required.values():
        assert entry["authority"] == "machine-native-complexity-development-specification"
    assert boundary["obligation_check_id"] == "mncds-obligations"
    assert boundary["tolerated_obligations"] == []


def test_authority_map_covers_boundary_requirements() -> None:
    boundary = _load(PROMOTION / "mncds-promotion.boundary.json")
    authority_map = _load(PROMOTION / "authority-map.json")
    assert authority_map["schema_version"] == "mncs-authority-map/0.1"
    for entry in boundary["required_evidence"]:
        binding = authority_map["authorities"][entry["check_id"]]
        assert binding["authority"] == entry["authority"]
        assert binding["provider"] == "mncds"
        assert binding["repository"] == REPO


def test_obligations_are_candidate_bound_and_resolved() -> None:
    candidate = _load(PROMOTION / "candidate.json")
    records = [_load(ROOT / path) for path in candidate["obligations"]]
    assert records, "candidate must carry at least one obligation record"
    for record in records:
        assert schema_errors(record, "mncds-obligation-record-0.2") == []
        assert record["subject"] == {
            "repository": candidate["repository"],
            "commit": candidate["commit"],
        }
    evaluation = evaluate_obligations(
        records,
        subject_repository=candidate["repository"],
        subject_commit=candidate["commit"],
    )
    assert evaluation.verdict == "PASS"


def test_development_record_validates_pass() -> None:
    from mncds_validator.mncds import validate_development_record

    candidate = _load(PROMOTION / "candidate.json")
    report = validate_development_record(ROOT / candidate["record"])
    assert report.valid and report.supported
    assert report.computed_status == "PASS"
