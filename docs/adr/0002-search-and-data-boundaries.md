# ADR-0002: Search, Source Data and Derived Data Boundaries

- Status: Proposed

## Decision direction

Keep source resources, metadata, search indexes and derived artifacts separate:
- Source: original system remains authoritative.
- Metadata: Trust Trash's canonical resource references and provenance.
- Search index: rebuildable projection for retrieval.
- Derived artifacts: extracted text, OCR output, normalized tables and embeddings, linked to the source resource and processor version.

Search results must preserve source identity and permission context. Index presence alone does not grant authorization to retrieve content.
