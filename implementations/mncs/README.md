# Machine-native MNCDS decision core

Status: non-normative reference implementation (machine-native)

This directory hosts `development.mncs`, an MNCS Language encoding of the
MNCDS development-decision semantics specified normatively by RFC 0005 and
`spec/MNCDS-v0.1-rc.1.md` section 10:

| Function | Encodes |
| --- | --- |
| `is_evidentiary` | RFC 0005 B6/B9/B10 role gating (selection + final evaluation only) |
| `contribution` | tri-state propagation: evidentiary bindings carry producer status; all other roles are dominance-neutral |
| `same_epoch_feedback_eligible` | RFC 0005 B7: final-partition evidence is never same-epoch repair feedback |
| `selection_outcome` | 0.1-rc.1 §10 selection discipline: FAIL dominates; UNKNOWN fails closed under reject; survives only under explicit accept-with-UNKNOWN review |

Dominance discipline is inherited from `mncs.core.status`: no operation can
turn UNKNOWN into PASS or delete FAIL.

## Provenance pins

| Item | Identity |
| --- | --- |
| Module | `mncs.family.development.v01` (`implementations/mncs/development.mncs`) |
| Language profile | Source Profile 0.6 (`mncs 0.6;`) with module imports |
| Toolchain source | `epi13/mncs-language@29f41e8fae331c954ac9c3fc81ff49abad79aa97` |
| Compiler identity | `mncs:compiler:compiler:f862227638ca7fbc716123d8378cddfef4f76a9ef10ab0e99cc791e65207e45d` |
| Vendored dependency | `mncs/core/status.mncs`, byte-exact copy of `library/core/status.mncs` at the pinned commit, sha256 `fdde0134033a002b5ef13dd4150b8ce7ac1d406cd723773436647170984a4538` |
| Corpus | `development-corpus.json` — 33 cases covering every decisive cell |

## Reproduce

```bash
# from a checkout of mncs-language at the pinned commit
cargo run -p mncs-cli -- source-study <this-dir>/development.mncs
cargo run -p mncs-cli -- experiment run <this-dir>/development.mncs \
    --backend mncs-portable-wasm-mvp \
    --corpus <this-dir>/development-corpus.json
cargo run -p mncs-cli -- experiment run <this.mncs> \
    --backend mncs-c11 --corpus <this-dir>/development-corpus.json
```

Regenerate the corpus deterministically:

```bash
python3 implementations/mncs/gen_development_corpus.py \
    > implementations/mncs/development-corpus.json
```

## Recorded results (2026-08-25, pinned toolchain)

- `mncs-portable-wasm-mvp`: **PASS**, 33/33 cases
  (`evidence/backend-portable-wasm-result.json`,
  result identity
  `mncs:language:experiment:result:89c23f8db47046947722894fcfff2af777cb4a477031b053549bdfb4e6b64019`).
- `mncs-c11`: all 33 execution cases agreed with expected outcomes; the
  realization itself reports `completed_with_unresolved_obligations` because
  C11 declares itself "a portability/bootstrap realization, not native MNCS"
  ("C struct layout is not a language-owned record representation"). Per
  tri-state discipline this is recorded as-is, not upgraded to PASS.
- Compilation: zero diagnostics (`evidence/source-study.json`).

## Boundary

The Python reference validator remains the conformance authority for MNCDS
records. This module is an executable cross-check of decision logic, useful as
the family moves toward machine-native implementations of its own governance.
It is not required to validate any record and makes no claim about backends
beyond the recorded runs.
