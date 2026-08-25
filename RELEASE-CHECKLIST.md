# MNCDS release checklist

This checklist governs any MNCDS specification or validator-package release.
Bootstrap governance notes apply: authorities recorded as OPEN in
`GOVERNANCE.md` block claims that require them; they do not block preparing a
release candidate.

## 1. Semantics

- [ ] Every normative change in the release is covered by an RFC at
      `rfcs/`, with status updated (Proposed → Accepted) through review.
- [ ] Released schemas of prior versions are byte-identical to their released
      state (`git diff` against the release tag proves it).
- [ ] Exact-version dispatch covers every schema shipped in
      `src/mncds_validator/resources/schemas/`.
- [ ] Tri-state semantics verified: no vector upgrades UNKNOWN to PASS;
      FAIL dominates where required.

## 2. Conformance

- [ ] `python conformance/run_corpus.py` passes every vector across all
      supported record versions.
- [ ] Every normative rule added or changed since the last release has at
      least one positive and one negative executable vector.
- [ ] Examples referenced by documentation validate with the packaged CLI.

## 3. Quality gates

- [ ] `ruff check src tests conformance scripts`
- [ ] `mypy src`
- [ ] `pytest -q`
- [ ] CI green on the release commit for all supported Python versions.

## 4. Artifacts and provenance

- [ ] Package version bumped per semantic-versioning policy (spec versions and
      package versions are independent).
- [ ] Sdist/wheel built, and sha256 hashes recorded in the release notes.
- [ ] Release notes identify: accepted RFCs, compatibility effects, known
      limitations, conformance status, migration impact.
- [ ] Git tag named `mncds-v<version>` signed or hash-pinned per available
      custody (disclose which).

## 5. Interoperability

- [ ] `docs/VERSION-SUPPORT.md` updated (record versions, MNCS binding
      versions, observed producer bindings).
- [ ] Downstream consumers notified when a producer family changes identity
      surfaces (Commons compatibility entries).
