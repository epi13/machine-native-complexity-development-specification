# Obligation projection: pressure evidence into the MNCDS obligation lifecycle

Status: normative for MNCDS 0.2-alpha.1.

Development pressure discovered during family execution must enter the same
lifecycle as every other development obligation rather than living beside
it:

```text
pressure discovered
      |
      v
MNCDS obligation created (`open`)
      |
      v
ChangeSet / development work
      |
      v
evidence produced
      |
      v
obligation `resolved` or still `open`
      |
      v
MNCS promotion boundary evaluates it
```

This document defines the mechanical projection. Transport layers
(`mncs-actions` `development_pressure.py` and successors) implement this
mapping verbatim; they do not invent the semantic relationship.

## Projection rules

Each pressure item projects to exactly one obligation record
(`schemas/mncds-obligation-record-0.1.schema.json`):

| Pressure field              | Obligation field              | Rule                                              |
| --------------------------- | ----------------------------- | ------------------------------------------------- |
| `obligation_key`            | `obligation_key`              | carried verbatim; duplicates are contradictory    |
| pressure category           | `origin.kind`                 | `development-pressure`                            |
| pressure producer/authority | `origin.authority`            | carried verbatim                                  |
| `pressure_id`               | `origin.pressure_id`          | carried verbatim when present                     |
| candidate under evaluation  | `subject.repository/commit`   | exact 40-hex SHA; unbound pressure stays `open`   |
| lifecycle `NEW`/`REPRODUCED`| `status`                      | `open`                                            |
| lifecycle `RESOLVED` + refs | `status` + `resolution`       | `resolved`, `resolution.fixed`, refs required     |
| authoritative negative      | `status` + `resolution`       | `rejected`, `resolution.rejected`, refs required  |
| `not_reproduced`            | no obligation                 | observation only, never an obligation             |
| severity / blocking flag    | `required`                    | blocking pressure -> `true`; advisory -> `false`  |

## Rules transport must not break

1. Projection never closes an obligation. Only evidence produced by
   development work, referenced in `resolution.evidence_refs`, resolves one.
2. Projection never marks `required`. The `required` flag comes from the
   pressure's own blocking declaration or the owning repository's policy,
   never from transport heuristics.
3. `not_reproduced` pressure (could not be reproduced) projects to nothing.
   Absence of reproduction is not evidence of resolution.
4. An `evaluation-gap` origin (`origin.kind == "evaluation-gap"`) is how
   transport records missing authority semantics: the obligation stays
   `open` and `required`, the check stays `UNKNOWN`, and the missing
   authority is named in `evidence`. Transport must not substitute its own
   opinion for the missing semantics.
5. Convergent pressures (same underlying gap, distinct `pressure_id`s) link
   through `supersedes`; they are never silently merged into one key.

## Evaluation

The `mncds-obligations` check (`docs/mncds-check-catalog.md`) evaluates a
set of these records: all `resolved` (or none `required`) -> `PASS`; a
`required` `open` -> `UNKNOWN`; a `rejected` with authoritative evidence ->
`FAIL`; malformed/duplicated/unbound input -> no claim.
