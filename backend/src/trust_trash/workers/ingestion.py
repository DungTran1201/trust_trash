"""Source synchronization and batch ingestion worker.

Placeholder entry point. Queue consumption and graceful shutdown are not implemented yet.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trust_trash.workers.ingestion")


def main() -> None:
    logger.warning("Ingestion worker is a placeholder; no tasks are consumed.")


if __name__ == "__main__":
    main()
