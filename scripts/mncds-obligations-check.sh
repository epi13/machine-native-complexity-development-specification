#!/usr/bin/env bash
# Owner-native MNCDS obligation evidence for the mncds-promotion boundary.
#
# Evaluates the repository-owned obligation set for the recorded promotion
# candidate (promotion/candidate.json) with `mncds evaluate-obligations`
# (docs/mncds-check-catalog.md, mncds-obligations) and wraps the owner
# verdict in a check-result/1 transport envelope. The envelope is
# mechanical (ids, subject stamp, unresolved keys); the verdict is MNCDS's.
#
# Exit behavior: PASS exits 0. UNKNOWN/FAIL exits 3 after writing the claim
# so aggregation can decide the boundary (mirrors dogfood project-command).
# No-claim (exit 2, nothing written) records NOT_ESTABLISHED downstream.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CANDIDATE_REPO="$(python3 -c "import json; print(json.load(open('promotion/candidate.json'))['repository'])")"
CANDIDATE_COMMIT="$(python3 -c "import json; print(json.load(open('promotion/candidate.json'))['commit'])")"
mapfile -t OBLIGATIONS < <(python3 -c "import json; [print(p) for p in json.load(open('promotion/candidate.json'))['obligations']]")

python3 -m pip install -q -e . >/tmp/mncds-install.log 2>&1

mncds evaluate-obligations "${OBLIGATIONS[@]}" \
  --subject-repository "$CANDIDATE_REPO" \
  --subject-commit "$CANDIDATE_COMMIT" \
  --json >/tmp/mncds-obligations.json
EVAL_RC=$?
if [ "$EVAL_RC" -eq 2 ]; then
  echo "mncds evaluate-obligations established no claim; emitting nothing" >&2
  exit 2
fi
if [ "$EVAL_RC" -ne 0 ] && [ "$EVAL_RC" -ne 3 ]; then
  echo "mncds evaluate-obligations failed operationally (rc=$EVAL_RC)" >&2
  exit "$EVAL_RC"
fi

mkdir -p .mncs
python3 - "$CANDIDATE_REPO" "$CANDIDATE_COMMIT" <<'PY'
import json, sys
repo, commit = sys.argv[1], sys.argv[2]
evaluation = json.load(open("/tmp/mncds-obligations.json"))
check = {
    "schema_version": "mncs.check-result/1",
    "id": "mncds-obligations",
    "provider": "mncds",
    "verdict": evaluation["verdict"],
    "summary": (
        f"mncds obligations {evaluation['verdict']}: "
        f"{len(evaluation['resolved'])} resolved, "
        f"{len(evaluation['unresolved'])} unresolved, "
        f"{len(evaluation['rejected'])} rejected"
    ),
    "scope": "mncds promotion candidate obligations",
    "claim": "candidate obligations are resolved enough for evaluation",
    "contract_revision": "mncds-obligation-record/0.2",
    "producer_revision": "mncds-validator/0.1-rc.1",
    "subject": {"repository": repo, "commit": commit},
    "references": [
        {
            "kind": "mncds-obligation-record",
            "producer": "mncds",
            "authority": "machine-native-complexity-development-specification",
        }
    ],
}
required = set(evaluation.get("required_unresolved", []))
if evaluation["unresolved"]:
    check["unresolved"] = [
        f"obligation {key} open (required)" if key in required
        else f"obligation {key} open (optional)"
        for key in evaluation["unresolved"]
    ]
json.dump(check, open(".mncs/mncds-obligations-check.json", "w"), indent=2, sort_keys=True)
print(f"mncds-obligations -> {evaluation['verdict']}")
PY
[ "$EVAL_RC" -eq 0 ]
