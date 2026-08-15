# Changelog

All notable MNCDS specification and reference-tooling changes should be recorded here.

## Unreleased

### Repository extraction

- Established `machine-native-complexity-development-specification` as the independent development home for MNCDS.
- Defined separate MNCDS normative authority and governance from MNCS.
- Added explicit MNCS ↔ MNCDS interoperability rules.
- Added a provenance-preserving extraction plan and machine-readable migration inventory.
- Added specification, schema, conformance, RFC, documentation, and CI scaffolding.

- Migrated MNCDS 0.1-draft, 0.1-rc.1, records-and-decisions, schemas, examples,
  RFC 0004, and a standalone `mncds` validator from MNCS commit
  `f0088c4d46dec84f289d9b4417eec32b0ac028e6`.
- This repository is now the canonical home of MNCDS meaning. MNCS retains a
  consumer and consumed schema copies only.

No normative MNCDS meaning is changed by the extraction itself.
