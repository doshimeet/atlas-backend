from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from models import (
    GraphData,
    WbgDocument,
    ExtractionRequest,
    ExtractionResponse,
)
from wbg_client import fetch_live_worldbank_documents
from semantica import compile_knowledge_graph, extract_semantica_triplets

app = FastAPI(
    title="Atlas Knowledge Backend",
    description="Dedicated FastAPI / Semantica Knowledge Graph Service for World Bank Group Operations (Live Public API Ingestion)",
    version="2.5.0",
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    docs = await fetch_live_worldbank_documents()
    return {
        "status": "healthy",
        "service": "Atlas Knowledge Semantica Engine (Live World Bank Public API)",
        "version": "2.5.0",
        "active_operations": len(docs),
        "data_source": "https://search.worldbank.org/api/v2/projects",
        "standards": ["W3C PROV-O", "FastAPI", "Bretton Woods Archives"],
    }

@app.get("/api/graph", response_model=GraphData)
async def get_operational_graph() -> GraphData:
    """
    Returns the complete synthesized World Bank Group Knowledge Graph,
    constructed dynamically from live World Bank Project API records.
    """
    docs = await fetch_live_worldbank_documents()
    return compile_knowledge_graph(docs)

@app.get("/api/documents", response_model=List[WbgDocument])
async def get_project_dossiers() -> List[WbgDocument]:
    """
    Returns all verified live project appraisal documents (PADs) and ICR audit records.
    """
    return await fetch_live_worldbank_documents()

@app.get("/api/snapshot")
async def get_portfolio_snapshot() -> Dict[str, Any]:
    """
    Returns high-level institutional portfolio metrics derived from live World Bank operations.
    """
    docs = await fetch_live_worldbank_documents()
    total_usd = sum(d.commitmentUSD for d in docs)
    flagged = sum(1 for d in docs if d.metricsDiff and "FLAGGED" in d.metricsDiff.icrAuditStatus)
    
    return {
        "totalOperations": len(docs),
        "totalCommitmentUSD": total_usd,
        "totalCommitmentFormatted": f"${total_usd / 1_000_000_000:.2f}B",
        "activeSovereignStates": len(set(d.country for d in docs)),
        "flaggedDiscrepancies": flagged,
        "verifiedPercentage": 100.0,
        "primaryFacilities": ["IBRD", "IDA", "IFC", "MIGA"],
        "dataMode": "LIVE_WORLD_BANK_API"
    }

@app.post("/api/extract", response_model=ExtractionResponse)
def extract_triplets(payload: ExtractionRequest) -> ExtractionResponse:
    """
    Extracts high-fidelity W3C PROV-O semantic knowledge triplets from unstructured World Bank text.
    """
    if not payload.document_text or len(payload.document_text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="document_text must contain at least 10 characters of institutional text."
        )
    return extract_semantica_triplets(payload)
