# MNCDS 0.2-alpha examples

| File | Version | Profile | Nature |
| --- | --- | --- | --- |
| `language-span-fix.development-record.json` | 0.2-alpha.1 | D1 | **real episode reconstruction** — mncs-language module-import span repair, with pinned commits and verification rerun |
| `d4-release-lifecycle.fixture.json` | 0.2-alpha.1 | D4 | synthetic-but-realistic fixture exercising release, monitoring, rollback, regeneration/replacement, and RFC 0005 bindings across Forge/Fabric/Harness producers |

## Honesty statement

The case-study record reconstructs a real development episode that happened in
[`epi13/mncs-language`](https://github.com/epi13/mncs-language):

- candidate A: `67fc26f49ef7c12130f9828231253464a6ce0388`
  (Source Profile 0.6 module imports) — the regression assertion
  `imported_name_resolutions_retain_the_declaring_source_span` FAILS against it
  (verified by rerun: the imported call is not resolved at all);
- candidate B: `cdee9783bd9a8e05e487fb0146515aa6736d6769` (span preservation)
  — the full `module_imports` suite passes (8/8), merged to `mncs-language`
  main.

Evidence digests pin actual captured test-run outputs from the declared
verification rerun of 2026-08-25. The original episode's own console output was
not digest-captured at the time; the record therefore declares itself a
reconstruction with a declared rerun rather than upgrading unverifiable history
into PASS claims. Organizational independence is not claimed (bootstrap
governance, OPEN rosters).

Validate:

```bash
mncds validate language-span-fix.development-record.json --require-pass
```

The D4 fixture makes no historical claim; it exists so profile-D4 lifecycle
semantics and producer bindings have executable coverage.
