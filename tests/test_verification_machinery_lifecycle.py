from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "schemas/mncds-verification-machinery-lifecycle-0.1.schema.json").read_text()
)
LANGUAGE_ROOT = ROOT.parent / "mncs-language"
MNCS = Path(os.environ.get("MNCS_BINARY", LANGUAGE_ROOT / "target/debug/mncs"))


def _native_lifecycle(request: dict) -> dict:
    environment = dict(os.environ)
    environment["MNCS_LIBRARY_PATH"] = str(LANGUAGE_ROOT / "library")
    with tempfile.TemporaryDirectory(prefix=".mncds-lifecycle-", dir=ROOT) as directory:
        directory_path = Path(directory)
        request_path = directory_path / "request.json"
        result_path = directory_path / "result.json"
        request_path.write_text(json.dumps(request), encoding="utf-8")
        completed = subprocess.run(
            [
                str(MNCS),
                "run-app",
                str(ROOT / "native-applications/verification-machinery-lifecycle.json"),
                "--grant-structured",
                "mncds_artifact",
                "--step-budget",
                "32768",
                "--",
                request_path.relative_to(ROOT).as_posix(),
                result_path.relative_to(ROOT).as_posix(),
            ],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=180,
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout
        return json.loads(result_path.read_text(encoding="utf-8"))


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


def test_native_kernel_enforces_transition_ordinary_and_reproducer_laws() -> None:
    valid = _native_lifecycle(
        {
            "schema_version": "mncds.verification-machinery-lifecycle-kernel-request/1",
            "machinery_kind": "pressure_reproducer",
            "current_state": "active",
            "next_state": "cutover_pending",
            "canonical_authority": "mncs-language:callable-identity",
            "owning_regression": "mncs-language:generic-callable-regression",
            "workaround_removed": False,
            "ordinary_verification": True,
            "cutover_declared": False,
            "parity_established": False,
            "retirement_decision": "delete",
            "replacement_identity": "",
            "historical_identity": "",
        }
    )
    assert valid["valid"] is True
    assert valid["transition_allowed"] is True
    assert valid["ordinary_verification_allowed"] is True
    assert valid["ownership_valid"] is True

    invalid = _native_lifecycle(
        {
            "schema_version": "mncds.verification-machinery-lifecycle-kernel-request/1",
            "machinery_kind": "pressure_reproducer",
            "current_state": "canonical",
            "next_state": "reference_only",
            "canonical_authority": "mncs-language:callable-identity",
            "owning_regression": "mncs-language:generic-callable-regression",
            "workaround_removed": False,
            "ordinary_verification": True,
            "cutover_declared": True,
            "parity_established": True,
            "retirement_decision": "retain_reference",
            "replacement_identity": "",
            "historical_identity": "old-reproducer",
        }
    )
    assert invalid["valid"] is False
    assert invalid["ordinary_verification_allowed"] is False
    assert invalid["retirement_valid"] is False
