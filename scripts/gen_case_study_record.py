"""One-off generator for the mncs-language span-fix case-study record.

Writes examples/mncds-0.2-alpha/language-span-fix.development-record.json as
canonical, valid JSON. Kept in the working tree only during this tranche.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = "github.com/epi13/mncs-language"
COMMIT_A = "67fc26f49ef7c12130f9828231253464a6ce0388"
COMMIT_B = "cdee9783bd9a8e05e487fb0146515aa6736d6769"
FAIL_EVIDENCE = "sha256:8b9d854949b511108b8d1f5ded681e4d2b6fd5fde33bb4fdd8517353d638b3bb"
PASS_EVIDENCE = "sha256:1e1c49a23a91343a13f1abdecfe3d4481b8887224f6b83293da52528f4c62e7b"
STUDY_ID = (
    "mncs:compiler:compilation-study-result:"
    "78bd8cbdb0697c46febbf299ffc3e4818b1381f14a304b2cb97f059debd7fa3c"
)
STUDY_DIGEST = "sha256:925326f6b583420a64596308f93c8470601f668892d93e5fd68e519cd5d07152"
COMPILER_ID = "mncs:compiler:compiler:f862227638ca7fbc716123d8378cddfef4f76a9ef10ab0e99cc791e65207e45d"
TARGET_ID = "mncs:compiler:target-contract:8b1b5cfaa3d4e5be63c4c42af2334fda37b15f7bd4f81283dc1a049a7c61c81e"

record = {
    "schema_version": "0.2-alpha.1",
    "mncds_version": "0.2-alpha.1",
    "record_id": "development.mncs-language-span-fix-2026-08",
    "profile": "MNCDS-D1",
    "epoch_id": "epoch.span-fix-1",
    "created_at": "2026-08-25T00:00:00Z",
    "supersedes_record_id": None,
    "charter": {
        "charter_id": "charter.mncs-language-span-resolution",
        "problem_statement": (
            "Source Profile 0.6 module imports lose the declaring source spans of "
            "imported declarations during elaboration-time linking, so language "
            "tooling cannot resolve an imported call site to its declaration."
        ),
        "intended_use": (
            "Repair the mncs-language frontend so name resolutions retain declaring "
            "spans across module imports, exercised through the module_imports corpus."
        ),
        "exclusions": [
            "No MNCS implementation-assurance claim is made.",
            "Organizational independence of review is not claimed; roster is OPEN.",
            "Backend execution behavior is out of scope for this episode.",
        ],
        "contract_id": "contract.module-imports-tooling-resolution",
        "baseline_id": "baseline.mncs-language-imports-baseline",
        "environment_id": "environment.mncs-language-dev",
        "threat_model_id": "threat.tooling-silent-resolution-loss",
        "objective": {
            "objective_id": "objective.imported-span-resolution",
            "metric": "module_imports regression failures",
            "unit": "failing assertions",
            "direction": "minimize",
            "minimum_useful_benefit": 1,
            "operational_rationale": (
                "Language-service navigation across imports must resolve to the exact "
                "declaring span; a lost span is a silent tooling defect."
            ),
        },
        "selection_policy_id": "selection.policy.regression-green",
        "planned_mncs_level": None,
        "hard_rejection_gates": [
            "gate.imported-span-resolution",
            "gate.no-module-imports-regression",
        ],
        "release_owner_id": "authority.epi13-maintenance",
        "rollback_owner_id": "authority.epi13-maintenance",
        "retirement_owner_id": "authority.epi13-maintenance",
    },
    "baseline": {
        "baseline_id": "baseline.mncs-language-imports-baseline",
        "artifact_id": f"mncs-language.src.{COMMIT_A}",
        "source_id": f"github.epi13.mncs-language.{COMMIT_A}",
        "build_id": "build.cargo-workspace-67fc26f",
        "dependency_ids": ["dependency.rust-1.97.1", "dependency.cargo-workspace"],
        "environment_id": "environment.mncs-language-dev",
        "evaluator_ids": ["evaluator.cargo-module-imports"],
        "results": [
            {
                "evaluator_id": "evaluator.cargo-module-imports",
                "gate_id": "gate.imported-span-resolution",
                "partition_id": "partition.development",
                "required": True,
                "status": "FAIL",
                "evidence_id": FAIL_EVIDENCE,
            }
        ],
        "captured_at": "2026-08-25T00:00:00Z",
        "immutable": True,
    },
    "environment_lock": {
        "environment_id": "environment.mncs-language-dev",
        "toolchain_id": "toolchain.cargo-1.97.1-fedora",
        "dependency_ids": ["dependency.rust-1.97.1", "dependency.cargo-workspace"],
        "hardware_id": "hardware.epi13-workstation",
        "configuration_id": "configuration.workspace-worktree-pinned-commits",
        "permitted_variance": [
            "Wall-clock durations vary; test outcomes are deterministic for pinned commits.",
        ],
        "locked": True,
    },
    "roles": [
        {"role": "contract_authority", "authority_id": "authority.epi13-maintenance", "executable_id": None},
        {"role": "generator_authority", "authority_id": "authority.agent-development-session", "executable_id": "generator.agent-session-span-repair"},
        {"role": "evaluator_authority", "authority_id": "authority.cargo-test-harness", "executable_id": "evaluator.cargo-test-executable"},
        {"role": "selection_authority", "authority_id": "authority.epi13-maintenance", "executable_id": None},
        {"role": "release_authority", "authority_id": "authority.epi13-maintenance", "executable_id": None},
        {"role": "independent_reviewer", "authority_id": "authority.community-review-open-roster", "executable_id": None},
    ],
    "authority_overlaps": [
        {
            "authority_id": "authority.epi13-maintenance",
            "roles": ["contract_authority", "selection_authority", "release_authority"],
            "scope": "Bootstrap-phase repository maintenance of epi13/mncs-language.",
            "rationale": (
                "The project operates under bootstrap governance with a single "
                "maintainer of record; separating contract, selection, and release "
                "authorities is not yet organizationally possible."
            ),
            "risk": "Contract, acceptance, and release decisions are not independently checked.",
            "recusal_or_control": (
                "Disclosed bootstrap overlap. Independent-review authority remains "
                "unassigned (OPEN roster), so organizational independence stays UNKNOWN "
                "and no assurance claim derives from selection or release."
            ),
        }
    ],
    "generator": {
        "generator_id": "generator.agent-session-span-repair",
        "configuration_id": "generator.configuration.agent-tranche-2026-08",
        "authority_id": "authority.agent-development-session",
        "executable_id": "generator.agent-session-span-repair",
        "permissions": {
            "modify_contract": False,
            "modify_baseline": False,
            "modify_evaluators": False,
            "modify_selection_policy": False,
            "modify_thresholds": False,
            "access_protected_holdout": False,
            "network_access": True,
            "filesystem_scope": ["mncs-language working tree"],
            "process_scope": ["cargo build", "cargo test", "cargo run -p mncs-cli"],
            "tool_ids": ["mncs-cli", "cargo"],
            "mutation_scope": [
                "crates/mncs-compiler/src/frontend.rs",
                "crates/mncs-compiler/tests/module_imports.rs",
            ],
        },
        "resource_limits": {
            "max_candidates": 2,
            "max_wall_seconds": 3600,
            "max_memory_bytes": 4294967296,
            "max_processes": 16,
        },
    },
    "partitions": {
        "development_id": "partition.development",
        "selection_id": "partition.selection",
        "final_evaluation_id": None,
        "holdout_contaminated": False,
        "access_policy_ids": ["policy.repository-visible-evidence"],
    },
    "protected_evidence": [],
    "evaluators": [
        {
            "evaluator_id": "evaluator.cargo-module-imports",
            "purpose": "development",
            "authority_id": "authority.cargo-test-harness",
            "executable_id": "evaluator.cargo-test-executable",
            "configuration_id": "configuration.cargo-test-module_imports",
            "environment_id": "environment.mncs-language-dev",
            "independent": False,
            "operator_independence": "UNKNOWN",
            "organizational_independence": "UNKNOWN",
            "regression_corpus_id": f"corpus.module-imports.{COMMIT_B}",
        }
    ],
    "candidates": [
        {
            "candidate_id": "candidate.mncs-language-67fc26f",
            "parent_ids": [],
            "epoch_id": "epoch.span-fix-1",
            "generator_id": "generator.agent-session-span-repair",
            "generation_sequence": 0,
            "materially_evaluated": True,
            "retained": True,
            "build_status": "PASS",
            "disposition": "rejected",
            "objective_value": 1,
            "evaluator_results": [
                {
                    "evaluator_id": "evaluator.cargo-module-imports",
                    "gate_id": "gate.imported-span-resolution",
                    "partition_id": "partition.development",
                    "required": True,
                    "status": "FAIL",
                    "evidence_id": FAIL_EVIDENCE,
                }
            ],
        },
        {
            "candidate_id": "candidate.mncs-language-cdee978",
            "parent_ids": ["candidate.mncs-language-67fc26f"],
            "epoch_id": "epoch.span-fix-1",
            "generator_id": "generator.agent-session-span-repair",
            "generation_sequence": 1,
            "materially_evaluated": True,
            "retained": True,
            "build_status": "PASS",
            "disposition": "selected",
            "objective_value": 0,
            "evaluator_results": [
                {
                    "evaluator_id": "evaluator.cargo-module-imports",
                    "gate_id": "gate.imported-span-resolution",
                    "partition_id": "partition.development",
                    "required": True,
                    "status": "PASS",
                    "evidence_id": PASS_EVIDENCE,
                },
                {
                    "evaluator_id": "evaluator.cargo-module-imports",
                    "gate_id": "gate.no-module-imports-regression",
                    "partition_id": "partition.selection",
                    "required": True,
                    "status": "PASS",
                    "evidence_id": PASS_EVIDENCE,
                },
            ],
        },
    ],
    "candidate_aggregates": [],
    "selection": {
        "policy_id": "selection.policy.regression-green",
        "selection_epoch_id": "epoch.span-fix-1",
        "selected_candidate_id": "candidate.mncs-language-cdee978",
        "rule_recorded_before_final_evaluation": True,
        "unknown_policy": "reject",
        "minimum_useful_benefit_met": True,
        "hard_gates_passed": True,
        "rationale": (
            "The repair candidate resolves imported call sites to their declaring "
            "spans and passes the full module_imports suite (8/8); it was merged to "
            f"mncs-language main as {COMMIT_B}. The predecessor candidate is "
            "rejected and retained as lineage."
        ),
        "human_review": None,
    },
    "reproducibility": {
        "class": "EXACT",
        "seeds_preserved": True,
        "protocol": (
            "Check out the pinned commit in a clean worktree, apply the recorded "
            "regression corpus, run cargo test -p mncs-compiler --test module_imports; "
            "outcomes are deterministic for pinned commits."
        ),
        "measurement_repetitions": 2,
        "comparison_statistic": "Exact per-test outcome equality.",
        "acceptance_bounds": "All outcomes must reproduce exactly; any divergence is FAIL.",
        "failure_treatment": "A failed regeneration attempt is FAIL; an unrunnable one is UNKNOWN.",
    },
    "epochs": [
        {
            "epoch_id": "epoch.span-fix-1",
            "parent_epoch_id": None,
            "toolchain_id": "toolchain.cargo-1.97.1-fedora",
            "corpus_id": "corpus.module-imports-regression",
            "objective_id": "objective.imported-span-resolution",
            "contract_id": "contract.module-imports-tooling-resolution",
            "threshold_policy_id": "threshold.zero-regression-failures",
            "development_partition_id": "partition.development",
            "final_partition_id": None,
            "change_evidence_ids": [FAIL_EVIDENCE],
            "regression_fixture_ids": [
                "fixture.imported_name_resolutions_retain_the_declaring_source_span",
            ],
        }
    ],
    "mncs_binding": None,
    "release_controls": None,
    "producer_bindings": [
        {
            "binding_id": "binding.commit.baseline",
            "role": "diagnostic_evidence",
            "producer": REPO,
            "record_kind": "Commit",
            "native_schema_version": "git",
            "stable_record_id": COMMIT_A,
            "compatibility_status": "supported",
            "evidence_status": "UNKNOWN",
            "subject_candidate_id": "candidate.mncs-language-67fc26f",
            "artifact": {
                "identity": f"mncs-language@{COMMIT_A}",
                "kind": "source-revision",
                "location": f"https://github.com/epi13/mncs-language/commit/{COMMIT_A}",
            },
            "declared_scope": {
                "repository_revision": COMMIT_A,
                "summary": "module imports feature introduction; evaluated baseline subject",
            },
            "notes": (
                "Source-revision pin only; it carries no outcome claim, so its "
                "evidence status is UNKNOWN by construction."
            ),
        },
        {
            "binding_id": "binding.commit.selected",
            "role": "diagnostic_evidence",
            "producer": REPO,
            "record_kind": "Commit",
            "native_schema_version": "git",
            "stable_record_id": COMMIT_B,
            "compatibility_status": "supported",
            "evidence_status": "UNKNOWN",
            "subject_candidate_id": "candidate.mncs-language-cdee978",
            "artifact": {
                "identity": f"mncs-language@{COMMIT_B}",
                "kind": "source-revision",
                "location": f"https://github.com/epi13/mncs-language/commit/{COMMIT_B}",
            },
            "declared_scope": {
                "repository_revision": COMMIT_B,
                "summary": "span preservation fix merged to main; selected candidate source",
            },
        },
        {
            "binding_id": "binding.regression-counterexample",
            "role": "development_feedback",
            "producer": REPO,
            "record_kind": "TestCorpusEntry",
            "native_schema_version": "rust-test",
            "stable_record_id": (
                f"{COMMIT_B}#crates/mncs-compiler/tests/module_imports.rs"
                "#imported_name_resolutions_retain_the_declaring_source_span"
            ),
            "compatibility_status": "supported",
            "evidence_status": "FAIL",
            "subject_candidate_id": "candidate.mncs-language-67fc26f",
            "partition_id": "partition.development",
            "declared_scope": {
                "candidate_identity": "candidate.mncs-language-67fc26f",
                "test_binary": "module_imports",
            },
            "notes": (
                "Retained failing assertion demonstrating that the imports-only "
                "candidate does not resolve imported call sites. FAIL is preserved "
                "as first-class development evidence; it is permitted feedback "
                "because it originates in the development partition."
            ),
        },
        {
            "binding_id": "binding.compiler-study.baseline",
            "role": "reproduction_evidence",
            "producer": "mncs-language",
            "record_kind": "CompilationStudyResult",
            "native_schema_version": "mncs-language.family-compiler-reference.v0.1",
            "stable_record_id": STUDY_ID,
            "content_digest": STUDY_DIGEST,
            "compatibility_status": "supported",
            "subject_candidate_id": "candidate.mncs-language-67fc26f",
            "declared_scope": {
                "compiler": COMPILER_ID,
                "target": TARGET_ID,
                "compilation_status": "completed_with_unresolved_obligations",
            },
            "evidence_status": "UNKNOWN",
            "notes": (
                "Rerun of compiler-study on the pinned baseline commit (2026-08-25). "
                "Compilation completes with an unresolved integer-overflow obligation, "
                "so the producer outcome remains UNKNOWN; compilation identity is "
                "unaffected by the span repair."
            ),
        },
        {
            "binding_id": "binding.compiler-study.selected",
            "role": "reproduction_evidence",
            "producer": "mncs-language",
            "record_kind": "CompilationStudyResult",
            "native_schema_version": "mncs-language.family-compiler-reference.v0.1",
            "stable_record_id": STUDY_ID,
            "content_digest": STUDY_DIGEST,
            "compatibility_status": "supported",
            "rerun_of_binding_id": "binding.compiler-study.baseline",
            "declared_changes": [
                (
                    "subject source revision changed from "
                    f"{COMMIT_A} to {COMMIT_B}"
                ),
                "verification rerun executed 2026-08-25 in a pinned worktree",
            ],
            "subject_candidate_id": "candidate.mncs-language-cdee978",
            "declared_scope": {
                "compiler": COMPILER_ID,
                "target": TARGET_ID,
                "observation": (
                    "identical CompilationStudyResult identity on both sides of the "
                    "repair; backend-neutral compilation semantics were unchanged by "
                    "the span fix"
                ),
            },
            "evidence_status": "UNKNOWN",
            "notes": (
                "Declared rerun of binding.compiler-study.baseline against the "
                "repaired candidate; identical study identity demonstrates the repair "
                "changed only span bookkeeping. Producer outcome remains UNKNOWN "
                "(unresolved obligations)."
            ),
        },
    ],
    "extensions": {
        "io.github.epi13:mncs-language": {
            "episode_class": "historical reconstruction with declared verification rerun",
            "original_episode": {
                "discovered": "2026-08-24 during Source Profile 0.6 module-imports tranche",
                "fix_merged_to_main_as": COMMIT_B,
                "feature_commit": COMMIT_A,
            },
            "verification_rerun": {
                "executed": "2026-08-25",
                "method": "clean git worktrees at pinned commits; regression test applied to predecessor",
                "predecessor_outcome": "FAIL (assertion 'imported call is resolved')",
                "selected_outcome": "PASS (8 passed; 0 failed)",
            },
            "downstream_consumers": [
                "mncs-language-service name resolution",
                "RAVEL Profile 0.6 friction notes",
            ],
        }
    },
}

out = Path("examples/mncds-0.2-alpha/language-span-fix.development-record.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
print("wrote", out)
