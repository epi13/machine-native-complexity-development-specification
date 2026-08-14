# MNCDS Repository Roadmap

## Phase 0 — Repository bootstrap

- [x] Independent project identity and scope
- [x] Governance and contribution boundary
- [x] MNCS interoperability contract
- [x] Migration plan and ownership inventory
- [x] Directory and CI scaffolding

## Phase 1 — Provenance-preserving extraction

- [ ] Freeze the actual MNCS source commit used for migration
- [ ] Transfer MNCDS 0.1 draft and 0.1-rc.1 specification material
- [ ] Transfer MNCDS-owned schemas and examples
- [ ] Split shared release-candidate conformance vectors by normative owner
- [ ] Classify historical RFCs, docs, and case studies
- [ ] Record provenance for migrated artifacts

## Phase 2 — Independent validation surface

- [ ] Extract the `mncds` CLI and validator behavior from the mixed historical implementation
- [ ] Preserve pre/post-migration fixture outcomes
- [ ] Remove source-tree coupling to the MNCS repository
- [ ] Establish package metadata and developer environment
- [ ] Add MNCDS-specific unit, schema, adversarial, and conformance CI

## Phase 3 — Independent release line

- [ ] Publish a version/support matrix
- [ ] Establish release checklist and artifact hashing
- [ ] Establish independent tags/releases for MNCDS
- [ ] Document supported MNCS binding versions
- [ ] Complete or explicitly disclose bootstrap governance gaps

## Phase 4 — MNCS cleanup

Performed in the sibling MNCS repository after this repository is independently testable:

- [ ] Remove transferred MNCDS normative source from active MNCS paths
- [ ] Replace it with concise pointers and compatibility documentation
- [ ] Split or simplify mixed validator/package surfaces
- [ ] Verify MNCS-only validation remains functional
- [ ] Ensure no accidental duplicate normative copies remain

## Long-term direction

Keep MNCDS focused on development-process governance and evidence, not on becoming a general orchestration framework. Forge, RAVEL, Fabric, local models, frontier agents, programming languages, and other mechanisms should be able to implement or exercise MNCDS without becoming required architecture of the specification itself.
