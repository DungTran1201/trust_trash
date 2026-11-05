from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class UniversalResource(BaseModel):
    """Portable reference to a resource; content can remain at its source."""

    model_config = ConfigDict(extra="allow")

    resource_id: str
    source_id: str
    external_id: str
    resource_type: str
    title: str
    uri: HttpUrl | str | None = None
    content_preview: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    source_updated_at: datetime | None = None
    indexed_at: datetime | None = None
    checksum: str | None = None
