# Machine-Native Complexity Development Specification 0.2-alpha.1

Status: **experimental alpha** implementing RFC 0005. It is not Accepted, Final,
or a release candidate. It exists to exercise versioned producer-record bindings
against real family development before any RC is proposed.

Normative terms use RFC 2119/8174 meanings from [`normative-language.md`](normative-language.md).

## 1. Relationship to MNCDS 0.1-rc.1

A 0.2-alpha.1 record contains the complete 0.1-rc.1 aggregate structure with the
same meaning, plus one required top-level array:

```text
producer_bindings: []
```

All 0.1-rc.1 normative text applies except as modified by RFC 0005 and this
document. The schema identity is
`https://mncs.dev/schema/mncds/0.2-alpha.1/mncds-development-record.schema.json`.
Exact-version dispatch applies: validators that do not know `0.2-alpha.1` MUST
report `UNSUPPORTED`, never approximate.

## 2. Producer bindings

Each element of `producer_bindings` references one external producer-native
record by stable identity without importing its semantics. Required fields:
`binding_id`, `role`, `producer`, `record_kind`, `native_schema_version`,
`stable_record_id`, `compatibility_status`, `evidence_status`. Optional fields:
`content_digest`, `artifact`, `subject_candidate_id`, `partition_id`,
`declared_scope`, `rerun_of_binding_id`, `declared_changes`, `notes`.

Roles are MNCDS-owned development-process roles:

- `development_feedback`: evidence eligible to influence generation for its
  subject candidate's epoch;
- `selection_evidence`: evidence relied on by the selection decision;
- `final_evaluation_evidence`: evidence from the final-evaluation partition;
- `reproduction_evidence`: evidence from an independent reproduction or rerun;
- `diagnostic_evidence`: evidence retained for diagnosis only; it cannot support
  selection or release claims.

`evidence_status` is the producer-declared tri-state outcome. MNCDS preserves it
exactly; `FAIL > UNKNOWN > PASS`. A producer UNKNOWN MUST NOT become a record
PASS through any aggregation.

## 3. Binding rules

Structural rules B1–B5 of RFC 0005 are invalid-record conditions (identity
agreement, digest form, ledger membership, partition membership, declared rerun
changes). Role rules B6–B8 are invalid-record conditions: evidentiary bindings
must be supported, final evaluation is never same-epoch repair feedback, and a
binding whose scope declares generator provenance cannot serve as selection or
final evidence for that same generator's output.

Status rules B9–B12 propagate declared evidence into the computed status:
required FAIL fails; UNKNOWN and unsupported or unresolvable identities keep the
record at least UNKNOWN under the existing UNKNOWN policy.

Cross-family agreement rule B13 makes identity mismatch between a binding and
its subject candidate a FAIL where both identities are declared.

## 4. Independence

Validation remains offline and executes nothing. Producers referenced by
bindings are not contacted. Live verification is a non-normative integration
layer. No producer system becomes an MNCDS authority, and MNCDS claims no
authority over any producer's records.

## 5. Status of this version

0.2-alpha.1 is exercised by:

- `examples/mncds-0.2-alpha/` including a reconstructed real mncs-language
  development episode;
- `conformance/mncds-conformance-corpus/corpus-0.2-alpha.json`; and
- the MNCS-Commons Family Record Spine exercise, which stores a Commons
  `DevelopmentRecord` projection of a validated 0.2-alpha.1 aggregate.

Experience from these exercises will drive either revision of this alpha or a
0.2-rc proposal.
