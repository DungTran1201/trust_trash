from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from trust_trash.connector_sdk.contracts import ConnectorCapabilities
from trust_trash.shared.contracts.resource import UniversalResource
from trust_trash.shared.contracts.search import SearchRequest


class BaseConnector(ABC):
    """Base contract. Implement only capabilities declared by the manifest."""

    @property
    @abstractmethod
    def capabilities(self) -> ConnectorCapabilities:
        raise NotImplementedError

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    async def discover(self) -> list[dict[str, Any]]:
        raise NotImplementedError("discovery capability is not implemented")

    async def search(self, request: SearchRequest) -> list[UniversalResource]:
        raise NotImplementedError("search capability is not implemented")

    async def fetch(self, external_id: str) -> Any:
        raise NotImplementedError("fetch capability is not implemented")

    async def sync(self, cursor: str | None = None) -> AsyncIterator[Any]:
        raise NotImplementedError("sync capability is not implemented")
        yield  # Makes this an async generator for type-checking purposes.

    async def health_check(self) -> dict[str, Any]:
        return {"status": "unknown"}

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
