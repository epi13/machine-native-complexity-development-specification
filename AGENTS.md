# MNCDS repository agent guidance

## Repository authority

This repository is the development home and normative authority for the Machine-Native Complexity Development Specification (MNCDS). The sibling `machine-native-complexity-standard` repository is the authority for MNCS implementation-evidence semantics.

Agents MUST keep those authorities separate. A change to MNCDS MUST NOT silently redefine MNCS, and an MNCS implementation detail MUST NOT become normative MNCDS behavior merely because it is convenient to reuse.

## Migration discipline

During migration from the historical combined MNCS repository:

- preserve source provenance, version identities, release-candidate labels, and historical attribution;
- distinguish exact transfer from editorial cleanup and from normative change;
- do not rewrite historical records merely to fit the new repository layout;
- move MNCDS-owned schemas, conformance fixtures, validator surfaces, RFC material, and documentation here when ownership is clear;
- leave MNCS-owned implementation-evidence semantics in the MNCS repository;
- convert genuinely shared semantics into explicit, versioned interoperability boundaries rather than duplicated normative text;
- flag ambiguous ownership in the migration manifest instead of guessing;
- never describe a migrated artifact as independently reviewed merely because it crossed repositories.

Migration-only pull requests SHOULD avoid changing normative meaning. If a semantic change is necessary, separate it into an RFC or clearly identified follow-up.

## Evidence and status rules

- Preserve `PASS`, `FAIL`, and `UNKNOWN`; `FAIL` dominates `UNKNOWN`, which dominates `PASS` when aggregation rules require an ordering.
- Missing, inaccessible, unsupported, crashed, or timed-out evidence does not become `PASS`.
- Keep candidate generation, evaluation, selection, release, governance, and independent-review authorities explicit.
- Do not let a generator, evaluator, Forge workflow, RAVEL loop, model, or agent promote its own output by implication.
- Do not use final/protected evaluation as repair feedback for the same candidate epoch.
- Local execution cannot create organizational independence, protected custody, or an independent witness.

## Tool neutrality

Models, generators, analyzers, compilers, providers, benchmarks, programming languages, MNCS Forge, RAVEL, Fabric, and case studies may implement or exercise MNCDS, but they are not normative authorities.

Forge may be used as an optional development/evidence-control interface when configured, but Forge results remain development evidence within their declared authority. Source inspection is review, not a substitute for unavailable independent evidence.

## Change discipline

Before changing normative text or schemas:

1. identify the affected MNCDS version and artifact identity;
2. identify compatibility impact on existing development records;
3. identify any affected MNCS binding explicitly;
4. add or update valid/invalid conformance vectors;
5. preserve prior released schemas and historical records;
6. use an RFC for changes to normative meaning, governance, result aggregation, authority, release semantics, or interoperability contracts.

A cleaner implementation is not by itself permission to change the standard.
