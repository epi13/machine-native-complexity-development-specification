# Conformance

This directory contains machine-checkable artifacts used to test implementations against a declared MNCDS version.

Recommended structure after migration:

```text
conformance/
  0.1/
    valid/
    invalid/
    corpus/
  interoperability/
    mncs-<version>/
```

A conformance fixture MUST identify the normative version it exercises. Cross-project fixtures MUST identify both MNCDS and MNCS versions and must not blur an MNCS result into an MNCDS result.

`PASS` means only that the tested implementation satisfied the declared conformance case within its scope. It does not create organizational independence, protected custody, security assurance, or release authority.
