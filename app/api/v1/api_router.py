from fastapi import APIRouter
from app.api.v1.endpoints import (
    health_router,
    graph_router,
    documents_router,
    snapshot_router,
    ingest_router,
    reports_router,
    extract_router,
)

api_router = APIRouter()

# Core Domain Routes
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(graph_router, tags=["Knowledge Graph"])
api_router.include_router(documents_router, tags=["Documents & Publications"])
api_router.include_router(snapshot_router, tags=["Portfolio Snapshot"])
api_router.include_router(ingest_router, tags=["Ingestion & ETL"])
api_router.include_router(reports_router, tags=["Executive Reports"])
api_router.include_router(extract_router, tags=["Extraction"])
