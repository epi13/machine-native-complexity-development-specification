"""One-off generator for the 0.2-alpha D4 release/lifecycle fixture.

Derives examples/mncds-0.2-alpha/d4-release-lifecycle.fixture.json from the
released 0.1-rc example so profile semantics stay consistent, then layers
producer bindings that exercise RFC 0005 rules end-to-end. The result is a
synthetic-but-realistic fixture: it is clearly labeled as a fixture and makes
no claim about a real historical episode.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "examples/mncds-0.1-rc/development-record.json"
OUT = ROOT / "examples/mncds-0.2-alpha/d4-release-lifecycle.fixture.json"

record = json.loads(SRC.read_text())
record["schema_version"] = "0.2-alpha.1"
record["mncds_version"] = "0.2-alpha.1"
record["record_id"] = "fixture.alpha-release-lifecycle-v1"
record["charter"]["charter_id"] = "fixture.charter.alpha-release-v1"
record["created_at"] = "2026-08-25T00:00:00Z"

FORGE_EVAL_DIGEST = "sha256:" + "a1" * 32
LANG_STUDY_DIGEST = "sha256:" + "b2" * 32
FABRIC_EXEC_IDENTITY = "mncs-fabric://execution/fixture-job-attempt-2"
HARNESS_ACTOR_ID = (
    "mncs-harness://actor-provenance/" + "c3" * 16
)

record["producer_bindings"] = [
    {
        "binding_id": "binding.fix.lang-study",
        "role": "selection_evidence",
        "producer": "mncs-language",
        "record_kind": "CompilationStudyResult",
        "native_schema_version": "mncs-language.family-compiler-reference.v0.1",
        "stable_record_id": "mncs:compiler:compilation-study-result:fixturealpha001",
        "content_digest": LANG_STUDY_DIGEST,
        "subject_candidate_id": "candidate.epoch-two",
        "partition_id": "partition.selection",
        "declared_scope": {
            "candidate_identity": "candidate.epoch-two",
            "backend": "portable-wasm-mvp",
        },
        "compatibility_status": "supported",
        "evidence_status": "PASS",
    },
    {
        "binding_id": "binding.fix.forge-final",
        "role": "final_evaluation_evidence",
        "producer": "mncs-forge",
        "record_kind": "ConceptEvaluation",
        "native_schema_version": "commons.mncs.dev/concept-evaluation/v0alpha1",
        "stable_record_id": "mncs-forge://evaluation/fixturealpha002",
        "content_digest": FORGE_EVAL_DIGEST,
        "subject_candidate_id": "candidate.epoch-two",
        "partition_id": "partition.final",
        "declared_scope": {
            "concept_experiment_id": "cre-fixture-alpha",
            "verifier_identity": "forge:independent-verifier",
        },
        "compatibility_status": "supported",
        "evidence_status": "PASS",
    },
    {
        "binding_id": "binding.fix.fabric-execution",
        "role": "reproduction_evidence",
        "producer": "mncs-fabric",
        "record_kind": "FamilyExecutionReference",
        "native_schema_version": "mncs-fabric/family-execution-reference/v0alpha1",
        "stable_record_id": FABRIC_EXEC_IDENTITY,
        "rerun_of_binding_id": "binding.fix.fabric-execution-attempt-1",
        "declared_changes": [
            "execution attempt changed from 1 to 2 after worker replacement",
            "declared environment runtime image refreshed",
        ],
        "subject_candidate_id": "candidate.epoch-two",
        "artifact": {
            "identity": FABRIC_EXEC_IDENTITY,
            "kind": "execution-reference",
        },
        "compatibility_status": "supported",
        "evidence_status": "UNKNOWN",
    },
    {
        "binding_id": "binding.fix.fabric-execution-attempt-1",
        "role": "development_feedback",
        "producer": "mncs-fabric",
        "record_kind": "FamilyExecutionReference",
        "native_schema_version": "mncs-fabric/family-execution-reference/v0alpha1",
        "stable_record_id": "mncs-fabric://execution/fixture-job-attempt-1",
        "subject_candidate_id": "candidate.epoch-one",
        "partition_id": "partition.development",
        "compatibility_status": "supported",
        "evidence_status": "FAIL",
    },
    {
        "binding_id": "binding.fix.harness-actor",
        "role": "diagnostic_evidence",
        "producer": "mncs-harness",
        "record_kind": "ActorProvenance",
        "native_schema_version": "mncs-harness/actor-provenance/v0alpha1",
        "stable_record_id": HARNESS_ACTOR_ID,
        "declared_scope": {"harness_role": "skeptic", "model": "fixture-model"},
        "compatibility_status": "supported",
        "evidence_status": "UNKNOWN",
    },
]

OUT.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
print("wrote", OUT)
