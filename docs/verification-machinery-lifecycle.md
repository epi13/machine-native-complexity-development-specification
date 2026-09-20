# Verification machinery lifecycle

Status: experimental interoperability contract
`mncds.verification-machinery-lifecycle/0.1`

MNCDS owns the development lifecycle of temporary verification machinery. The
record is deliberately separate from the Standard's repository-owned
verification-obligation inventory: Standard describes what must be proven;
MNCDS records whether a parity harness, pressure reproducer, differential
oracle, or compatibility fallback is still part of ordinary development.

The minimum state transition is:

```text
active -> cutover_pending -> canonical -> reference_only | scheduled | retired
```

At a native cutover, the record must name the criteria and evidence that made
the native path canonical. Once those criteria are satisfied, parity machinery
must make an explicit choice:

- `reference_only` when the comparison remains useful but is not needed for
  ordinary proof;
- `scheduled` when exhaustive comparison remains a deliberate periodic or
  release obligation; or
- `retired` when it is redundant and its provenance is preserved elsewhere.

A pressure reproducer follows a different path. The owning capability first
gets a permanent regression or conformance obligation. Only after that proof
exists may the consumer workaround be removed and the consumer reproducer be
retired or retained as historical reference. A reproducer is not silently
promoted to a permanent suite merely because it is easy to run.

The `ordinary_verification` flag is the machine-readable stop signal for
planners. It must be `false` for `reference_only`, `scheduled`, and `retired`
machinery. A record does not grant PASS, close a development obligation, or
authorize a repository change; it preserves the lifecycle and its evidence
boundary so agents do not reconstruct it from history.
