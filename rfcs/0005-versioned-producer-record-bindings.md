# MNCDS RFC 0005: Versioned producer-record bindings for development records

- Status: Proposed (experimental)
- Target version: MNCDS 0.2-alpha.1 (new experimental surface; no change to released 0.1 semantics)
- Classification: Normative proposal for a new versioned record surface; additive only
- Related: RFC 0004, `spec/MNCDS-v0.1-rc.1.md`, `docs/concept-experiment-bindings.md`,
  `INTEROPERABILITY.md`, MNCS-Commons Family Record Spine
  (`commons.mncs.dev/producer-reference/v0alpha1`)

## 1. Problem statement

MNCDS 0.1 records bind an optional MNCS result through the fixed `mncs_binding`
object, and `docs/concept-experiment-bindings.md` non-normatively describes how
family-native evidence should be cited. The family has since grown
producer-native, identity-bearing records that real development episodes must be
able to reference without importing their semantics:

- Commons producer references (`commons.mncs.dev/producer-reference/v0alpha1`);
- Concept Experiment envelopes and Replication records;
- MNCS Language compilation study results (compiler, pipeline, target, backend,
  stage fingerprints, unresolved obligations);
- Forge bounded evaluations (verifier identity, obligation, tri-state status);
- Fabric execution references (job/request/node/environment/attempt identities);
- Harness actor provenance (role, model, provider, worker, route, policy);
- Control experiment manifests; and
- MNCS assurance cases where applicable.

0.1-rc.1 is a released candidate with a closed schema (`additionalProperties:
false` outside the free-form `extensions` object). Citing these records today is
either unrepresentable or forced into unvalidated `extensions`. The open-ended
`extensions` object cannot carry validation semantics such as identity agreement,
feedback eligibility, or compatibility outcomes.

## 2. Goals and non-goals

Goals:

1. Give an MNCDS development record a first-class, versioned way to reference
   external producer-native records by stable identity.
2. Keep every producer's normative semantics in its owning repository. MNCDS
   validates only what it owns: whether the reference is well-formed, which role
   the referenced evidence plays in the development process, whether that role is
   permitted, and how declared statuses propagate into the computed record status.
3. Preserve exact tri-state semantics: `FAIL > UNKNOWN > PASS`; missing,
   unsupported, or unresolved evidence never becomes PASS.
4. Remain independently usable offline: validating an MNCDS record MUST NOT
   require access to any producer system.

Non-goals:

- Redefining any producer's record formats.
- Hard-wiring MNCDS to today's producer list.
- Making MNCDS dependent on Commons, Forge, Fabric, Harness, Language, or Control.
- Changing released 0.1-draft or 0.1-rc.1 semantics.

## 3. Proposed surface: MNCDS 0.2-alpha.1

A new experimental version `0.2-alpha.1` of the development-record aggregate:

- contains all 0.1-rc.1 aggregate structure unchanged except where this RFC adds
  fields;
- adds one required top-level array, `producer_bindings`, which MAY be empty; and
- is dispatched by exact `mncds_version`, so existing validators reject it as
  `UNSUPPORTED` until updated, and 0.1 validators are unaffected.

This follows the repository's additive-evolution rule ("compatible additive
changes increment the standard minor version") and the established pattern that
unknown versions are `UNSUPPORTED` rather than reinterpreted.

### 3.1 Binding object

Each element of `producer_bindings` is one object with these required fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `binding_id` | id | Unique within the record. |
| `role` | enum | Development-process role of the bound evidence: `development_feedback`, `selection_evidence`, `final_evaluation_evidence`, `reproduction_evidence`, `diagnostic_evidence`. |
| `producer` | text | Producer identity, e.g. `mncs-language`, `mncs-forge`, `mncs-fabric`, `mncs-harness`, `mncs-control-mcp`, `mncs-commons`, `mnscd`-style names are forbidden; producers are named exactly as they name themselves. |
| `record_kind` | text | Producer-native record kind, e.g. `CompilationStudyResult`, `ConceptEvaluation`, `FamilyExecutionReference`, `ActorProvenance`, `ConceptExperiment`, `Replication`, `DevelopmentRecord`, `AssuranceCase`. |
| `native_schema_version` | text | Version of the producer-native schema of the referenced record. |
| `stable_record_id` | id-like text | Producer-native stable identity of the referenced record. |
| `compatibility_status` | enum | MNCDS-side compatibility declaration for this binding kind/version: `supported`, `unsupported_native_schema`, `unverified_producer`. |
| `evidence_status` | enum | The producer-declared tri-state outcome carried by the bound record: `PASS`, `FAIL`, `UNKNOWN`. MNCDS never reinterprets it. |

Optional fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `content_digest` | hash | `sha256:` digest of the referenced record content when known. |
| `artifact` | object | `{identity, kind, digest?, location?}` locator for large artifacts held in producer-owned stores. |
| `subject_candidate_id` | id | Candidate in this record's ledger that the bound evidence is about. |
| `partition_id` | id | Evaluation partition the evidence belongs to, when applicable. |
| `declared_scope` | object | Bounded, producer-defined scope echo (e.g. backend identity, attempt number, language profile). Not interpreted by MNCDS beyond identity equality checks the validator can perform. |
| `rerun_of_binding_id` | id | Another binding in this record that this binding reruns under declared changes. |
| `declared_changes` | texts | Non-empty when `rerun_of_binding_id` is present; what changed between the rerun pair (toolchain, evaluator, policy, budget, environment, corpus, profile, backend). |
| `notes` | text | Human-readable context. |

