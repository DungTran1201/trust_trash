from abc import ABC, abstractmethod
from typing import Any


class BaseProcessor(ABC):
    """A processor transforms a source artifact into versioned output artifacts."""

    processor_id: str
    processor_version: str = "0.1.0"

    @abstractmethod
    async def validate_input(self, payload: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def process(self, payload: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    async def validate_output(self, result: dict[str, Any]) -> None:
        """Override to validate processor-specific output contracts."""
        return None
