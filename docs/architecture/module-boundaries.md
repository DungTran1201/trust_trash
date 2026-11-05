# Module Boundaries

| Module | Owns | Must not own |
|---|---|---|
| identity | users, sessions, workspace identity | source data content |
| connections | connection instances and credential references | connector implementation details |
| connector_registry | manifests, capabilities, connector versions | user secrets in plaintext |
| resources | canonical resource identity and provenance | all source content copies |
| discovery | query plans, retrieval and result aggregation | connector-specific SDK internals |
| ingestion | sync state, cursors and ingestion jobs | interactive search sessions |
| processing | processor execution metadata and derived artifacts | source system permissions |
| storage | storage references and provider adapters | business rules of other domains |
| analytics | curated dataset definitions and analytics access | raw source credentials |
| governance | policies, classifications, audits and retention | connector-specific transport |
| observability | health and operational telemetry interfaces | domain business data ownership |

Cross-module access must use public application interfaces, ports, or versioned events. Avoid direct imports of private repositories and models from another module.
