# Machine-Native Complexity Development Specification

**MNCDS** is an open experimental specification for evidence-governed development of machine-native implementations.

MNCDS governs how machine-native implementations are created, evaluated, selected, released, monitored, regenerated, replaced, and retired. It is a companion to the [Machine-Native Complexity Standard (MNCS)](https://github.com/epi13/machine-native-complexity-standard), but it is **independently versioned, governed, and released**.

> **Repository bootstrap in progress.** The normative MNCDS 0.1 release-candidate material currently lives in the MNCS repository and will be migrated here under an explicit provenance-preserving plan. Until that migration is completed and validated, this repository does not supersede the existing MNCDS source material.

## Core boundary

**MNCS asks:** What evidence supports acceptance of an implementation?

**MNCDS asks:** What development process produced, evaluated, selected, released, monitored, regenerated, replaced, or retired that implementation?

Those responsibilities interact through explicit, versioned bindings. Neither project silently owns or rewrites the other's normative meaning.

## Design principles

1. **Independent normative authority.** MNCDS changes are reviewed and released here.
2. **Explicit interoperability.** Dependencies on MNCS use versioned contracts and identities rather than source duplication.
3. **Process evidence is first-class.** Candidate lineage, partitions, authority, selection, reproducibility, release, and lifecycle state remain inspectable artifacts.
4. **Unknown stays unknown.** Missing, inaccessible, unsupported, crashed, or timed-out evidence does not become `PASS`.
5. **History is immutable.** Corrections create new records and preserve superseded identities.
6. **Tool neutrality.** Models, generators, analyzers, compilers, providers, benchmarks, languages, Forge, RAVEL, and case studies are implementations or research mechanisms, not normative authorities.
7. **No self-promotion.** Generators, evaluators, orchestration systems, and recursive agents cannot silently broaden authority or promote their own results.

## Repository map

- `spec/` — normative and release-candidate MNCDS specification text.
- `schemas/` — versioned machine-readable MNCDS schemas.
- `conformance/` — valid/invalid vectors and release-candidate conformance corpora.
- `rfcs/` — proposals that change normative meaning, governance, or interoperability.
- `docs/` — architecture, rationale, migration, and non-normative guidance.
- `migration/` — provenance and transfer planning for material currently housed in the MNCS repository.
- `scripts/` — repository and conformance support tooling; tools are non-normative unless a specification explicitly says otherwise.

## Status

- Project: **Machine-Native Complexity Development Specification**
- Acronym: **MNCDS**
- Current specification line: **0.1**
- Current source release candidate: **0.1-rc.1**, pending migration from the MNCS repository
- Maturity: **experimental / pre-1.0**
- License: **Apache-2.0**

The current migration source is [`epi13/machine-native-complexity-standard`](https://github.com/epi13/machine-native-complexity-standard). See [`MIGRATION.md`](MIGRATION.md) for the transfer boundary and [`INTEROPERABILITY.md`](INTEROPERABILITY.md) for the long-term MNCS ↔ MNCDS relationship.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md), [`GOVERNANCE.md`](GOVERNANCE.md), and [`AGENTS.md`](AGENTS.md) before changing normative material. Normative changes require explicit review and must not be smuggled in as migration cleanup.

## Non-claims

MNCDS is experimental. It is not accredited certification, a security warranty, organizational independence, protected custody, or proof that a development process is safe or correct. A validator can check declared records and invariants; it cannot manufacture missing real-world evidence or authority.
