#!/usr/bin/env python3
"""Generate the bounded corpus for implementations/mncs/development.mncs.

The corpus exercises every decisive cell of the machine-native MNCDS decision
core against mncs.core.status:

- contribution(): evidentiary roles propagate producer status; all other roles
  are dominance-neutral;
- same_epoch_feedback_eligible(): final-partition evidence is never eligible
  as same-epoch repair feedback (RFC 0005 rule B7);
- selection_outcome(): FAIL dominates; UNKNOWN fails closed under reject,
  survives only under explicit accept-with-UNKNOWN human review; PASS passes.

Usage:
    python3 implementations/mncs/gen_development_corpus.py \
        > implementations/mncs/development-corpus.json
"""

from __future__ import annotations

import json
import sys

MODULE = "mncs.family.development.v01"
STATUS_MODULE = "mncs.core.status.v1"

ROLE = f"mncs:0.2:finite-type:{MODULE}::Role"
ROLE_VARIANTS = [
    "DevelopmentFeedback",
    "SelectionEvidence",
    "FinalEvaluation",
    "Reproduction",
    "Diagnostic",
]
STATUS = f"mncs:0.2:finite-type:{STATUS_MODULE}::Status"
STATUS_VARIANTS = ["PASS", "FAIL", "UNKNOWN"]
POLICY = f"mncs:0.2:finite-type:{MODULE}::UnknownPolicy"
POLICY_VARIANTS = ["Reject", "HumanReview"]


def finite(type_identity: str, variants: list[str], name: str, discriminant: int) -> dict:
    variant_base = type_identity.replace("finite-type", "finite-variant")
    return {
        "finite": {
            "type_identity": type_identity,
            "variant_identity": f"{variant_base}::{variants[discriminant]}",
            "discriminant": discriminant,
        }
    }


def role(index: int) -> dict:
    return finite(ROLE, ROLE_VARIANTS, "Role", index)


def status(index: int) -> dict:
    return finite(STATUS, STATUS_VARIANTS, "Status", index)


def policy(index: int) -> dict:
    return finite(POLICY, POLICY_VARIANTS, "UnknownPolicy", index)


def boolean(value: bool) -> dict:
    return {"boolean": {"value": value}}


def case(case_id: str, function: str, arguments: list[dict], expected: dict) -> dict:
    return {
        "id": case_id,
        "request": {
            "schema_version": "0.1",
            "target": {"module": MODULE, "function": function},
            "arguments": arguments,
            "step_budget": 1024,
        },
        "expected": [expected],
    }


def main() -> int:
    cases: list[dict] = []

    # contribution(): propagation matrix over decisive cells.
    for role_index, role_name in enumerate(ROLE_VARIANTS):
        for status_index, status_name in enumerate(STATUS_VARIANTS):
            expected = (
                status_index
                if role_name in {"SelectionEvidence", "FinalEvaluation"}
                else 0  # PASS is the dominance-neutral element
            )
            cases.append(
                case(
                    f"contribution-{role_name.lower()}-{status_name.lower()}",
                    "contribution",
                    [role(role_index), status(status_index)],
                    status(expected),
                )
            )

    # same_epoch_feedback_eligible(): RFC 0005 rule B7.
    eligible = {
        "DevelopmentFeedback": True,
        "SelectionEvidence": True,
        "FinalEvaluation": False,
        "Reproduction": True,
        "Diagnostic": True,
    }
    for role_index, role_name in enumerate(ROLE_VARIANTS):
        cases.append(
            case(
                f"feedback-eligible-{role_name.lower()}",
                "same_epoch_feedback_eligible",
                [role(role_index)],
                boolean(eligible[role_name]),
            )
        )

    # is_evidentiary().
    evidentiary = {
        "DevelopmentFeedback": False,
        "SelectionEvidence": True,
        "FinalEvaluation": True,
        "Reproduction": False,
        "Diagnostic": False,
    }
    for role_index, role_name in enumerate(ROLE_VARIANTS):
        cases.append(
            case(
                f"is-evidentiary-{role_name.lower()}",
                "is_evidentiary",
                [role(role_index)],
                boolean(evidentiary[role_name]),
            )
        )

    # selection_outcome(): tri-state discipline including fail-closed paths.
    # aggregate, policy, review_accepted -> expected
    selections = [
        (1, 0, False, 1),  # FAIL + reject -> FAIL
        (1, 1, True, 1),   # FAIL + review + accept -> FAIL still dominates
        (2, 0, False, 1),  # UNKNOWN + reject -> FAIL (fail closed)
        (2, 0, True, 1),   # UNKNOWN + reject + spurious accept flag -> FAIL
        (2, 1, True, 2),   # UNKNOWN + review + explicit accept -> UNKNOWN preserved
        (2, 1, False, 1),  # UNKNOWN + review + missing acceptance -> FAIL
        (0, 0, False, 0),  # PASS + reject -> PASS
        (0, 1, True, 0),   # PASS + review -> PASS
    ]
    for index, (aggregate, pol, accepted, expected) in enumerate(selections):
        names = {0: "pass", 1: "fail", 2: "unknown"}
        cases.append(
            case(
                f"selection-{names[aggregate]}-{['reject', 'review'][pol]}-{str(accepted).lower()}",
                "selection_outcome",
                [status(aggregate), policy(pol), boolean(accepted)],
                status(expected),
            )
        )

    corpus = {
        "schema_version": "0.1",
        "name": "mncds-family-development",
        "cases": cases,
    }
    json.dump(corpus, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
