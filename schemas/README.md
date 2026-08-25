# Schemas

This directory is the canonical home of MNCDS development-record schemas.

- `mncds-development-record.schema.json` — 0.1-draft aggregate schema
- `mncds-development-record-0.1.schema.json` — 0.1-rc.1 aggregate schema (released candidate)
- `mncds-development-record-0.2-alpha.schema.json` — experimental alpha implementing RFC 0005 (`producer_bindings`); may change or be withdrawn before any RC

Exact-version dispatch applies: a record's `mncds_version` selects its schema;
unknown versions are `UNSUPPORTED`, never approximated. Released schemas are
preserved byte-for-byte. Packaged copies live in
`src/mncds_validator/resources/schemas/` and must stay identical to this
directory.

MNCS may keep consumed copies for its local consumer. Those copies are not
authoritative.
