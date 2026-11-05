---
name: data-quality-lineage-governance
description: "Apply data contracts, quality validation, lineage, classification, ownership, retention and source-aware access controls across the data lifecycle."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Data Quality, Lineage and Governance

## Data contract
Every durable dataset/resource contract should define owner, schema/version, identifiers, timestamps, nullability, allowed values, semantics, classification, retention, freshness target and compatibility policy.

## Quality dimensions
- Completeness: required fields/records present.
- Uniqueness: business keys and duplicate rules.
- Validity: type, format, domain and range.
- Consistency: cross-field and cross-dataset invariants.
- Timeliness: freshness and event lateness.
- Accuracy: measured against trusted source/sample where possible.
- Integrity: referential and relationship constraints.

## Validation lifecycle
Validate connector envelope → raw write integrity → refined schema → business rules → warehouse model tests → published data product. Store check result, severity, rule version, affected partition/rows, sample-safe evidence and run ID. Route bad records to quarantine; do not silently drop them.

## Lineage
Represent source → job/run → input/output dataset/resource relationships. Record code, connector, processor and model versions. Distinguish observed lineage from inferred lineage. Use stable IDs and timestamps. For events, model job/run/dataset and lifecycle START/COMPLETE/FAIL/ABORT where OpenLineage is used.

## Governance workflow
Classify data → assign owner/steward → define access policy → map provider ACL → apply retention/deletion → audit accesses/exports → review exceptions. Treat index, embeddings, caches, extracts and analytics copies as derived governed data.

## Permission propagation
Track source ACL version/fingerprint and last checked time. On revocation, prevent result exposure immediately when possible, invalidate cached authorization, then remove/restrict derived index copies. Fail closed for sensitive content if authorization cannot be resolved. Distinguish denied from source unavailable.

## Acceptance
Test schema violation, null/duplicate thresholds, late data, lineage completeness, classification, tenant isolation, ACL revoke propagation, retention/deletion and audit trail.
