#!/usr/bin/env bash
# Adversarial promotion vectors for the repository-owned mncds-promotion boundary.
#
# Exercises the real MNCDS boundary, authority map, and evidence through the
# pinned MNCS evaluator and the pinned mncs-actions claim validator. Every
# vector asserts an exact outcome; a green run means the boundary holds.
#
# Environment overrides (local runs only; CI clones the pins):
#   MNC_ACTIONS_DIR  local mncs-actions checkout (default: clone MNC_ACTIONS_PIN)
#   MNCS_DIR         local machine-native-complexity-standard checkout
#                    (default: clone MNCS_PIN)
#   MNC_ACTIONS_PIN  immutable transport revision (never @main)
#   MNCS_PIN         immutable evaluator revision (never @main)
set -uo pipefail

MNC_ACTIONS_PIN="${MNC_ACTIONS_PIN:-4b132651d50b31ae12f5f00c749ee1f32adb6322}"
MNCS_PIN="${MNCS_PIN:-688445783971db9027dc7fc44224bd63acd7a08a}"
MNC_ACTIONS_DIR="${MNC_ACTIONS_DIR:-/tmp/mncds-vectors-mncs-actions}"
MNCS_DIR="${MNCS_DIR:-/tmp/mncds-vectors-mncs-standard}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -x "$MNC_ACTIONS_DIR/adapters/mncds_adapter.py" ]; then
  rm -rf "$MNC_ACTIONS_DIR"
  git clone -q --filter=blob:none --no-checkout https://github.com/epi13/mncs-actions "$MNC_ACTIONS_DIR"
  git -C "$MNC_ACTIONS_DIR" fetch -q --depth 1 origin "$MNC_ACTIONS_PIN"
  git -C "$MNC_ACTIONS_DIR" checkout -q "$MNC_ACTIONS_PIN"
fi
if [ ! -x "$MNCS_DIR/scripts/mncs_promotion_evaluate.py" ]; then
  rm -rf "$MNCS_DIR"
  git clone -q --filter=blob:none --no-checkout https://github.com/epi13/machine-native-complexity-standard "$MNCS_DIR"
  git -C "$MNCS_DIR" fetch -q --depth 1 origin "$MNCS_PIN"
  git -C "$MNCS_DIR" checkout -q "$MNCS_PIN" -- scripts/mncs_promotion_evaluate.py
fi
EVAL="python3 $MNCS_DIR/scripts/mncs_promotion_evaluate.py"

CANDIDATE_REPO="$(python3 -c "import json; print(json.load(open('promotion/candidate.json'))['repository'])")"
CANDIDATE_COMMIT="$(python3 -c "import json; print(json.load(open('promotion/candidate.json'))['commit'])")"
OBLIGATION="promotion/obligations/adopt-repository-owned-promotion.obligation.json"
VECTORS="$(mktemp -d)"

export MNC_ACTIONS_DIR
bash scripts/mncds-check.sh >/dev/null
bash scripts/mncds-obligations-check.sh >/dev/null

PASS=0
check_verdict() {  # name expected actual
  if [ "$2" = "$3" ]; then PASS=$((PASS+1)); echo "vector $1: PASS ($2)";
  else echo "vector $1: FAIL (expected $2, got $3)"; exit 1; fi
}
check_no_claim() {  # name rc
  if [ "$2" -ne 0 ]; then PASS=$((PASS+1)); echo "vector $1: PASS (no claim, exit $2)";
  else echo "vector $1: FAIL (expected no claim, got exit 0)"; exit 1; fi
}
BASE_ARGS="--boundary promotion/mncds-promotion.boundary.json --authority-map promotion/authority-map.json --checks .mncs/mncds-check.json .mncs/mncds-obligations-check.json --obligations $OBLIGATION --subject-repository $CANDIDATE_REPO --subject-commit $CANDIDATE_COMMIT"

# 1. pass universe: real evidence over the real boundary.
$EVAL $BASE_ARGS --output "$VECTORS/pass.json" >/dev/null
check_verdict "pass-universe" "PASS" "$(python3 -c "import json; print(json.load(open('$VECTORS/pass.json'))['verdict'])")"

