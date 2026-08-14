# MNCDS Extraction from the Historical MNCS Repository

This repository is being established before the normative MNCDS material is extracted from `epi13/machine-native-complexity-standard`.

The goal is **not** to fork MNCS. The goal is to make the existing conceptual separation between MNCS and MNCDS real at the repository, release, governance, validator, and conformance layers.

## Migration invariants

The transfer MUST preserve:

1. normative meaning unless a separate reviewed change says otherwise;
2. version and release-candidate identities;
3. schema identifiers and compatibility behavior;
4. valid/invalid conformance behavior;
5. record identities and historical evidence;
6. commit/file provenance sufficient to trace migrated material back to its source;
7. Apache-2.0 licensing and attribution; and
8. explicit `UNKNOWN` states and authority limitations.

A cleaner repository layout is not evidence that a semantic change is safe.

## Recommended migration sequence

### 1. Freeze a source point

At migration time, record the exact MNCS source commit used for extraction. The bootstrap inspection observed source commit `f0088c4d46dec84f289d9b4417eec32b0ac028e6`, but the transfer agent MUST refresh this and use the actual current source commit rather than assuming that observation remains current.

### 2. Build a complete inventory

Start with `migration/inventory.json`, then expand it from the frozen source tree. Every MNCDS-related artifact should receive one disposition:

- `MOVE` — normative or implementation material owned by MNCDS;
- `KEEP_IN_MNCS` — owned by MNCS;
- `SHARED_INTERFACE` — keep normative ownership in one project and consume through a versioned interface;
- `SPLIT` — a mixed file/module must be separated without changing behavior;
- `REVIEW_REQUIRED` — ownership or semantics are ambiguous.

### 3. Transfer normative source first

Move the MNCDS specification, records-and-decisions material, MNCDS-owned schemas, and clearly MNCDS-specific conformance vectors before restructuring implementation code.

Do not delete the historical source from MNCS until the new repository has equivalent content, CI, provenance notes, and cross-links.

### 4. Separate validator surfaces

The historical Python implementation is mixed under `src/mncs_validator`. Extract MNCDS validation behavior behind a dedicated package/CLI surface here. Preserve existing `mncds` command behavior and fixture outcomes before refactoring internals.

Shared low-level utilities such as canonical JSON, hashing, safe file handling, or generic result types may remain duplicated temporarily or become explicitly versioned libraries later. Avoid creating a hidden runtime dependency from the MNCDS validator to the MNCS repository checkout.

### 5. Split conformance and examples

Copy MNCDS-specific valid/invalid vectors and development-record examples here. For combined release-candidate corpora, split by normative owner while retaining cross-project integration cases in a clearly labeled interoperability area.

Cross-project fixtures should identify the exact MNCS and MNCDS versions they exercise.

### 6. Re-home RFCs and documentation

Move RFCs whose normative subject is MNCDS. For mixed MNCS/MNCDS RFCs, preserve the historical document and either:

- keep an archival copy with provenance plus successor RFCs in the owning repositories; or
- retain one canonical historical source and link to it from both projects.

Do not rewrite history so that an old combined RFC appears to have originated here.

### 7. Establish independent release machinery

MNCDS should end with its own:

- package metadata and `mncds` CLI;
- CI and conformance checks;
- release tags and changelog;
- specification/schema version table;
- RFC index;
- governance and security policy;
- release checklist; and
- compatibility matrix for supported MNCS bindings.

### 8. Clean the MNCS repository last

Only after MNCDS is independently testable should the MNCS repository remove transferred implementation/specification material. Replace removed material with concise pointers and compatibility documentation, not duplicated normative text.

## Acceptance criteria for the extraction

The migration is complete when:

- MNCDS 0.1-rc.1 can be located and validated entirely from this repository;
- all MNCDS-owned schemas and conformance vectors live here;
- the `mncds` validator/CLI no longer depends on private knowledge of the MNCS repository layout;
- equivalent pre/post-migration fixture outcomes are demonstrated;
- cross-project MNCS bindings remain explicit and versioned;
- historical provenance is documented;
- the MNCS repository can remove MNCDS-owned source without breaking MNCS-only validation; and
- neither repository contains an accidental second normative copy of the other's standard.

## Important non-goal

Do not use extraction as an opportunity to make MNCDS more tightly coupled to the rest of the MNCS tooling family. The purpose of this repository boundary is to let MNCDS evolve cleanly as an independent companion specification while keeping integration explicit.
