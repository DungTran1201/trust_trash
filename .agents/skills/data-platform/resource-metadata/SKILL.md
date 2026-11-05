---
name: resource-metadata
description: "Design and evolve the Universal Resource Model, metadata catalog, source identity, provenance, relationships and freshness semantics."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Resource and Metadata Modeling

## Modeling principles
- A resource has a stable Trust Trash identity and a provider-native identity.
- Separate resource identity/metadata from content bytes, search projections, derived artifacts and access policy.
- Preserve source structure. A relational row, table, PDF page, image region, repository file and browser history entry are not interchangeable blobs.
- Metadata is versioned and may evolve independently from provider payloads.

## Required identity fields
`resource_id`, `workspace_id`, `source_id`, `external_id`, `resource_type`, `canonical_uri`, `parent_resource_id` where applicable, `source_created_at`, `source_updated_at`, `discovered_at`, `ingested_at`, `processed_at`, `indexed_at`, `etag/checksum`, `schema_ref`, `acl_ref`, `provenance_ref`, `metadata_version`, `status`.

## Identity and deduplication
Use `(workspace_id, source_id, external_id)` as the provider identity key unless a provider-specific immutable ID requires a different scheme. Do not deduplicate solely by title or content similarity. Keep cross-source equivalence as a relationship (`same_as`, `derived_from`, `references`, `contains`, `implements`) with confidence and evidence, not by destructive merging.

## Metadata discovery workflow
1. Discover provider account/project/container/database hierarchy.
2. Normalize resource type and parent relationships.
3. Store raw provider metadata separately from normalized common fields.
4. Record observed schema/version and last observed timestamp.
5. Detect additions, updates, removals and permission changes.
6. Publish metadata/resource events for indexing and governance consumers.

## Provenance
For every derived artifact preserve source resource IDs, source URI, extraction method, connector version, processor/model version, run ID, input checksum, output checksum, timestamps and transformation lineage. A result must be traceable from index/warehouse back to the original source.

## Schema evolution
Use additive, backward-compatible changes when possible. Mark deprecated fields with migration windows. Unknown provider fields may be preserved in an extension map but must not silently override canonical fields. Validate contract versions at boundaries.

## Acceptance
Test stable IDs across repeated sync; update detection; deletion tombstones; two sources with same title remain distinct; hierarchy; schema drift; provenance chain; ACL reference updates; timestamp semantics; serialization compatibility.
