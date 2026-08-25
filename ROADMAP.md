# MNCDS Repository Roadmap

Statuses are evidence-based as of 2026-08-25. An item is marked complete only
when the repository itself proves it (committed artifacts, tests, or CI).

## Phase 0 — Repository bootstrap

- [x] Independent project identity and scope
- [x] Governance and contribution boundary
- [x] MNCS interoperability contract
- [x] Migration plan and ownership inventory
- [x] Directory and CI scaffolding

## Phase 1 — Provenance-preserving extraction

- [x] Freeze the actual MNCS source commit used for migration
      (`f0088c4d46dec84f289d9b4417eec32b0ac028e6`, pinned in spec provenance
      headers and `migration/inventory.json`; policy documented there)
- [x] Transfer MNCDS 0.1 draft and 0.1-rc.1 specification material
- [x] Transfer MNCDS-owned schemas and examples
- [x] Split shared release-candidate conformance vectors by normative owner
      (`corpus.json` for 0.1-draft, `corpus-0.1-rc1.json` for 0.1-rc.1,
      `corpus-0.2-alpha.json` for the alpha surface; all executable via
      `conformance/run_corpus.py`)
- [x] Classify historical RFCs, docs, and case studies
      (`rfcs/README.md`, `docs/mncds-decisions.md`,
      `docs/interoperability/MNCS-v0.3-MNCDS-v0.1-decisions.md`)
- [x] Record provenance for migrated artifacts

## Phase 2 — Independent validation surface

- [x] Extract the `mncds` CLI and validator behavior from the mixed historical implementation
- [x] Preserve pre/post-migration fixture outcomes
- [x] Remove source-tree coupling to the MNCS repository
- [x] Establish package metadata and developer environment
- [x] Add MNCDS-specific unit, schema, adversarial, and conformance CI
      (`pytest`, `ruff`, `mypy`, `conformance/run_corpus.py`, example
      validation in `.github/workflows/ci.yml`)

## Phase 3 — Family-integrated development-process protocol

New phase opened by the family's evolution since extraction.

- [x] Versioned producer-record binding surface (RFC 0005; `0.2-alpha.1`
      schema, validator support, conformance corpus)
- [x] Real development-case reconstruction: mncs-language module-import span
      repair encoded as an MNCDS D3→D1 record with pinned producer identities
      (`examples/mncds-0.2-alpha/language-span-fix.development-record.json`)
- [x] Commons Family Record Spine participation: `DevelopmentRecord`
      classification, producer-reference support, and a spine exercise path
      Control → Harness → Language → Fabric → Forge → Concept Experiment →
      **MNCDS** → Commons (implemented in MNCS-Commons)
- [ ] Promote bindings from experimental alpha to a 0.2 release candidate
      after additional real episodes accumulate
- [ ] MNCS assurance projection onto selected candidates (stop at the clean
      MNCDS boundary until MNCS side defines the consuming interface)

## Phase 4 — Independent release line

- [x] Publish a version/support matrix (`docs/VERSION-SUPPORT.md`)
- [x] Establish release checklist and artifact hashing (`RELEASE-CHECKLIST.md`)
- [ ] Establish independent tags/releases for MNCDS (first prerelease pending
      merge of this tranche)
- [x] Document supported MNCS binding versions (schema `mncs_binding.mncs_version`
      plus RFC 0005 generic bindings; see `docs/VERSION-SUPPORT.md`)
- [x] Complete or explicitly disclose bootstrap governance gaps
      (`GOVERNANCE.md` records OPEN rosters; records must not claim authorities
      that do not exist)

## Phase 5 — Historical MNCS cleanup

Performed in the sibling MNCS repository:

- [x] Point MNCDS specification authority at the independent MNCDS repository
      (MNCS PR #64)
- [x] Retain MNCS-side schema copies as consumer/consumed compatibility
      surfaces with pointer documentation
- [ ] Verify no accidental duplicate normative copies remain after MNCS next
      schema reorganization

## Long-term direction

Keep MNCDS focused on development-process governance and evidence, not on becoming a general orchestration framework. Forge, RAVEL, Fabric, local models, frontier agents, programming languages, and other mechanisms should be able to implement or exercise MNCDS without becoming required architecture of the specification itself.
