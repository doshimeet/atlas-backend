from typing import List, Optional, Dict, Any
from pydantic import BaseModel

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

class DocumentChunkResponse(BaseModel):
    id: str
    assetId: str
    chunkIndex: int
    sectionTitle: str
    pageNumber: int
    chunkType: str
    content: str

class DocumentInsightsResponse(BaseModel):
    asset: Dict[str, Any]
    chunks: List[Dict[str, Any]]
    triplets: List[Dict[str, Any]]
    totalSections: int
    totalTriplets: int