# 2. open required obligation holds the boundary at UNKNOWN.
python3 - "$OBLIGATION" "$VECTORS/open.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1])); doc["status"] = "open"; del doc["resolution"]
json.dump(doc, open(sys.argv[2], "w"), indent=2)
PY
$EVAL --boundary promotion/mncds-promotion.boundary.json --authority-map promotion/authority-map.json \
  --checks .mncs/mncds-check.json .mncs/mncds-obligations-check.json --obligations "$VECTORS/open.json" \
  --subject-repository "$CANDIDATE_REPO" --subject-commit "$CANDIDATE_COMMIT" \
  --output "$VECTORS/open-out.json" >/dev/null
check_verdict "open-obligation" "UNKNOWN" "$(python3 -c "import json; print(json.load(open('$VECTORS/open-out.json'))['verdict'])")"

# 3. rejected required obligation stays a negative result.
python3 - "$OBLIGATION" "$VECTORS/rejected.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1])); doc["status"] = "rejected"; doc["resolution"]["resolution"] = "rejected"
json.dump(doc, open(sys.argv[2], "w"), indent=2)
PY
$EVAL --boundary promotion/mncds-promotion.boundary.json --authority-map promotion/authority-map.json \
  --checks .mncs/mncds-check.json .mncs/mncds-obligations-check.json --obligations "$VECTORS/rejected.json" \
  --subject-repository "$CANDIDATE_REPO" --subject-commit "$CANDIDATE_COMMIT" \
  --output "$VECTORS/rejected-out.json" >/dev/null
check_verdict "rejected-obligation" "FAIL" "$(python3 -c "import json; print(json.load(open('$VECTORS/rejected-out.json'))['verdict'])")"

# 4. malformed obligation establishes no claim (never UNKNOWN).
python3 - "$OBLIGATION" "$VECTORS/malformed.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1])); del doc["obligation_key"]
json.dump(doc, open(sys.argv[2], "w"), indent=2)
PY
$EVAL --boundary promotion/mncds-promotion.boundary.json --authority-map promotion/authority-map.json \
  --checks .mncs/mncds-check.json .mncs/mncds-obligations-check.json --obligations "$VECTORS/malformed.json" \
  --subject-repository "$CANDIDATE_REPO" --subject-commit "$CANDIDATE_COMMIT" \
  --output "$VECTORS/malformed-out.json" >/dev/null 2>&1
check_no_claim "malformed-obligation" "$?"

# 5. contradictory duplicate obligation keys establish no claim.
$EVAL --boundary promotion/mncds-promotion.boundary.json --authority-map promotion/authority-map.json \
  --checks .mncs/mncds-check.json .mncs/mncds-obligations-check.json --obligations "$OBLIGATION" "$OBLIGATION" \
  --subject-repository "$CANDIDATE_REPO" --subject-commit "$CANDIDATE_COMMIT" \
  --output "$VECTORS/dup-out.json" >/dev/null 2>&1
check_no_claim "duplicate-obligation" "$?"

# 6. wrong commit: evidence for another revision promotes nothing here.
$EVAL $BASE_ARGS --subject-commit dddddddddddddddddddddddddddddddddddddddd \
  --output "$VECTORS/wrong-commit.json" >/dev/null 2>&1
check_no_claim "wrong-commit" "$?"

# 7. moving ref instead of an immutable revision is rejected.
$EVAL --boundary promotion/mncds-promotion.boundary.json --authority-map promotion/authority-map.json \
  --checks .mncs/mncds-check.json .mncs/mncds-obligations-check.json --obligations "$OBLIGATION" \
  --subject-repository "$CANDIDATE_REPO" --subject-commit main \
  --output "$VECTORS/moving-ref.json" >/dev/null 2>&1
check_no_claim "moving-ref" "$?"

# 8. missing required evidence stays UNKNOWN (never PASS).
$EVAL --boundary promotion/mncds-promotion.boundary.json --authority-map promotion/authority-map.json \
  --checks .mncs/mncds-check.json --obligations "$OBLIGATION" \
  --subject-repository "$CANDIDATE_REPO" --subject-commit "$CANDIDATE_COMMIT" \
  --output "$VECTORS/missing.json" >/dev/null
check_verdict "missing-required" "UNKNOWN" "$(python3 -c "import json; print(json.load(open('$VECTORS/missing.json'))['verdict'])")"

