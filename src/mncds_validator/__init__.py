"""Reference MNCDS validator.

This package is the MNCDS-owned consumer for MNCDS 0.1 development records.
It does not define MNCS implementation-evidence semantics.
"""

from .mncds import validate_development_record, validate_development_value

__all__ = ["validate_development_record", "validate_development_value"]
