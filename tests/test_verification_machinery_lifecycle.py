from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "schemas/mncds-verification-machinery-lifecycle-0.1.schema.json").read_text()
)


def test_native_cutover_can_reclassify_parity_without_ordinary_suite_cost() -> None:
    record = {
        "schema_version": "mncds.verification-machinery-lifecycle/0.1",
        "machinery_identity": "mncs-forge:differential-assurance-vectors",
        "machinery_kind": "differential_oracle",
        "state": "reference_only",
        "canonical_authority": "mncs-forge:native-assurance",
        "ordinary_verification": False,
        "evidence_refs": ["mncs-forge/tests/test_mncs_assurance.py"],
        "retirement": {
            "decision": "retain_reference",
            "reason": "native assurance state machine is canonical; vectors remain useful for scheduled parity",
            "historical_identity": "mncs-forge:differential-assurance-vectors:history",
        },
    }
    assert list(Draft202012Validator(SCHEMA).iter_errors(record)) == []


def test_pressure_reproducer_requires_an_upstream_regression_before_retirement() -> None:
    record = {
        "schema_version": "mncds.verification-machinery-lifecycle/0.1",
        "machinery_identity": "mncs-test:callable-provider-reproducer",
        "machinery_kind": "pressure_reproducer",
        "state": "retired",
        "canonical_authority": "mncs-language:typed-invocation",
        "owning_regression": "mncs-language:generic-callable-identity-regression",
        "ordinary_verification": False,
        "evidence_refs": ["MNCS-LANG-5E290D20B90B"],
        "retirement": {
            "decision": "retain_reference",
            "reason": "the owning regression is permanent; the consumer workaround is removed",
            "replacement_identity": "mncs-language:generic-callable-identity-regression",
        },
    }
    assert list(Draft202012Validator(SCHEMA).iter_errors(record)) == []
