#!/usr/bin/env python3
"""Executable MNCDS conformance corpus runner.

Loads one or more corpus manifests, applies their declared mutations to the
base records, validates each resulting record with the reference validator,
and compares the outcome against the expected tri-state result.

Corpus manifest format (version 1):

{
  "schema_version": "1",
  "mncds_version": "<record version the corpus targets>",
  "base_record": "<path relative to repository root>",
  "cases": [
    {
      "id": "<case id>",
      "mutations": [
        {"op": "set", "path": "/a/b", "value": true},
        {"op": "remove", "path": "/c"},
        {"path": "/d/e", "value": 1}
      ],
      "base_record": "<optional per-case base override>",
      "expected": {"valid": false, "computed_status": "FAIL",
                   "issue_codes": ["code"]}
    }
  ]
}

A mutation object without "op" is a set. Paths are JSON pointers against the
decoded record. Expected issue_codes must match the produced issue-code set
exactly. Validation never executes evidence and never reads producer systems.
"""

# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mncds_validator.mncds import validate_development_value


class CorpusError(Exception):
    """A corpus manifest or vector is structurally unusable."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CorpusError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CorpusError(f"{path} must contain a JSON object")
    return value


def _pointer_tokens(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise CorpusError(f"JSON pointer must start with '/': {pointer}")
    tokens = [token.replace("~1", "/").replace("~0", "~") for token in pointer.split("/")[1:]]
    if not tokens:
        raise CorpusError(f"empty JSON pointer: {pointer}")
    return tokens


def apply_pointer(document: dict[str, Any], pointer: str, value: Any) -> None:
    tokens = _pointer_tokens(pointer)
    target: Any = document
    for token in tokens[:-1]:
        if isinstance(target, list):
            target = target[int(token)]
        else:
            child = target.get(token)
            if not isinstance(child, (dict, list)):
                raise CorpusError(f"pointer traverses non-container at {pointer}")
            target = child
    last = tokens[-1]
    if isinstance(target, list):
        target[int(last)] = value
    else:
        target[last] = value


def remove_pointer(document: dict[str, Any], pointer: str) -> None:
    tokens = _pointer_tokens(pointer)
    target: Any = document
    for token in tokens[:-1]:
        target = target[int(token)] if isinstance(target, list) else target[token]
    last = tokens[-1]
    if isinstance(target, list):
        del target[int(last)]
    elif isinstance(target, dict):
        target.pop(last, None)


def apply_mutations(record: dict[str, Any], mutations: list[dict[str, Any]]) -> None:
    for index, mutation in enumerate(mutations):
        operation = mutation.get("op", "set")
        if operation == "set":
            apply_pointer(record, str(mutation["path"]), mutation.get("value"))
        elif operation == "remove":
            remove_pointer(record, str(mutation["path"]))
        else:
            raise CorpusError(f"mutation {index} has unsupported op: {operation!r}")


def run_corpus(manifest_path: Path) -> tuple[list[str], int]:
    manifest = load_json(manifest_path)
    default_base = manifest.get("base_record")
    if not isinstance(default_base, str):
        raise CorpusError(f"{manifest_path}: corpus manifest needs a base_record")
    failures: list[str] = []
    ran = 0
    for case in manifest.get("cases") or []:
        if not isinstance(case, dict) or "id" not in case or "expected" not in case:
            raise CorpusError(f"{manifest_path}: each case needs id and expected")
        case_id = str(case["id"])
        ran += 1
        base = ROOT / case.get("base_record", default_base)
        record = copy.deepcopy(load_json(base))
        try:
            apply_mutations(record, case.get("mutations") or [])
        except (CorpusError, KeyError, ValueError, IndexError) as exc:
            failures.append(f"{manifest_path}:{case_id}: unusable mutation ({exc})")
            continue
        report = validate_development_value(record, target=case_id)
        actual_codes = sorted({issue.code for issue in report.issues})
        expected = case["expected"]
        problems: list[str] = []
        if report.valid != bool(expected.get("valid")):
            problems.append(f"valid={report.valid} want {expected.get('valid')}")
        if report.category != expected.get("computed_status"):
            problems.append(
                f"status={report.category} want {expected.get('computed_status')}"
            )
        want_codes = sorted(set(expected.get("issue_codes") or []))
        if actual_codes != want_codes:
            problems.append(f"codes={actual_codes} want {want_codes}")
        if "warning_codes" in expected:
            actual_warnings = sorted({issue.code for issue in report.warnings})
            want_warnings = sorted(set(expected["warning_codes"]))
            if actual_warnings != want_warnings:
                problems.append(f"warnings={actual_warnings} want {want_warnings}")
        if problems:
            failures.append(f"{manifest_path}:{case_id}: " + "; ".join(problems))
    return failures, ran


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "corpora",
        nargs="*",
        type=Path,
        help="corpus manifests (default: every conformance/**/corpus*.json)",
    )
    args = parser.parse_args(argv)

    corpora = args.corpora
    if not corpora:
        corpora = sorted((ROOT / "conformance").rglob("corpus*.json"))
    if not corpora:
        print("no corpus manifests found", file=sys.stderr)
        return 2

    total = 0
    all_failures: list[str] = []
    for manifest in corpora:
        try:
            failures, ran = run_corpus(manifest)
        except CorpusError as exc:
            print(f"CORPUS ERROR: {exc}", file=sys.stderr)
            return 2
        total += ran
        mark = "ok" if not failures else "FAILED"
        print(f"{manifest.relative_to(ROOT)}: {ran} vectors {mark}")
        all_failures.extend(failures)

    for failure in all_failures:
        print(f"  FAIL {failure}", file=sys.stderr)
    print(f"{total - len(all_failures)}/{total} conformance vectors passed")
    return 1 if all_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
