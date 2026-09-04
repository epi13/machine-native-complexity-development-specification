# MNCDS repository-owned promotion

Status: implemented (promotion boundary `mncds-promotion`).

MNCDS is the first MNCS-family repository after `mncs-actions` to consume
the reusable `mncs-actions` promotion machinery from a repository-owned
boundary. This document describes the implementation, not an aspiration.

## What promotion decides here

Promotion evaluates the **recorded candidate revision**
(`promotion/candidate.json`), not HEAD. The candidate names an exact
immutable commit plus the development record and obligation set that
describe it. Advancing the candidate is a reviewed change that rebinds
the obligation set: every obligation record carries the candidate as its
exact subject, and anything bound to another subject establishes no claim.

## Required evidence (all MNCDS authority)

The boundary (`promotion/mncds-promotion.boundary.json`) requires exactly:

- `mncds-development-record` (contract `0.2-alpha.1`): the candidate's
  development record, validated by the owner-native `mncds validate` CLI
  per `docs/mncds-check-catalog.md`. The promotion evidence is the
  repository's own record
  (`promotion/mncds-promotion-integration.development-record.json`),
  which describes this integration tranche with real test runs and real
  commit bindings -- not a fixture.
- `mncds-obligations` (contract `mncds-obligation-record/0.2`): the
  candidate's obligation set, evaluated by the owner-native
  `mncds evaluate-obligations` command (`src/mncds_validator/obligations.py`).
  A required open obligation holds the boundary at UNKNOWN; an
  authoritative required rejection holds it at FAIL; malformed or
  contradictory input establishes no claim (exit 2, never UNKNOWN).

No check outside the MNCDS authority is required here by design. The
authority map (`promotion/authority-map.json`) is repository-owned and
covers exactly these two checks.

## Who owns what

- MNCDS owns development/obligation semantics: the check catalog, the
  record and obligation schemas, the validator, and the evaluator.
- `mncs-actions` transports: the reusable `mncs-family-verify` workflow
  (pinned, never `@main`), the check-result envelope adapters, claim
  shape validation, aggregation, and gating. It redefines nothing.
- MNCS owns promotion-boundary semantics: the pinned evaluator
  (`scripts/mncs_promotion_evaluate.py` at the reviewed MNCS revision)
  decides PASS/FAIL/UNKNOWN over the transported claims.
- Commons relates: the resulting promotion claim, candidate revision,
  boundary, evidence, obligations, producer revisions, and digests are
  recorded through the Commons ChangeSet path (see MNCS-Commons
  `docs/changeset-promotion.md`). Commons never decides promotion.

## Compatibility observation vs promotion

A compatibility canary observes what the family currently produces and
reports UNKNOWN while blockers stand; it must never imply promotability.
The `promotion` workflow here is an actual gate (`fail-on-unknown: true`):
green means the candidate revision genuinely satisfied the boundary.
The `vectors` job proves the gate bites: 12 adversarial vectors over the
real boundary and real evidence (open/rejected/malformed/duplicate
obligations, wrong commit, moving ref, missing evidence, tampered
authority, duplicate checks, stale revision, forged digest).

## The loop, end to end

```text
development pressure
  -> MNCDS obligation record (open, candidate-bound)
  -> development work with evidence
  -> obligation resolved (or still open / rejected)
  -> owner-native evaluation (mncds CLI)
  -> mncs-actions transport (pinned adapters, subject stamps, digests)
  -> MNCS promotion evaluator (pinned revision, repository-owned boundary)
  -> promotion claim (PASS expensive: right claims, right owners,
     right exact revision, right contracts, digests rebound to bytes)
  -> Commons ChangeSet relation (record, not decide)
```

## Pins (immutable reviewed revisions)

- Reusable workflow + transport: `4b13265...` (mncs-actions main,
  post PR #19 duplicate-binding hardening).
- Promotion evaluator: `6884457...` (MNCS main, post PR #74
  self-reference hardening).

Advance only after the upstream merge lands, in a follow-up change, then
re-run CI against the merged revision. The scripts default to these pins
and accept `MNC_ACTIONS_DIR` / `MNCS_DIR` overrides for local runs.
