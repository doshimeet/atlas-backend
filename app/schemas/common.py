from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class W3CProvenance(BaseModel):
    wasGeneratedBy: str = Field(..., description="Entity or Board authority that generated the record")
    wasDerivedFrom: str = Field(..., description="Source document URI or official portal link")
    documentSha256: str = Field(..., description="Cryptographic SHA-256 digest")
    provActivity: str = Field(..., description="W3C PROV-O Activity identifier")
    timestamp: str = Field(..., description="ISO timestamp of record creation or approval")
    confidenceScore: float = Field(..., ge=0.0, le=1.0, description="Confidence rating between 0 and 1")
    verifiedStatus: str = Field(default="CRYPTOGRAPHICALLY_VERIFIED")

class DatabaseMetrics(BaseModel):
    knowledgeAssets: int
    graphEntities: int
    graphRelationships: int
    semanticTriplets: int
    servingLatency: str

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    repository: str
    database: DatabaseMetrics
    standards: List[str]

class SnapshotResponse(BaseModel):
    totalPublications: int
    thematicDomainsCount: int
    thematicDomains: List[str]
    countriesAnalyzed: int
    verifiedPercentage: float
    dataMode: str
    cacheStatus: str