Field names deliberately mirror the Commons producer-reference shape
(producer / recordKind / schemaVersion / stableId / contentDigest / artifact /
scope) so family bindings round-trip without translation, while remaining
generic enough for non-family producers.

### 3.2 Validation semantics added by this RFC

All rules below apply at 0.2-alpha.1 only.

Well-formedness (invalid record):

- B1. `binding_id` values MUST be unique within the record.
- B2. `content_digest` and `artifact.digest`, when present, MUST be `sha256:` +
  64 lowercase hex characters.
- B3. `subject_candidate_id`, when present, MUST identify a candidate in the
  record's candidate ledger.
- B4. `partition_id`, when present, MUST identify a partition declared by the
  record.
- B5. `rerun_of_binding_id` MUST reference another binding in the same record,
  and `declared_changes` MUST be non-empty. A changed rerun is not silently the
  same experiment.

Role and eligibility (invalid record):

- B6. A binding with role `selection_evidence` or `final_evaluation_evidence`
  MUST declare `compatibility_status: supported`.
- B7. A binding with role `final_evaluation_evidence` MUST NOT declare
  `feedback_eligibility` permitting same-epoch repair feedback. This RFC encodes
  the existing rule that protected/final evaluation is never same-epoch repair
  feedback: such bindings are invalid when their declared scope marks them as
  used for generation of the same epoch (`declared_scope.feedback_use` present
  and equal to `"same_epoch_repair"`).
- B8. A binding whose declared scope carries a generator identity equal to the
  record's generator executable identity MUST NOT hold role
  `selection_evidence` or `final_evaluation_evidence` (no generator
  self-certification across the binding boundary).

Status propagation (affects computed status, not structural validity):

- B9. A selected candidate whose required selection or final-evaluation evidence
  includes a binding with `evidence_status: FAIL` fails the record (`FAIL`).
- B10. A binding with `evidence_status: UNKNOWN` in an evidentiary role
  (`selection_evidence`, `final_evaluation_evidence`) for the selected candidate
  contributes `UNKNOWN` to the computed status under the existing UNKNOWN
  policy; it never strengthens to PASS.
- B11. A binding with `compatibility_status: unsupported_native_schema` or
  `unverified_producer` used in an evidentiary role for the selected candidate
  contributes `UNKNOWN` (the claim is unverifiable), unless a stronger rule in
  this section requires failure.
- B12. A binding with `compatibility_status: supported` but no `content_digest`
  and no `artifact` locator used in an evidentiary role for the selected
  candidate contributes `UNKNOWN` (identity cannot be checked offline).

Cross-family agreement (invalid record):

- B13. When a binding declares `declared_scope.candidate_identity`, it MUST equal
  `subject_candidate_id` when both are present (identity mismatch is FAIL, per
  the existing MNCS-binding mismatch rule).

MNCS interop unchanged: `mncs_binding` keeps its 0.1 meaning at 0.2-alpha.1. An
assurance projection MAY be expressed as one additional producer binding with
producer `mncs`; this RFC does not define assurance semantics.

### 3.3 Independence from producers

Validation uses only record-local information. Producers are referenced by
identity; they are never contacted, imported, or executed. Live verification of
bound artifacts is an optional integration layer outside the normative
validator.

## 4. Compatibility and migration

- 0.1-draft and 0.1-rc.1 records remain valid and unchanged; their schemas are
  preserved byte-for-byte.
- Exact-version dispatch means 0.2-alpha.1 records are `UNSUPPORTED` on old
  validators rather than misinterpreted.
- No migration path from 0.1 to 0.2-alpha is defined in this RFC. A future RC
  may define one; missing historical facts would remain `UNKNOWN`.

## 5. Security and authority considerations

Bindings increase the amount of producer-declared data inside an MNCDS record.
All such data is untrusted input:

- declared scopes and notes are opaque text for identity comparison only;
- a binding can never promote itself: role permissions come from MNCDS-owned
  authority structure, not from the producer;
- tri-state collapse remains forbidden: bindings preserve producer `UNKNOWN`.

## 6. Alternatives considered

- Extend 0.1-rc.1 in place: rejected; mutates a released candidate schema.
- Use only the free-form `extensions` object: rejected; no validation semantics,
  no versioning, no dispatch.
- Per-producer hardwired binding objects: rejected; brittle against family
  evolution and violates tool neutrality.

## 7. Rollout plan

1. Land schema, validator support, conformance vectors, and examples behind
   `mncds_version: 0.2-alpha.1`.
2. Exercise the surface end-to-end against a real mncs-language development
   episode and the Commons Family Record Spine.
3. Promote to 0.2-rc or revise based on that evidence through a successor RFC.
