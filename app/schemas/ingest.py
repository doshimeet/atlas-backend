from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.schemas.common import W3CProvenance

class IngestTriggerResponse(BaseModel):
    status: str
    message: str
    docId: str

class SyncRequest(BaseModel):
    rows: Optional[int] = 15
    query: Optional[str] = ""

class ReportRequest(BaseModel):
    focus_id: Optional[str] = "34462766"

class ReportResponse(BaseModel):
    title: str
    assetId: Optional[str] = None
    markdown: str
    generatedAt: str
    provenanceHash: str

class ExtractionRequest(BaseModel):
    document_text: str
    doc_id: Optional[str] = "PAD-UPLOAD"
    country: Optional[str] = "Unknown"

class SemanticTriplet(BaseModel):
    subject: str
    predicate: str
    object: str
    citation: str
    hash: str
    prov_activity: str

class ExtractionResponse(BaseModel):
    doc_id: str
    triplets: List[SemanticTriplet]
    execution_time_ms: float
    provenance: W3CProvenance
