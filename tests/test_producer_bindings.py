# SPDX-License-Identifier: Apache-2.0

"""RFC 0005 producer-binding semantics at MNCDS 0.2-alpha.1."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from mncds_validator.mncds import validate_development_value
from mncds_validator.schemas import SCHEMA_NAMES, load_schema, schema_errors

ROOT = Path(__file__).resolve().parents[1]
CASE_STUDY = ROOT / "examples/mncds-0.2-alpha/language-span-fix.development-record.json"
FIXTURE_D4 = ROOT / "examples/mncds-0.2-alpha/d4-release-lifecycle.fixture.json"


def _case_study() -> dict[str, Any]:
    return json.loads(CASE_STUDY.read_text(encoding="utf-8"))


def _fixture_d4() -> dict[str, Any]:
    return json.loads(FIXTURE_D4.read_text(encoding="utf-8"))


def _codes(report) -> set[str]:
    return {issue.code for issue in report.issues}


def _warnings(report) -> set[str]:
    return {issue.code for issue in report.warnings}


def test_alpha_schema_is_packaged_and_discoverable() -> None:
    assert "mncds-development-record-0.2-alpha" in SCHEMA_NAMES
    schema = load_schema("mncds-development-record-0.2-alpha")
    assert schema["properties"]["mncds_version"]["const"] == "0.2-alpha.1"
    assert schema_errors(_case_study(), "mncds-development-record-0.2-alpha") == []


def test_case_study_record_passes_at_d1() -> None:
    report = validate_development_value(_case_study())
    assert report.valid, report.as_dict()
    assert report.computed_status == "PASS"
    assert report.profile == "MNCDS-D1"


def test_d4_fixture_preserves_unknown_from_custody() -> None:
    report = validate_development_value(_fixture_d4())
    assert report.valid, report.as_dict()
    assert report.computed_status == "UNKNOWN"
    assert "protected-evidence-unknown" in _warnings(report)


def test_binding_ids_must_be_unique() -> None:
    record = _case_study()
    record["producer_bindings"][1]["binding_id"] = record["producer_bindings"][0]["binding_id"]
    report = validate_development_value(record)
    assert not report.valid
    assert "duplicate-id" in _codes(report)


def test_digests_are_sha256_only() -> None:
    record = _case_study()
    record["producer_bindings"][3]["content_digest"] = "md5:abcd"
    report = validate_development_value(record)
    assert not report.valid


def test_subject_must_exist_in_ledger() -> None:
    record = _case_study()
    record["producer_bindings"][0]["subject_candidate_id"] = "candidate.ghost"
    report = validate_development_value(record)
    assert "binding-subject-missing" in _codes(report)


def test_rerun_requires_declared_changes() -> None:
    record = _case_study()
    del record["producer_bindings"][4]["declared_changes"]
    report = validate_development_value(record)
    assert "binding-rerun-changes-undeclared" in _codes(report)


def test_rerun_target_must_be_another_binding() -> None:
    record = _case_study()
    record["producer_bindings"][4]["rerun_of_binding_id"] = (
        record["producer_bindings"][4]["binding_id"]
    )
    report = validate_development_value(record)
    assert "binding-rerun-unknown" in _codes(report)


def test_evidentiary_role_requires_supported_compatibility() -> None:
    record = _case_study()
    binding = record["producer_bindings"][3]
    binding["role"] = "selection_evidence"
    binding["compatibility_status"] = "unverified_producer"
    report = validate_development_value(record)
    assert "binding-ineligible-evidence" in _codes(report)
    assert not report.valid


def test_final_evidence_cannot_feed_same_epoch_repair() -> None:
    record = _case_study()
    binding = record["producer_bindings"][2]
    binding["role"] = "final_evaluation_evidence"
    binding.setdefault("declared_scope", {})["feedback_use"] = "same_epoch_repair"
    report = validate_development_value(record)
    assert "binding-feedback-leakage" in _codes(report)


def test_generator_scope_cannot_self_certify() -> None:
    record = _case_study()
    binding = record["producer_bindings"][2]
    binding["role"] = "selection_evidence"
    binding["declared_scope"]["generator_executable_identity"] = (
        record["generator"]["executable_id"]
    )
    report = validate_development_value(record)
    assert "binding-generator-self-certification" in _codes(report)


def test_cross_family_identity_mismatch_fails() -> None:
    record = _case_study()
    record["producer_bindings"][3]["declared_scope"]["candidate_identity"] = (
        "candidate.mncs-language-cdee978"
    )
    report = validate_development_value(record)
    assert "binding-subject-mismatch" in _codes(report)


def test_selected_candidate_fail_evidence_fails_record() -> None:
    record = _fixture_d4()
    record["producer_bindings"][1]["evidence_status"] = "FAIL"
    report = validate_development_value(record)
    assert not report.valid
    assert "selected-binding-fail" in _codes(report)
    assert report.computed_status == "FAIL"


def test_selected_unknown_evidence_is_never_promoted() -> None:
    record = copy.deepcopy(_case_study())
    binding = record["producer_bindings"][4]
    binding["role"] = "final_evaluation_evidence"
    report = validate_development_value(record)
    assert report.valid
    assert report.computed_status == "UNKNOWN"
    assert "selected-binding-unknown" in _warnings(report)


def test_unresolvable_evidentiary_identity_stays_unknown() -> None:
    record = copy.deepcopy(_case_study())
    binding = record["producer_bindings"][4]
    binding["role"] = "selection_evidence"
    binding["evidence_status"] = "PASS"
    binding.pop("content_digest")
    report = validate_development_value(record)
    assert report.valid
    assert report.computed_status == "UNKNOWN"
    assert "selected-binding-unresolvable" in _warnings(report)


def test_diagnostic_roles_do_not_propagate_status() -> None:
    record = _fixture_d4()
    harness = next(
        item for item in record["producer_bindings"] if item["binding_id"].endswith("harness-actor")
    )
    harness["evidence_status"] = "FAIL"
    report = validate_development_value(record)
    assert report.valid
    assert report.computed_status == "UNKNOWN"


def test_partition_reference_must_be_declared() -> None:
    record = _case_study()
    record["producer_bindings"][2]["partition_id"] = "partition.final"
    report = validate_development_value(record)
    assert "binding-partition-missing" in _codes(report)


def test_older_versions_remain_dispatched_exactly() -> None:
    draft = json.loads(
        (ROOT / "examples/mncds-d4/development-record.json").read_text(encoding="utf-8")
    )
    rc = json.loads(
        (ROOT / "examples/mncds-0.1-rc/development-record.json").read_text(encoding="utf-8")
    )
    assert validate_development_value(draft).supported
    assert validate_development_value(rc).supported
    mutated = copy.deepcopy(rc)
    mutated["schema_version"] = "0.9.0"
    mutated["mncds_version"] = "0.9.0"
    report = validate_development_value(mutated)
    assert report.category == "UNSUPPORTED"
    assert "unsupported-version" in _codes(report)


@pytest.mark.parametrize(
    "path",
    [
        "examples/mncds-0.2-alpha/language-span-fix.development-record.json",
        "examples/mncds-0.2-alpha/d4-release-lifecycle.fixture.json",
        "examples/mncds-0.1-rc/development-record.json",
        "examples/mncds-d4/development-record.json",
    ],
)
def test_packaged_examples_validate(path: str) -> None:
    value = json.loads((ROOT / path).read_text(encoding="utf-8"))
    report = validate_development_value(value)
    assert report.supported, path
    assert report.valid, f"{path}: {report.as_dict()}"
