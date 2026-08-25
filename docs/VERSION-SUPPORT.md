# MNCDS version and support matrix

Status: normative-adjacent reference for dispatch behavior; the schemas and
specification text remain authoritative.

## Record versions

| Record version | Schema (`$id` path) | Dispatch | Status | Notes |
| --- | --- | --- | --- | --- |
| `0.1-draft` | `/schema/mncds/0.1/mncds-development-record.schema.json` | exact | historical draft, frozen | validated with draft semantics; never reinterpreted |
| `0.1-rc.1` | `/schema/mncds/0.1-rc.1/mncds-development-record.schema.json` | exact | release candidate; current stable interchange | |
| `0.2-alpha.1` | `/schema/mncds/0.2-alpha.1/mncds-development-record.schema.json` | exact | experimental alpha (RFC 0005) | may change or be withdrawn before any RC |
| anything else | — | `UNSUPPORTED` | — | unknown versions are never approximated |

## Supported MNCS bindings inside records

| Field | Permitted values | Rule |
| --- | --- | --- |
| `mncs_binding.mncs_version` (0.1 line) | `0.1`, `0.1.1`, `0.2`, `0.3-rc.1` | mismatch with charter/selection/candidate identities is FAIL per 0.1-rc.1 §11 |
| RFC 0005 producer bindings (0.2-alpha) | any producer; family producers observed today: `mncs-language`, `mncs-forge`, `mncs-fabric`, `mncs-harness`, `mncs-control-mcp`, `mncs-commons`, plus repository revision pins via `github.com/epi13/...` | MNCDS validates binding form, role eligibility, and identity agreement only; native semantics stay with the producer |

## Validator package

| Package | Version surface | Supports |
| --- | --- | --- |
| `mncds-validator` | tracks the current specification line | all record versions listed above, dispatched exactly by `mncds_version` |

## Compatibility rules

1. Adding a new exact record version never changes older versions' meaning.
2. Producer-binding compatibility statuses are declared per record
   (`supported`, `unsupported_native_schema`, `unverified_producer`);
   evidentiary roles require `supported`.
3. A rerun under changed compiler, backend, evaluator, policy, budget,
   environment, or corpus is a descendant binding with non-empty
   `declared_changes`; it is never silently the same experiment.
4. Missing, unsupported, or unresolved evidence contributes UNKNOWN, never
   PASS; identity disagreement fails where this specification requires
   agreement.
