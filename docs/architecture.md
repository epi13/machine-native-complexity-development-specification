# MNCDS Repository Architecture

This repository separates four concerns that were historically co-located with MNCS.

## 1. Normative layer

`spec/` and normative schemas define MNCDS meaning. They own development-process concepts such as charter binding, baseline/environment lock, authority separation, partitions, candidate lineage, reproducibility, selection, release, lifecycle, and MNCS binding requirements.

Normative meaning changes only through the MNCDS governance process.

## 2. Conformance layer

`conformance/` contains machine-checkable valid/invalid vectors and release-candidate corpora. Conformance artifacts demonstrate whether an implementation agrees with a declared MNCDS version; they do not override specification meaning.

Cross-project conformance should live under an explicit interoperability namespace and identify both MNCDS and MNCS versions.

## 3. Implementation layer

Reference validators, CLIs, helper libraries, scripts, Forge providers, and other tooling implement or exercise MNCDS. They are replaceable and non-normative unless a normative specification explicitly fixes an algorithm or wire representation.

The target architecture should allow the `mncds` validator to operate from this repository without requiring an MNCS repository checkout. Dependencies on MNCS artifacts should be versioned inputs, packages, or fixtures rather than source-tree assumptions.

## 4. Research and integration layer

Case studies, recursive agents, RAVEL, Fabric, MNCS Forge, language implementations, and experimental evaluators may produce MNCDS records or evidence. Their behavior is bounded by declared authority and cannot promote itself into normative meaning.

## Dependency direction

```text
MNCDS specification
       |
       +--> MNCDS schemas / conformance contracts
       |          |
       |          +--> reference validators and tools
       |
       +--> versioned MNCS interoperability requirement
                  |
                  +--> externally supplied MNCS artifacts/results
```

The important rule is that implementation code depends on specifications and interfaces; specifications do not depend on a particular agent, model, validator, Forge workflow, or orchestration system.

## Release independence

MNCDS releases independently of MNCS. A release records the MNCS versions/interfaces it supports, but no synchronized version numbering or release date is required.

This permits either project to evolve while compatibility remains explicit and testable.