# 9. tampered authority binding establishes no claim.
python3 - "$VECTORS/authmap.json" <<'PY'
import json, sys
doc = json.load(open("promotion/authority-map.json"))
doc["authorities"]["mncds-obligations"]["authority"] = "adversarial-authority"
json.dump(doc, open(sys.argv[1], "w"), indent=2)
PY
$EVAL --boundary promotion/mncds-promotion.boundary.json --authority-map "$VECTORS/authmap.json" \
  --checks .mncs/mncds-check.json .mncs/mncds-obligations-check.json --obligations "$OBLIGATION" \
  --subject-repository "$CANDIDATE_REPO" --subject-commit "$CANDIDATE_COMMIT" \
  --output "$VECTORS/tampered.json" >/dev/null 2>&1
check_no_claim "wrong-authority" "$?"

# 10. duplicate check ids for one requirement establish no claim.
cp .mncs/mncds-check.json "$VECTORS/mncds-check-dup.json"
$EVAL --boundary promotion/mncds-promotion.boundary.json --authority-map promotion/authority-map.json \
  --checks .mncs/mncds-check.json "$VECTORS/mncds-check-dup.json" .mncs/mncds-obligations-check.json \
  --obligations "$OBLIGATION" \
  --subject-repository "$CANDIDATE_REPO" --subject-commit "$CANDIDATE_COMMIT" \
  --output "$VECTORS/dup-check.json" >/dev/null 2>&1
check_no_claim "duplicate-checks" "$?"

# 11. stale revision: a superseded candidate no longer promotes.
STALE_OBLIGATION="$VECTORS/stale.json"
python3 - "$OBLIGATION" "$STALE_OBLIGATION" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1])); doc["subject"]["commit"] = "0" * 40
json.dump(doc, open(sys.argv[2], "w"), indent=2)
PY
$EVAL --boundary promotion/mncds-promotion.boundary.json --authority-map promotion/authority-map.json \
  --checks .mncs/mncds-check.json .mncs/mncds-obligations-check.json --obligations "$STALE_OBLIGATION" \
  --subject-repository "$CANDIDATE_REPO" --subject-commit "$CANDIDATE_COMMIT" \
  --output "$VECTORS/stale.json" >/dev/null 2>&1
check_no_claim "stale-revision" "$?"

# 12. forged digest: every bound digest must recompute from the exact
# consumed bytes (byte rebinding, the forgery detector where bytes are at
# hand). The control rebinds the genuine claim cleanly; the forged claim
# (one digest flipped) must mismatch.
python3 - "$VECTORS/pass.json" "$OBLIGATION" <<'PY'
import hashlib, json, sys

def digest(path):
    return "sha256:" + hashlib.sha256(open(path, "rb").read()).hexdigest()

consumed = {
    ("check-result", "mncds-development-record"): ".mncs/mncds-check.json",
    ("check-result", "mncds-obligations"): ".mncs/mncds-obligations-check.json",
    ("mncds-obligation-record", "pressure.mncds.promotion-integration.required"): sys.argv[2],
    ("promotion-boundary", "mncds-promotion"): "promotion/mncds-promotion.boundary.json",
    ("authority-map", ""): "promotion/authority-map.json",
}

def key(ref):
    kind = ref.get("kind")
    if kind == "check-result":
        return (kind, ref.get("check_id"))
    if kind == "mncds-obligation-record":
        return (kind, ref.get("obligation_key"))
    if kind == "promotion-boundary":
        return (kind, ref.get("boundary_id"))
    if kind == "authority-map":
        return (kind, "")
    return (kind, None)

def rebind(doc):
    problems = []
    for ref in doc.get("references", []):
        path = consumed.get(key(ref))
        if path is None:
            problems.append(f"unconsumed reference: {key(ref)}")
        elif ref.get("digest") != digest(path):
            problems.append(f"digest mismatch: {key(ref)}")
    return problems

genuine = json.load(open(sys.argv[1]))
control = rebind(genuine)
assert not control, f"control claim must rebind cleanly: {control}"

forged = json.loads(json.dumps(genuine))
forged["references"][0]["digest"] = "sha256:" + "f" * 64
problems = rebind(forged)
assert problems, "forged digest must mismatch the consumed bytes"
print("forged-digest detected:", problems[0])
PY
if [ "$?" -ne 0 ]; then echo "vector forged-digest: FAIL"; exit 1; fi
PASS=$((PASS+1)); echo "vector forged-digest: PASS"

rm -rf "$VECTORS"
echo "promotion vectors: $PASS/12 PASS"
