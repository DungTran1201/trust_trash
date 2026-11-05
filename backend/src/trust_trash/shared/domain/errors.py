class TrustTrashError(Exception):
    """Base exception for expected application/domain errors."""


class CapabilityNotSupported(TrustTrashError):
    """Raised when a connector does not implement a requested capability."""


class ResourceNotFound(TrustTrashError):
    """Raised when a requested resource does not exist or is not visible."""
