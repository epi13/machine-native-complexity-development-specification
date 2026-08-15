# Machine-Native Complexity Development Specification

**MNCDS** is an open experimental specification for evidence-governed development of machine-native implementations.

MNCDS governs how machine-native implementations are created, evaluated, selected, released, monitored, regenerated, replaced, and retired. It is a companion to the [Machine-Native Complexity Standard (MNCS)](https://github.com/epi13/machine-native-complexity-standard), but it is **independently versioned, governed, and released**.

This repository is the canonical home of MNCDS 0.1-draft, MNCDS 0.1-rc.1, the development-record schemas, and the MNCDS-owned reference validator.

## What belongs here

- development-process semantics and profiles (D1–D4)
- development records, authority, lineage, partitions, selection, release, monitoring, regeneration, and retirement
- MNCDS schemas, conformance vectors, and the `mncds` validator
- RFCs that change MNCDS meaning

## What does not belong here

- MNCS implementation-evidence acceptance rules
- operator infrastructure such as MNCS Harness, MNCS Control MCP, MNCS Fabric, or MNCS Commons
- Forge workflows, RAVEL/MNEL research, or reference-study implementations

Those projects may *produce* MNCDS records. They do not own MNCDS meaning.

## Core boundary

**MNCS asks:** What evidence supports acceptance of an implementation?

**MNCDS asks:** What development process produced, evaluated, selected, released, monitored, regenerated, replaced, or retired that implementation?

Those responsibilities interact through explicit, versioned bindings. Neither project silently owns or rewrites the other's normative meaning.

A reader can understand MNCS without first understanding this repository. MNCDS may require an MNCS result only when a record declares an MNCS binding.

## Status

- Project: **Machine-Native Complexity Development Specification**
- Acronym: **MNCDS**
- Current specification line: **0.1**
- Current release candidate: **0.1-rc.1**
- Maturity: **experimental / pre-1.0**
- License: **Apache-2.0**
- Historical source: extracted from [`epi13/machine-native-complexity-standard`](https://github.com/epi13/machine-native-complexity-standard) commit `f0088c4d46dec84f289d9b4417eec32b0ac028e6`

See [`MIGRATION.md`](MIGRATION.md) and [`INTEROPERABILITY.md`](INTEROPERABILITY.md).

## Validate a record

```bash
python3 -m pip install -e '.[dev]'
mncds validate examples/mncds-0.1-rc/development-record.json --json
mncds validate examples/mncds-d4/development-record.json --require-pass
```

The validator checks the declared record and invariants. It does not launch generators, evaluators, models, Forge, Fabric, or Harness.

## Repository map

- `spec/` — normative MNCDS 0.1-draft and 0.1-rc.1 text
- `schemas/` — versioned machine-readable MNCDS schemas
- `examples/` — development-record examples
- `conformance/` — MNCDS-owned corpora
- `rfcs/` — proposals that change MNCDS meaning
- `docs/` — architecture, rationale, and non-normative guidance
- `src/mncds_validator/` — reference `mncds` CLI

## Family relationships

Family orientation lives in [MNCS Atlas](https://github.com/epi13/mncs-atlas). Atlas is descriptive.

| Project | Relationship to MNCDS |
|---|---|
| MNCS | sibling standard for implementation-evidence acceptance |
| MNCS Forge | may produce or evaluate development evidence; not an authority |
| MNCS Validator (in MNCS / Rust) | may consume MNCDS records as a shared interface |
| MNCS Harness, Control, Fabric, Commons | operator/implementation ecosystem; not required by MNCDS |
| RAVEL / MNEL / Reference Studies | research and empirical work that may emit MNCDS records |

## Non-claims

MNCDS is experimental. It is not accredited certification, a security warranty, organizational independence, protected custody, or proof that a development process is safe or correct.
