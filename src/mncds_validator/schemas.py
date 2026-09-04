"""Packaged MNCDS JSON Schema discovery and validation."""

# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import math
from importlib.resources import files
from typing import Any, cast

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

from .errors import SchemaNotFoundError

SCHEMA_NAMES = {
    "mncds-development-record": "mncds-development-record.schema.json",
    "mncds-development-record-0.1": "mncds-development-record-0.1.schema.json",
    "mncds-development-record-0.2-alpha": (
        "mncds-development-record-0.2-alpha.schema.json"
    ),
    "mncds-obligation-record-0.1": "mncds-obligation-record-0.1.schema.json",
    "mncds-obligation-record": "mncds-obligation-record-0.2.schema.json",
    "mncds-obligation-record-0.2": "mncds-obligation-record-0.2.schema.json",
}


def load_schema(name: str) -> dict[str, Any]:
    filename = SCHEMA_NAMES.get(name, name)
    if filename not in SCHEMA_NAMES.values():
        raise SchemaNotFoundError(f"unknown schema: {name}")
    candidate = files("mncds_validator.resources.schemas").joinpath(filename)
    if not candidate.is_file():
        raise SchemaNotFoundError(f"schema is not installed: {filename}")
    value: Any = json.loads(candidate.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SchemaError(f"schema {name} is not an object")
    Draft202012Validator.check_schema(value)
    return cast(dict[str, Any], value)


def _nonfinite_paths(value: Any, path: str = "$") -> list[str]:
    if isinstance(value, float) and not math.isfinite(value):
        return [f"{path}: nonfinite numbers are forbidden"]
    if isinstance(value, dict):
        return [
            finding
            for key, child in value.items()
            for finding in _nonfinite_paths(child, f"{path}/{key}")
        ]
    if isinstance(value, list):
        return [
            finding
            for index, child in enumerate(value)
            for finding in _nonfinite_paths(child, f"{path}/{index}")
        ]
    return []


def schema_errors(instance: Any, name: str) -> list[str]:
    validator = Draft202012Validator(load_schema(name), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    rendered = _nonfinite_paths(instance)
    for error in errors:
        location = "/".join(str(part) for part in error.absolute_path) or "$"
        rendered.append(f"{location}: {error.message}")
    return sorted(rendered)
