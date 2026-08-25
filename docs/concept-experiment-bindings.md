# Concept Experiment Bindings into MNCDS

Status: implemented as the experimental RFC 0005 binding surface (`MNCDS 0.2-alpha.1`); this document remains background rationale

## Purpose

Concept Reconstruction Experiments (CREs) can produce useful development evidence for MNCDS, but the experiment system should not become part of MNCDS normative meaning. This document proposes a narrow binding boundary between producer-neutral Concept Experiment identities and MNCDS development records.

## Boundary

MNCDS continues to own development-process semantics: candidate lineage, authority, evaluation partitions, feedback eligibility, selection, release, monitoring, regeneration, replacement and retirement.

A Concept Experiment is evidence about a bounded study. It does not by itself establish that a development process satisfies MNCDS.

## Binding shape

An MNCDS record that cites a Concept Experiment should identify, where applicable:

- exact Concept Experiment ID/digest;
- candidate/subject identity;
- language profile and compiler identity;
- frozen study/evaluator policy identity;
- relevant Forge evaluation result identities;
- relevant Fabric execution/environment identities;
- producer/actor provenance;
- evidence eligibility/partition status;
- unresolved `UNKNOWN`s and incompatibilities;
- whether the experiment was used as development feedback, selection evidence, reproduction evidence or only diagnostic evidence.

MNCDS should reference producer-native records rather than copy their semantics.

## Rerun lineage

CREs are especially useful when a failed frozen study is rerun after a language/compiler/tooling change. MNCDS should be able to preserve:

```text
candidate A
 -> experiment E1 FAIL/UNKNOWN
 -> permitted feedback/change
 -> candidate B
 -> rerun E1' under declared changed identities
 -> evaluation result
```

If language profile, evaluator, hidden material, budget or environment changes, the descendant record must make the difference explicit. A changed study is not silently the same experiment.

## Failure as development evidence

A failed or unresolved CRE may still be valuable development evidence. Candidate rejection, retained counterexamples, language expressivity gaps, verifier gaps and specification ambiguities can all inform development while remaining `FAIL` or `UNKNOWN` at their native boundaries.

MNCDS should not require every useful experiment to end in PASS before it can be cited as part of development history.

## Bootstrap before RAVEL/MNEL

The first CREs may use ordinary Harness/Fabric models under roles such as `experiment-investigator` and `adaptive-experiment-critic`. These are not RAVEL or MNEL records. MNCDS bindings should preserve the exact producer/model/worker identity and treat their recommendations as development inputs according to the applicable feedback/authority policy.

Future RAVEL/MNEL records can be added as new producer types without changing the fundamental experiment binding.

## Relationship to MNCS

MNCDS may later bind the selected/frozen candidate to an MNCS result using the existing explicit interoperability boundary. The conceptual projection is:

```text
raw compiler/execution/evaluator evidence
 -> Concept Experiment
 -> MNCDS development record
 -> MNCS assurance/conformance case
```

Each upper layer references exact lower-layer identities. MNCDS does not reinterpret MNCS assurance semantics, and MNCS does not absorb MNCDS development-process semantics.

## Implementation note

The smallest stable fields identified by real use are now specified in
[`rfcs/0005-versioned-producer-record-bindings.md`](../rfcs/0005-versioned-producer-record-bindings.md)
and exercised end-to-end by `examples/mncds-0.2-alpha/language-span-fix.development-record.json`
(a reconstructed mncs-language development episode) plus the MNCS-Commons
Family Record Spine exercise.
