# Changelog

All notable MNCDS specification and reference-tooling changes should be recorded here.

## Unreleased

### Family-integrated development-process protocol (RFC 0005)

- Added RFC 0005 proposing versioned producer-record bindings for development records.
- Alpha amendment (RFC 0005 §6.1): widened the 0.2-alpha-only `id` pattern to
  accept scheme-style producer-native identities (for example
  `mncs-forge://evaluation/<sha>`); discovered by the cross-family spine exercise.
- Added the experimental `MNCDS 0.2-alpha.1` record surface: the complete
  0.1-rc.1 aggregate plus `producer_bindings[]` with role, compatibility,
  evidence-status, subject/partition identity, and declared-rerun semantics.
- Validator: exact-version dispatch for `0.2-alpha.1`; RFC 0005 rules B1–B13
  implemented; tri-state propagation from producer evidence preserved
  (FAIL dominates, UNKNOWN never strengthened).
- Fixed a validator defect where release-candidate records with hard normative
  violations reported `valid: true`; `fail()` findings now invalidate the
  report, and report categories always surface the computed tri-state.
- Conformance: added an executable corpus runner and three corpora
  (0.1-draft 11 vectors, 0.1-rc.1 37 vectors, 0.2-alpha.1 19 vectors) covering
  authority violations, lineage violations, feedback leakage, UNKNOWN
  preservation, cross-family identity mismatch, malformed bindings, unsupported
  versions, and lifecycle inconsistencies.
- Added the first real-family development case study:
  `examples/mncds-0.2-alpha/language-span-fix.development-record.json`
  reconstructs the mncs-language module-import span repair
  (`67fc26f` FAIL → `cdee978` PASS) with pinned producer identities.
- Added `examples/mncds-0.2-alpha/d4-release-lifecycle.fixture.json`
  exercising D4 release/regeneration/replacement/rerun-binding coverage.
- CI now runs lint, type check, unit/schema/adversarial tests, all conformance
  corpora, packaged-example validation, and schema-bundle discovery.
- Documentation: version/support matrix, release checklist, roadmap
  reconciliation against implemented reality.

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
