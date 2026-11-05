---
name: secure-change
description: "Threat-model and implement secure changes involving identity, credentials, external connectors, source permissions, user data and web APIs."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Secure Change Workflow

## Threat-model sequence
1. Identify assets: credentials, personal data, source documents, tenant data, search snippets, browser history, pipeline state and audit logs.
2. Identify trust boundaries: browser, frontend, API, worker, connector plugin, provider API, queue, storage and admin.
3. Enumerate abuse cases: cross-tenant access, token leak, SSRF, injection, unsafe parsing, malicious connector, replay, overbroad browser permissions and stale ACL.
4. Enforce authorization at server/worker boundaries; never rely on hidden UI controls.
5. Use least privilege and scoped credentials. Store only secret references in ordinary configuration.
6. Validate URLs, redirects, content types, file size, archive expansion, MIME mismatch and untrusted payloads.
7. Defend URL fetchers against SSRF: allowlist schemes, block private/link-local/metadata IP ranges, re-check redirects/DNS and constrain egress.
8. Use parameterized SQL and read-only transactions by default. Never concatenate user input into SQL.
9. Redact telemetry. Never log tokens, passwords, cookies, auth headers or raw private document bodies.
10. Audit access, exports, permission failures, credential changes and destructive operations.
11. Add negative tests for unauthorized/malformed requests.

## Trust Trash requirements
Search indexes are governed copies, not a permission bypass. Re-check ACL before snippets/fetch. Propagate revocation/deletion to derived copies. Browser history and active-page content require explicit permission and retention controls. Treat connector/processor outputs as untrusted.

## Quality gate
Document residual risk and required operational controls. Consult OWASP ASVS and relevant Cheat Sheets.
