#!/usr/bin/env python3
"""Bootstrap repository invariants for MNCDS.

This checker intentionally uses only the Python standard library so it can run before
the reference validator/tooling migration is complete. It checks repository structure
and migration metadata; it is not an MNCDS conformance validator.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "INTEROPERABILITY.md",
    "MIGRATION.md",
    "spec/README.md",
    "schemas/README.md",
    "conformance/README.md",
    "rfcs/README.md",
    "docs/architecture.md",
    "migration/inventory.json",
]

ALLOWED_DISPOSITIONS = {
    "MOVE",
    "KEEP_IN_MNCS",
    "SHARED_INTERFACE",
    "SPLIT",
    "REVIEW_REQUIRED",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    errors = 0

    for relative in REQUIRED_PATHS:
        path = ROOT / relative
        if not path.exists():
            fail(f"required path missing: {relative}")
            errors += 1

    inventory_path = ROOT / "migration/inventory.json"
    if inventory_path.exists():
        try:
            inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"cannot parse migration inventory: {exc}")
            errors += 1
        else:
            if inventory.get("format") != "mncds-repository-migration-inventory-0.1":
                fail("unexpected migration inventory format")
                errors += 1

            declared = set(inventory.get("dispositions", []))
            if declared != ALLOWED_DISPOSITIONS:
                fail(
                    "migration disposition set mismatch: "
                    f"expected {sorted(ALLOWED_DISPOSITIONS)}, got {sorted(declared)}"
                )
                errors += 1

            items = inventory.get("items")
            if not isinstance(items, list) or not items:
                fail("migration inventory must contain at least one item")
                errors += 1
            else:
                for index, item in enumerate(items):
                    if not isinstance(item, dict):
                        fail(f"migration item {index} is not an object")
                        errors += 1
                        continue
                    if not item.get("source"):
                        fail(f"migration item {index} has no source")
                        errors += 1
                    if item.get("disposition") not in ALLOWED_DISPOSITIONS:
                        fail(
                            f"migration item {index} has invalid disposition: "
                            f"{item.get('disposition')!r}"
                        )
                        errors += 1
                    if not item.get("reason"):
                        fail(f"migration item {index} has no reason")
                        errors += 1

    readme = ROOT / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        required_phrases = [
            "independently versioned, governed, and released",
            "Machine-Native Complexity Standard (MNCS)",
            "canonical home of MNCDS",
        ]
        for phrase in required_phrases:
            if phrase not in text:
                fail(f"README boundary phrase missing: {phrase!r}")
                errors += 1

    if errors:
        print(f"repository bootstrap check failed with {errors} error(s)", file=sys.stderr)
        return 1

    print("MNCDS repository bootstrap checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
