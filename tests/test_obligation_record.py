# SPDX-License-Identifier: Apache-2.0

"""MNCDS obligation records: schema acceptance, rejection, and lifecycle rules."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from mncds_validator.schemas import SCHEMA_NAMES, load_schema, schema_errors

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_NAME = "mncds-obligation-record-0.1"
OPEN_EXAMPLE = ROOT / "examples/mncds-obligations/open-required-obligation.json"
RESOLVED_EXAMPLE = ROOT / "examples/mncds-obligations/resolved-obligation.json"


def _open() -> dict[str, Any]:
    return json.loads(OPEN_EXAMPLE.read_text(encoding="utf-8"))


def _resolved() -> dict[str, Any]:
    return json.loads(RESOLVED_EXAMPLE.read_text(encoding="utf-8"))


def test_obligation_schema_is_packaged_and_discoverable() -> None:
    assert SCHEMA_NAME in SCHEMA_NAMES
    schema = load_schema(SCHEMA_NAME)
    assert schema["properties"]["schema_version"]["const"] == "mncds-obligation-record/0.1"
    assert schema_errors(_open(), SCHEMA_NAME) == []
    assert schema_errors(_resolved(), SCHEMA_NAME) == []


def test_open_obligation_needs_no_resolution() -> None:
    record = _open()
    assert record["status"] == "open"
    assert "resolution" not in record
    assert schema_errors(record, SCHEMA_NAME) == []


def test_resolved_obligation_requires_resolution_refs() -> None:
    record = _resolved()
    assert record["status"] == "resolved"
    assert record["resolution"]["evidence_refs"]
    assert schema_errors(record, SCHEMA_NAME) == []

    missing_refs = copy.deepcopy(record)
    missing_refs["resolution"]["evidence_refs"] = []
    assert schema_errors(missing_refs, SCHEMA_NAME) != []

    missing_block = copy.deepcopy(record)
    del missing_block["resolution"]
    assert schema_errors(missing_block, SCHEMA_NAME) != []


def test_open_obligation_rejects_resolution_block() -> None:
    record = _open()
    record["resolution"] = _resolved()["resolution"]
    assert schema_errors(record, SCHEMA_NAME) != []


def test_subject_commit_must_be_exact_revision() -> None:
    record = _open()
    assert schema_errors(record, SCHEMA_NAME) == []
    for bad in ("main", "cdee978", "", "CDEE9783BD9A8E05E487FB0146515AA6700000000"):
        mutated = copy.deepcopy(record)
        mutated["subject"]["commit"] = bad
        assert schema_errors(mutated, SCHEMA_NAME) != [], bad


def test_duplicate_keys_are_detectable_by_consumers() -> None:
    first, second = _open(), _open()
    assert first["obligation_key"] == second["obligation_key"]
    keys = [first["obligation_key"], second["obligation_key"]]
    assert len(set(keys)) != len(keys), "evaluation sets must reject duplicate keys"


def test_rejected_resolution_is_expressible() -> None:
    record = _resolved()
    record["status"] = "rejected"
    record["resolution"]["resolution"] = "rejected"
    assert schema_errors(record, SCHEMA_NAME) == []
