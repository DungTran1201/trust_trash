"""Search-index update worker.

Placeholder entry point. Queue consumption and graceful shutdown are not implemented yet.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trust_trash.workers.indexing")


def main() -> None:
    logger.warning("Indexing worker is a placeholder; no tasks are consumed.")


if __name__ == "__main__":
    main()
