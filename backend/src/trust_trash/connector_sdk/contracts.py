from typing import Any

from pydantic import BaseModel, Field


class ConnectorCapabilities(BaseModel):
    discovery: bool = False
    metadata: bool = False
    search: bool = False
    fetch: bool = False
    query: bool = False
    sync: bool = False
    streaming: bool = False
    permission_discovery: bool = False


class ConnectorManifest(BaseModel):
    connector_id: str
    display_name: str
    version: str = "0.1.0"
    category: str
    capabilities: ConnectorCapabilities
    config_schema: dict[str, Any] = Field(default_factory=dict)
