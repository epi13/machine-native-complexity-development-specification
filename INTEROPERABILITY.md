# MNCS ↔ MNCDS Interoperability

MNCS and MNCDS are sibling specifications with separate normative authority, versioning, governance, conformance, and release histories.

## Responsibility boundary

### MNCS owns

MNCS defines implementation-evidence semantics: the evidence and assurance structures used to support claims about an implementation.

### MNCDS owns

MNCDS defines development-process semantics: how implementations are generated, evaluated, selected, released, monitored, regenerated, replaced, and retired, including process authority, candidate lineage, partitions, reproducibility, selection, release, and lifecycle records.

## Binding rule

MNCDS MAY reference an MNCS result or artifact through an explicit versioned binding. Such a binding should identify, at minimum, the relevant:

- MNCS specification/profile version;
- subject/candidate identity;
- contract identity;
- environment identity or declared compatibility envelope;
- result identity or canonical artifact digest; and
- compatibility status.

MNCDS MUST NOT copy MNCS normative semantics into this repository merely to validate a binding. It may define what information an MNCDS record requires from MNCS and how mismatches affect MNCDS, while the meaning of the MNCS artifact remains controlled by MNCS.

MNCS likewise should not embed MNCDS development-process semantics merely to consume an MNCDS record.

## Compatibility outcomes

Cross-project compatibility should be explicit and conservative:

- an exact supported binding may be accepted according to the applicable MNCDS rule;
- an identity or required semantic mismatch is `FAIL` where the specification requires agreement;
- a missing, inaccessible, unsupported, or unrecognized binding is `UNKNOWN` unless a stronger normative rule requires failure;
- compatibility shims are non-normative unless standardized through the appropriate project governance.

## Version evolution

A release of either project MUST NOT silently change the meaning of a released version of the other.

When one project evolves:

1. publish the new version under its own governance;
2. identify interoperability effects;
3. update compatibility tables or adapters in the consuming project;
4. add cross-version conformance fixtures where useful; and
5. preserve prior released bindings and historical records.

No synchronized release cadence is required. MNCDS 0.x may support multiple MNCS versions, and MNCS may exist independently of MNCDS.

## Family producer references (RFC 0005, experimental)

MNCDS 0.2-alpha.1 records may cite any producer-native record through a
versioned `producer_bindings` entry (producer, record kind, native schema
version, stable identity, optional digest/artifact locator, declared scope,
compatibility status, evidence status). The field names deliberately mirror the
MNCS-Commons producer reference (`commons.mncs.dev/producer-reference/v0alpha1`)
so family bindings round-trip without translation.

Rules carried over unchanged:

- MNCDS validates binding form, role eligibility, subject/partition identity
  agreement, and tri-state propagation only.
- Producer-native meaning is never imported or reinterpreted; Commons storage
  or indexing of an MNCDS record transfers no semantic authority.
- A rerun under changed identities is a descendant binding with non-empty
  `declared_changes`.
- Validation remains offline; producers are never contacted by the normative
  validator.

The Commons `DevelopmentRecord` projection stores a validated record's exact
identity and digest and links it to experiment/evaluation/candidate references;
it is descriptive, not an additional authority layer.

## Shared code

Shared implementation code is permitted, but shared code does not create shared normative authority. If both validators need a canonicalization, identity, archive, or transport implementation, prefer a clearly versioned library or duplicated non-normative implementation over ambiguous ownership of specification text.

A future common interoperability repository or package may be introduced if genuinely shared protocol surface becomes large enough to justify it. Until then, keep the boundary explicit and small.

## Family-level documentation

The MNCS Atlas may explain how MNCS and MNCDS fit together for contributors and agents, but it is descriptive rather than normative. Normative meaning remains in the owning repository.
