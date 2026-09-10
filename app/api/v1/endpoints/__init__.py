from .health import router as health_router
from .graph import router as graph_router
from .documents import router as documents_router
from .snapshot import router as snapshot_router
from .ingest import router as ingest_router
from .reports import router as reports_router
from .extract import router as extract_router

__all__ = [
    "health_router",
    "graph_router",
    "documents_router",
    "snapshot_router",
    "ingest_router",
    "reports_router",
    "extract_router",
]
