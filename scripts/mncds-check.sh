#!/usr/bin/env bash
# Owner-native MNCDS development-record evidence for the mncds-promotion boundary.
#
# Validates the repository-owned development record for the recorded
# promotion candidate (promotion/candidate.json) with the owner-native
# `mncds validate` CLI, then projects the report through the pinned
# mncs-actions transport adapter. The adapter owns the check-result
# envelope only; all verdict semantics come from docs/mncds-check-catalog.md.
#
# Environment overrides (local runs only; CI uses the pins):
#   MNC_ACTIONS_DIR  use a local mncs-actions checkout instead of cloning
#   MNC_ACTIONS_PIN  immutable transport revision (default below; never @main)
set -uo pipefail

MNC_ACTIONS_PIN="${MNC_ACTIONS_PIN:-4b132651d50b31ae12f5f00c749ee1f32adb6322}"
MNC_ACTIONS_DIR="${MNC_ACTIONS_DIR:-/tmp/mncds-promotion-mncs-actions}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CANDIDATE_REPO="$(python3 -c "import json; print(json.load(open('promotion/candidate.json'))['repository'])")"
CANDIDATE_COMMIT="$(python3 -c "import json; print(json.load(open('promotion/candidate.json'))['commit'])")"
RECORD="$(python3 -c "import json; print(json.load(open('promotion/candidate.json'))['record'])")"

if [ ! -d "$MNC_ACTIONS_DIR" ]; then
  rm -rf "$MNC_ACTIONS_DIR"
  git clone -q --filter=blob:none --no-checkout https://github.com/epi13/mncs-actions "$MNC_ACTIONS_DIR"
  git -C "$MNC_ACTIONS_DIR" fetch -q --depth 1 origin "$MNC_ACTIONS_PIN"
  git -C "$MNC_ACTIONS_DIR" checkout -q "$MNC_ACTIONS_PIN"
fi
ADAPTER="$MNC_ACTIONS_DIR/adapters/mncds_adapter.py"

python3 -m pip install -q -e . >/tmp/mncds-install.log 2>&1

mncds validate "$RECORD" --json >/tmp/mncds-report.json
VALIDATE_RC=$?
if [ "$VALIDATE_RC" -ne 0 ] && [ "$VALIDATE_RC" -ne 3 ]; then
  echo "mncds validate failed operationally (rc=$VALIDATE_RC); no claim established" >&2
  exit "$VALIDATE_RC"
fi

CONTRACT_REVISION="$(python3 -c "import json; print(json.load(open('$RECORD')).get('mncds_version', ''))")"

mkdir -p .mncs
python3 "$ADAPTER" \
  --input /tmp/mncds-report.json \
  --output .mncs/mncds-check.json \
  --check-id mncds-development-record \
  --provider mncds \
  --scope "mncds promotion candidate development record" \
  --claim "candidate development record validates under the MNCDS check catalog" \
  --contract-revision "$CONTRACT_REVISION" \
  --producer-revision "$(mncds version --json | python3 -c "import json,sys; print(json.load(sys.stdin)['mncds_version'])")" \
  --subject-repository "$CANDIDATE_REPO" \
  --subject-commit "$CANDIDATE_COMMIT"

# Propagate the evidence outcome: PASS continues green, anything else is red.
# Aggregation still decides the boundary; this only mirrors dogfood behavior.
VERDICT="$(python3 -c "import json; print(json.load(open('.mncs/mncds-check.json'))['verdict'])")"
echo "mncds-development-record -> $VERDICT"
[ "$VERDICT" = "PASS" ]
