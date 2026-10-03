# RFC 0006: Declared project structure and projection roles

Status: Experimental proposal, opt-in `mncds.project-structure-profile/1`.
Affected development specification: 0.2-alpha.1 companion profile. Released
0.1 development records, historical evidence and producer-binding rules retain
their existing identities and meaning.

Projects need structural expectations that machines can inspect without
assuming conventional directory names or interpreting README prose.
`profiles/semantic-project.json` declares required metadata paths and the
authoritative, derived, mixed and ephemeral interpretation roles. Repository
manifests declare actual directory/file roles and pin the selected profile by
content identity. An absent profile does not implicitly impose this anatomy.

Authoritative inputs MUST NOT be overwritten by projections. Derived targets
MUST have explicit declarations, dependencies, interpretation identities,
validation and provenance. Mixed documents MUST bound owned bytes unambiguously
and preserve authored bytes. Interpretation output MUST NOT establish evidence,
completion, conformance, or promotion by itself.

MNCDS owns these development expectations. MNCS Standard continues owning the
repository-manifest schema. Commons owns semantic projection declarations;
Doc owns interpretation/rendering; Doctor owns observed conformance and repair
admission; Environment consumes their declarations. None of these bindings
changes MNCS evidence semantics or creates independent review.

Failure: absent/inaccessible/moved authorities remain UNKNOWN; observed missing
required paths fail conformance; malformed/ambiguous ownership blocks repair.
Valid/invalid vectors live in `tests/test_project_structure_profile.py`.

Compatibility: existing repositories need no simultaneous migration. Add a
profile and explicit artifact ownership when adopting ambient projections.
