# Contributing to MNCDS

MNCDS welcomes specification, schema, conformance, tooling, research, documentation, and governance contributions.

## Before contributing

Read:

- `README.md` for the repository boundary;
- `AGENTS.md` for authority and migration rules;
- `GOVERNANCE.md` for normative decision-making;
- `INTEROPERABILITY.md` before changing any MNCS binding;
- `MIGRATION.md` while the historical MNCDS material is still being transferred.

## Pull requests

A pull request should:

1. explain the problem and intended outcome;
2. identify whether the change is migration-only, editorial, implementation-only, experimental, or normative;
3. identify compatibility effects on existing MNCDS records and versions;
4. include tests and valid/invalid fixtures where machine behavior changes;
5. update specification and user documentation together when semantics change;
6. identify affected MNCS bindings without redefining MNCS locally;
7. preserve historical schemas, records, provenance, and released identities; and
8. pass repository CI.

Changes to normative meaning, schemas used as normative interoperability surfaces, result aggregation, authority rules, release/lifecycle semantics, governance, or MNCS interoperability require an RFC unless an already accepted RFC explicitly authorizes the change.

## Migration contributions

Migration is not permission to redesign the standard. A migration PR SHOULD keep exact transfer, editorial cleanup, and semantic change visibly separate.

When historical ownership is ambiguous, add the item to the migration inventory with an explicit disposition such as `MOVE`, `KEEP_IN_MNCS`, `SHARED_INTERFACE`, `SPLIT`, or `REVIEW_REQUIRED`. Do not duplicate normative source merely to avoid deciding the boundary.

## Development tooling

Tooling in this repository is non-normative unless the specification explicitly defines an artifact format or algorithm as normative. A reference validator is an implementation of the specification, not the specification itself.

Use reproducible local environments and keep generated artifacts out of version control unless they are intentional conformance fixtures or release artifacts.

## Licensing and sensitive material

By intentionally submitting a contribution, you agree that it is licensed under Apache-2.0 as described in `LICENSE`.

Do not submit secrets, private datasets, proprietary transcripts, protected evaluation material, or evidence you do not have permission to redistribute.
