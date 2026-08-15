# Implementation identity is data, not policy

This is development guidance for MNCDS consumers. It does not change MNCDS 0.1
record schemas.

## Principle

An implementation identity — a model tag, worker id, runtime name, or provider
namespace — may be recorded as data. It must not silently define capability or
architecture.

Brand or family substrings in an identity are not capability proof.

## Required distinctions

- **Capability claim**: a fact reported by a provider or runtime.
- **Observed capability**: a capability demonstrated by bounded execution and
  recorded as evidence.
- **Policy preference**: an operator or system ranking choice.
- **Exact pin**: an operator request for one implementation identity. Pins fail
  closed when the identity is absent unless an explicit fallback policy says
  otherwise.
- **Compatibility mechanism**: an unusual but bounded path used only when
  evidence is missing. It must remain visible, testable, and removable.

Unknown remains unknown. Missing evidence must not be converted into PASS.

## Unconventional mechanisms

A workaround is acceptable only when its boundary, assumptions, invariant,
validation, and evidence are explicit. Accidental shortcuts around validators
are not architecture.
