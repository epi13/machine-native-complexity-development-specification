"""Safe JSON object loading for MNCDS development records."""

# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import ManifestError

JSON_MAX_BYTES = 4 * 1024 * 1024


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant is forbidden: {value}")


def load_json_object(path: Path, *, expected_sha256: str | None = None) -> dict[str, Any]:
    del expected_sha256
    try:
        content = path.read_bytes()
        if len(content) > JSON_MAX_BYTES:
            raise ManifestError(f"JSON object exceeds {JSON_MAX_BYTES} bytes: {path}")
        value: Any = json.loads(
            content.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_json_constant,
        )
    except ManifestError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise ManifestError(f"cannot read JSON object {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ManifestError(f"expected a JSON object: {path}")
    return value
