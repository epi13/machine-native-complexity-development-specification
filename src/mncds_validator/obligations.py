"""Owner-native evaluation of MNCDS obligation sets.

Implements ``docs/mncds-check-catalog.md`` (``mncds-obligations``) verbatim:
an obligation resolution is authoritative only when its kind coheres
(``resolved`` with ``resolution.fixed``, ``rejected`` with
``resolution.rejected``), evidence refs are non-empty, the resolver and
time are named, no resolution block accompanies ``open``, keys are unique
within the set, and the set is scoped to one exactly-bound subject.

Result mapping (catalog-literal):

- every obligation ``resolved``, or no obligation ``required`` -> PASS;
- a ``required`` obligation still ``open`` -> UNKNOWN with its key;
- a ``required`` obligation with an authoritative negative resolution
  (``rejected``) -> FAIL;
- malformed, contradictory (duplicate key), incoherent or anonymous
  resolution, or revision-unbound input -> no claim is established
  (``ObligationNoClaimError``; never UNKNOWN, never PASS).

Optional obligations stay visible in ``unresolved``/``rejected_optional``
but never decide the verdict on their own.
"""

# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .errors import MncdsError
from .schemas import schema_errors

SCHEMA_NAME = "mncds-obligation-record-0.2"

_HEX40 = frozenset("0123456789abcdefABCDEF")


class ObligationNoClaimError(MncdsError):
    """Raised when the input establishes no valid obligation claim."""


@dataclass(frozen=True)
class ObligationEvaluation:
    """Verdict over one subject-scoped obligation set."""

    verdict: str  # PASS, UNKNOWN, or FAIL
    subject_repository: str
    subject_commit: str
    resolved: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)
    rejected_optional: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "mncds-obligation-evaluation/0.1",
            "verdict": self.verdict,
            "subject": {
                "repository": self.subject_repository,
                "commit": self.subject_commit,
            },
            "resolved": sorted(self.resolved),
            "unresolved": sorted(self.unresolved),
            "rejected": sorted(self.rejected),
            "rejected_optional": sorted(self.rejected_optional),
        }


def _is_hex40(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(char in _HEX40 for char in value)
    )


def _resolution_is_authoritative(record: dict[str, Any]) -> bool:
    """Check the catalog's resolution-authority rules for one record."""
    status = record.get("status")
    resolution = record.get("resolution")
    if status == "open":
        return resolution is None
    if not isinstance(resolution, dict):
        return False
    kind = resolution.get("resolution")
    if status == "resolved" and kind != "fixed":
        return False
    if status == "rejected" and kind != "rejected":
        return False
    if status not in ("resolved", "rejected"):
        return False
    if not resolution.get("evidence_refs"):
        return False
    return bool(resolution.get("resolved_by") and resolution.get("resolved_at"))


def evaluate_obligations(
    records: list[dict[str, Any]],
    *,
    subject_repository: str,
    subject_commit: str,
) -> ObligationEvaluation:
    """Evaluate an obligation set scoped to one exactly-bound subject."""
    if not subject_repository or not _is_hex40(subject_commit):
        raise ObligationNoClaimError("evaluation subject must be exactly bound")
    if not isinstance(records, list):
        raise ObligationNoClaimError("obligation input must be a record array")

    seen_keys: set[str] = set()
    resolved: list[str] = []
    unresolved: list[str] = []
    optional_open: list[str] = []
    rejected: list[str] = []
    rejected_optional: list[str] = []

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ObligationNoClaimError(f"obligation #{index} is not an object")
        errors = schema_errors(record, SCHEMA_NAME)
        if errors:
            raise ObligationNoClaimError(
                f"obligation #{index} is malformed: {errors[0]}"
            )
        key = record["obligation_key"]
        if key in seen_keys:
            raise ObligationNoClaimError(
                f"contradictory duplicate obligation_key: {key}"
            )
        seen_keys.add(key)
        subject = record.get("subject", {})
        if (
            subject.get("repository") != subject_repository
            or subject.get("commit") != subject_commit
        ):
            raise ObligationNoClaimError(
                f"obligation {key} is bound to another subject"
            )
        if not _resolution_is_authoritative(record):
            raise ObligationNoClaimError(
                f"obligation {key} carries an incoherent or anonymous resolution"
            )
        required = record.get("required", False) is True
        if record["status"] == "resolved":
            resolved.append(key)
        elif record["status"] == "rejected":
            (rejected if required else rejected_optional).append(key)
        else:  # open
            if required:
                unresolved.append(key)
            else:
                # Optional open obligations stay visible but never decide.
                optional_open.append(key)

    if rejected:
        verdict = "FAIL"
    elif unresolved:
        verdict = "UNKNOWN"
    else:
        verdict = "PASS"

    return ObligationEvaluation(
        verdict=verdict,
        subject_repository=subject_repository,
        subject_commit=subject_commit,
        resolved=resolved,
        unresolved=[*unresolved, *optional_open],
        rejected=rejected,
        rejected_optional=rejected_optional,
    )
