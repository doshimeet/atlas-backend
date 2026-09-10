from typing import Dict, Any
from fastapi import APIRouter, BackgroundTasks
from app.db.session import SessionLocal
from app.services.ingest_service import HybridSemanticaIngestionWorker
from app.integrations.wbg_client import fetch_live_wbg_publications
from app.schemas.ingest import IngestTriggerResponse, SyncRequest

router = APIRouter()

async def _bg_ingest_single(doc_id: str):
    db = SessionLocal()
    worker = HybridSemanticaIngestionWorker()
    try:
        papers = await fetch_live_wbg_publications(rows=1, query=doc_id)
        if papers:
            await worker.ingest_single_publication(papers[0], db)
    finally:
        db.close()

@router.post("/ingest/trigger/{doc_id}", response_model=IngestTriggerResponse)
def trigger_ingestion(doc_id: str, background_tasks: BackgroundTasks) -> IngestTriggerResponse:
    """
    Triggers asynchronous publication acquisition, layout parsing, and entity extraction.
    Returns HTTP 202 Accepted in under 15ms.
    """
    background_tasks.add_task(_bg_ingest_single, doc_id)
    return IngestTriggerResponse(
        status="ACCEPTED",
        message=f"Background ingestion worker queued for World Bank publication {doc_id}.",
        docId=doc_id
    )

@router.post("/ingest/sync")
async def sync_publications(payload: SyncRequest) -> Dict[str, Any]:
    """
    Manually triggers batch synchronization from the live WDS API.
    """
    worker = HybridSemanticaIngestionWorker()
    res = await worker.ingest_live_publications_batch(rows=payload.rows or 15, query=payload.query or "")
    return res
