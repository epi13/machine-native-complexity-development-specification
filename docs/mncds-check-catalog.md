# MNCDS check catalog

Status: normative for MNCDS 0.2-alpha.1.

This catalog assigns stable, machine-readable check identities to MNCDS-owned
development/process claims so that transport layers (notably `mncs-actions`
`mncs-family-verify`) can invoke MNCDS as a first-class authority without
reaching through the generic `additional-checks` seam, and without
redefining MNCDS semantics in transport code.

MNCDS owns development/change/promotion-process semantics. This catalog is
the authority for what each MNCDS check means; transport layers must cite
these identities and apply the result mapping below verbatim.

## Checks

### `mncds-development-record`

- Provider: `mncds`.
- Contract revision: the validated record's `mncds_version`
  (currently `0.2-alpha.1`; also `0.1-draft`, `0.1-rc.1`).
- Input: one MNCDS development record validated by `mncds validate`.
- Result mapping (applied to the owner-native validation report):
  - report `valid == true` and `computed_status == PASS` -> `PASS`;
  - report `valid == true` and `computed_status == FAIL` -> `FAIL`;
  - report `valid == true` and `computed_status == UNKNOWN` -> `UNKNOWN`;
  - report `valid == true` with an unrecognized status -> `UNKNOWN`
    (never `PASS`);
  - report `valid == false` (issues established) -> `FAIL`;
  - record unsupported (`supported == false`) -> `UNKNOWN`
    (the authority cannot evaluate this version; not a negative finding);
  - malformed record, unreadable input, or validator operational failure ->
    no claim is established (`INVALID` / `NOT_ESTABLISHED` at the transport
    boundary; never `UNKNOWN`, never `PASS`).
- `mncds validate --require-pass` exit code 3 (valid record, status not
  `PASS`) preserves the distinction between "valid but not passing" and
  "invalid": transport must map exit 3 to the report's computed status,
  not to a missing claim.

### `mncds-obligations`

- Provider: `mncds`.
- Contract revision: `mncds-obligation-record/0.2`
  (see `schemas/mncds-obligation-record-0.2.schema.json`;
  `0.1` remains loadable but is superseded).
- Input: a set of MNCDS obligation records projected from development
  pressure and ChangeSet evidence (see `docs/obligation-projection.md`).
- Resolution authority rules (a resolution is authoritative only when):
  - `status` is `resolved` with `resolution.fixed`, or `rejected` with
    `resolution.rejected` (kinds cohere; `tolerated` is boundary policy,
    never a self-granted resolution);
  - `resolution.evidence_refs` is non-empty;
  - `resolution.resolved_by` names the resolver and `resolved_at` the time;
  - no `resolution` block accompanies `open`;
  - keys are unique within the evaluation set and scoped to one subject.
- Result mapping:
  - every obligation `resolved`, or no obligations are `required` ->
    `PASS` (development evidence is complete enough for evaluation);
  - at least one `required` obligation remains `open` -> `UNKNOWN`
    (valid but incomplete; the boundary cannot decide);
  - a `required` obligation carries a negative resolution
    (`rejected` with authoritative evidence) -> `FAIL`;
  - malformed, contradictory (duplicate `obligation_key`), incoherent
    resolution, anonymous resolution, or revision-unbound obligation
    input -> no claim is established (`INVALID` / `NOT_ESTABLISHED`;
    never `UNKNOWN`).
- Optional (`required == false`) obligations that remain `open` stay
  visible in `unresolved` but never decide the check on their own.

## Authority roles

For both checks, the semantic authority is
`machine-native-complexity-development-specification`; the evidence
provider is `mncds`; remediation is owned by the repository that produced
the development record under evaluation. Transport layers carry these
roles; they do not reinterpret them.

## Versioning

Check identities are stable across MNCDS record versions. When a new
record version changes the meaning of a check, this catalog gains a new
contract revision and the old mapping is preserved, not edited.
