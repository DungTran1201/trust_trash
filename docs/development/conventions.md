# Development Conventions

- Use type hints on public Python interfaces.
- Keep domain logic independent from FastAPI, SQLAlchemy, cloud SDKs and search clients.
- Define explicit DTOs at module boundaries.
- Do not share ORM models across bounded contexts.
- Use async I/O for network-bound operations; use process/work queues for CPU/GPU-heavy work.
- Make worker operations idempotent where possible.
- Propagate correlation IDs through API requests, jobs and events.
- Never log credentials, access tokens, cookies or full sensitive payloads.
- Add unit tests for domain/application rules and integration tests for adapters.
- Every placeholder must be labeled as such and have an implementation issue before production use.
