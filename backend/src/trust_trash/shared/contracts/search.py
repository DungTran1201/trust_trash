from typing import Any, Literal

from pydantic import BaseModel, Field

from trust_trash.shared.contracts.resource import UniversalResource


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=512)
    source_ids: list[str] | None = None
    resource_types: list[str] | None = None
    limit_per_source: int = Field(default=20, ge=1, le=100)


class SourceCoverage(BaseModel):
    source_id: str
    status: Literal["searched", "partial", "failed", "skipped"]
    reason: str | None = None
    result_count: int = 0


class SearchResponse(BaseModel):
    query: str
    status: Literal["completed", "partial", "failed"]
    results: list[UniversalResource] = Field(default_factory=list)
    coverage: list[SourceCoverage] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
