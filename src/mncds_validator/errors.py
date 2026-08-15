"""Validator exceptions for the MNCDS reference consumer."""

# SPDX-License-Identifier: Apache-2.0


class MncdsError(Exception):
    """Base class for expected MNCDS validator failures."""


class MncsError(MncdsError):
    """Compatibility alias used by the extracted MNCDS validator module."""


class SchemaNotFoundError(MncdsError):
    """Raised when a bundled schema name cannot be resolved."""


class ManifestError(MncdsError):
    """Raised when a development record cannot be loaded safely."""
