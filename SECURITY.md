# Security policy

MNCDS is experimental and pre-1.0. Until the validator migration is complete, supported-version statements remain provisional.

Report validator path escape, hash or identity confusion, schema bypass, unsafe execution, protected-evidence exposure, archive handling, dependency, release-integrity, or other security-sensitive issues privately through GitHub's security advisory interface. Do not open a public exploit issue before coordination.

Include the affected version or commit, impact, minimal reproduction when safe to share, and any suggested mitigation.

## Scope boundary

An MNCDS validator should treat development records, candidate metadata, archives, bindings, and externally supplied evidence as untrusted input. Validation must not silently execute candidate code or external evidence merely because a record references it.

MNCDS conformance is not a security warranty. A `PASS` result does not establish sandboxing, organizational independence, protected custody, confidentiality, operational safety, or resistance to a malicious host unless those properties are separately supported by the required evidence.

Security issues in MNCS-owned implementation-evidence semantics belong to the MNCS repository unless they also expose a distinct MNCDS specification, interoperability, or validator defect.
