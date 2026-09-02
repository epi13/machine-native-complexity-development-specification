# Development Pressure and Cross-Repository Change Sets

Status: experimental design extension for MNCDS 0.2/0.3.

MNCDS owns development records, authority, lineage, selection, release, monitoring, regeneration, and retirement. MNCS owns the meaning of evidence and its acceptance boundary. Commons exchanges records, Forge evaluates bounded candidates, and the language compiler supplies technical capability-gap artifacts.

## DevelopmentPressure

A `DevelopmentPressure` records a real implementation exposing a missing or unverifiable capability.

Required semantic fields:

- `pressure_id`: content-addressed identity;
- `producer`, `originating_project`, exact source revision, and contract revision;
- `requested_capability` and `current_limitation`;
- bounded `reproducer`;
- `affected_surfaces`: language, compiler, library, runtime, backend, tooling, or process;
- `protected_properties`;
- `evidence_requirements`;
- referenced `ResolutionProposal` identities;
- scoped `PASS`, `FAIL`, or `UNKNOWN) status;
- explicit `unresolved` fields.

A pressure is an observation, not authorization for a change.

## ResolutionProposal and ChangeSet

A `ResolutionProposal` identifies one candidate response, its semantic choice, implementation surfaces, compatibility impact, alternatives, and evaluation plan. Independent proposals retain separate identities.

A `ChangeSet` binds coordinated work crossing repositories. It records parent pressure/proposal identities, exact base revisions, participating repositories, intended changes, dependency and claim edges, compatibility snapshots, landing order, rollback/regeneration instructions, evidence, and the assembled final-tree identity. It does not replace repository pull requests.

A `PromotionDecision` names the selected candidate, authority level, policy, evaluator, evidence, scope, and unresolved unknowns.

## Lifecycle and authority

The lifecycle is:

`observed -> localized -> proposed -> evaluating -> selected|rejected -> adopted|retired`

Lifecycle state and evidence status are orthogonal. Authority levels are explicit:

1. local experiment;
2. candidate capability;
3. family-visible experimental capability;
4. verified standard;
5. core semantic guarantee.

No level implies universal correctness. Each transition is a new scoped claim.

## Distributed rules

Contributors may publish competing pressures and proposals concurrently. Coordination is required for promotion and cross-repository ChangeSets, not for local experiments. Convergent pressures may be linked but never silently merged.

Implementations must preserve PASS/FAIL/UNKNOWN, negative evidence, disagreements, unavailable evaluators, provenance, source revisions, tool versions, environments, and amendment history. A system-level PASS must never be inferred from component-level PASS records alone.

Compatibility reports use `COMPATIBLE`, `COMPATIBLE_WITH_UNRESOLVED_FIELDS`, `DRIFTED`, or `UNKNOWN`. Identity changes must be explicit. The first implementation may be documentation and fixtures; it must not claim that distributed promotion is solved until independent producers and evaluators exercise the protocol.
