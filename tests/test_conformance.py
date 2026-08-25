# SPDX-License-Identifier: Apache-2.0

"""Conformance corpus runner is deterministic and self-verifying."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE = ROOT / "conformance"


def _load_runner():
    spec = importlib.util.spec_from_file_location(
        "mncds_run_corpus", CONFORMANCE / "run_corpus.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_packaged_corpus_passes() -> None:
    runner = _load_runner()
    corpora = sorted(CONFORMANCE.rglob("corpus*.json"))
    assert corpora, "conformance corpora are missing"
    failures: list[str] = []
    total = 0
    for manifest in corpora:
        corpus_failures, ran = runner.run_corpus(manifest)
        total += ran
        failures.extend(corpus_failures)
    assert not failures, "\n".join(failures)
    assert total >= 60, f"expected a substantial corpus, found {total} vectors"


def test_mutations_support_set_and_remove() -> None:
    runner = _load_runner()
    document = {"a": {"b": [1, 2]}, "c": 3}
    runner.apply_mutations(
        document,
        [
            {"path": "/a/c", "value": True},
            {"op": "remove", "path": "/c"},
            {"path": "/a/b/0", "value": 9},
        ],
    )
    assert document == {"a": {"b": [9, 2], "c": True}}


def test_bad_pointers_raise_corpus_error() -> None:
    runner = _load_runner()
    with pytest.raises(runner.CorpusError):
        runner.apply_mutations({}, [{"path": "no-slash", "value": 1}])


def test_unsupported_version_is_reported_not_approximated() -> None:
    from mncds_validator.mncds import validate_development_value

    report = validate_development_value({"mncds_version": "7.7.7"})
    assert report.supported is False
    assert report.category == "UNSUPPORTED"
