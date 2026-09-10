"""
Legacy ingest_service module backward compatibility bridge.
Redirects imports to app.services.ingest_service.
"""
from app.services.ingest_service import HybridSemanticaIngestionWorker, _slugify

__all__ = ["HybridSemanticaIngestionWorker", "_slugify"]

if __name__ == "__main__":
    import sys
    import asyncio
    from app.db.session import init_db
    init_db()
    rows = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    worker = HybridSemanticaIngestionWorker()
    asyncio.run(worker.ingest_live_publications_batch(rows=rows))
