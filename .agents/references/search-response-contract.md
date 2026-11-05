# Universal Search Response Contract

## Request concepts
`query`, `workspace_id` (derived/verified server-side), `resource_types`, `source_ids`, `filters`, `sort`, `cursor`, `limit`, `deadline_ms`, `result_budget`, `consistency_preference` and optional search mode. Never accept client-provided authorization claims as truth.

## Response envelope
- `query_id`: stable ID for the execution.
- `status`: `complete`, `partial`, `failed`, `cancelled`.
- `results[]`: normalized resource hit with `resource_id`, `source_id`, `external_id`, `resource_type`, `title`, safe `snippet`, `uri`, `score/signals`, `source_updated_at`, `indexed_at`, `freshness`, `provenance_ref` and optional `highlights`.
- `coverage`: eligible, searched, skipped, unsupported, unauthorized, timed_out, failed source counts and per-source details.
- `timing`: accepted/start/completed and per-source duration.
- `pagination`: next cursor, limit and has_more.
- `warnings[]`: stale index, approximate results, unavailable feature, partial ACL mapping, etc.

## Coverage semantics
- `searched`: execution actually started and completed or returned partial hits.
- `skipped`: planner did not query an eligible source; include reason (budget, unsupported query, user filter, policy).
- `unsupported`: connector cannot perform the requested action.
- `unauthorized`: credentials/user scope insufficient; do not disclose protected resource details.
- `timed_out`: per-source deadline exceeded.
- `failed`: source execution failed for another reason.
A zero-result successful search is not the same as a failed or unauthorized source.

## Result safety
Re-check user/workspace/source/resource authorization before exposing snippets or content. Do not expose unsafe provider errors. Keep provider URI canonical and use a fetch endpoint that reauthorizes. Search index may lag source; show freshness type/time. Never call response complete when eligible sources were skipped or failed.
