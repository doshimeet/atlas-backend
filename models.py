from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class W3CProvenance(BaseModel):
    wasGeneratedBy: str = Field(..., description="Entity or Board authority that generated the record")
    wasDerivedFrom: str = Field(..., description="Source document URI or official portal link")
    documentSha256: str = Field(..., description="Cryptographic SHA-256 digest")
    provActivity: str = Field(..., description="W3C PROV-O Activity identifier")
    timestamp: str = Field(..., description="ISO timestamp of record creation or approval")
    confidenceScore: float = Field(..., ge=0.0, le=1.0, description="Confidence rating between 0 and 1")
    verifiedStatus: str = Field(default="CRYPTOGRAPHICALLY_VERIFIED")

class GraphNode(BaseModel):
    id: str
    label: str
    category: str = Field(..., description="project | country | ministry | tech | policy | discrepancy")
    subType: Optional[str] = None
    region: Optional[str] = None
    sector: Optional[str] = None
    financingAmountM: Optional[float] = None
    organization: Optional[str] = None
    provenance: W3CProvenance
    metadata: Optional[Dict[str, Any]] = None
    icon: Optional[str] = None
    fill: Optional[str] = None
    cluster: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str
    financingAmountM: Optional[float] = None
    provenanceRef: Optional[str] = None
    fill: Optional[str] = None
    size: Optional[float] = None

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

class AppraisalRating(BaseModel):
    environmentalRisk: str
    implementationProgress: str
    disbursedPercentage: float

class MetricsDiff(BaseModel):
    appraisalTargetBeneficiaries: int
    completionActualBeneficiaries: int
    variancePercentage: float
    icrAuditStatus: str

class WbgDocument(BaseModel):
    id: str
    docId: str
    projectTitle: str
    country: str
    region: str
    sector: str
    instrument: str
    commitmentUSD: float
    approvalDate: str
    closingDate: str
    status: str
    sha256Hash: str
    pdfUrl: str
    appraisalRating: AppraisalRating
    metricsDiff: Optional[MetricsDiff] = None

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
