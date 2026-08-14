# MNCDS Governance

MNCDS is a lightweight, open, community-developed experimental specification with independent normative authority from MNCS.

## Roles

- **Maintainers** administer the repository and releases.
- **Editors** integrate approved normative text, schemas, and conformance material.
- **Contributors** submit proposals, code, evidence, documentation, and research.
- **RFC authors** own proposed normative changes through review.
- **Reviewers** provide technical, security, compatibility, process, and interoperability review.

The repository owner acts as bootstrap maintainer until a public roster is adopted. Commit access alone does not imply normative authority.

Current bootstrap assignments:

- active maintainer roster: **OPEN**;
- active editor roster: **OPEN**;
- independent reviewer pool: **OPEN**;
- release authority: **OPEN**;
- signing authority and custody procedure: **OPEN**.

These OPEN fields block claims that require those authorities, but they do not block research, migration, implementation, or release-candidate preparation.

## Normative decisions

Work is public and consensus-seeking. Changes to normative meaning, record semantics, schemas, result aggregation, authority rules, lifecycle requirements, governance, or the MNCS interoperability contract require an RFC and explicit review.

Migration from the historical combined repository does **not** itself authorize semantic change. A migration commit may relocate or editorially normalize material while preserving meaning; semantic changes should be isolated and reviewed as such.

A single maintainer MUST NOT both author and finally approve a contested normative change. Reviewers disclose conflicts material to the decision and recuse where impartiality is reasonably in doubt.

## Relationship to MNCS governance

MNCS and MNCDS are sibling specifications. Neither repository's maintainers acquire decision authority over the other merely through technical dependency.

Cross-project changes should be handled as coordinated proposals with explicit version compatibility. An MNCDS RFC may propose a required MNCS interface version, but it cannot redefine MNCS. An MNCS change may require an MNCDS compatibility update, but it cannot silently rewrite MNCDS semantics.

## Releases and versions

MNCDS standard versions identify normative development-process semantics. Validator/tool packages use their own semantic versions.

- compatible additive changes increment the standard minor version;
- breaking normative meaning increments the major version;
- patch-level implementation fixes do not silently alter schema meaning;
- experimental extensions remain non-normative until adopted through governance.

Released schemas and historical record formats remain addressable. Release notes should identify accepted RFCs, compatibility, known limitations, conformance status, migration impact, and artifact hashes where applicable.

## Independence and authority claims

Repository governance cannot manufacture independent evaluation, protected custody, organizational independence, or an independent witness. Those claims require evidence from the relevant external actors and remain `UNKNOWN` when absent.

Reference validators, agents, Forge workflows, RAVEL mechanisms, models, and orchestration systems are non-normative implementations or development mechanisms unless a specific normative artifact explicitly defines an interface they must satisfy.

## Bootstrap completion

Bootstrap governance is complete only after the project publicly records:

- an active maintainer/editor roster;
- succession, inactivity, removal, and emergency-access rules;
- release and signing authorities;
- an independent reviewer pool or a disclosed inability to form one;
- conflict and material tool-ownership disclosure rules;
- a durable RFC process for changing development-process semantics; and
- a stable cross-project compatibility process with MNCS.

Until then, the project should describe itself as experimental and avoid stronger governance or independence claims.
