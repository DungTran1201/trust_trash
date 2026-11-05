# Database infrastructure

PostgreSQL is the initial application metadata store. Define migrations and schema ownership per bounded context before adding persistent business tables. Do not allow one domain to write directly to another domain's tables.
