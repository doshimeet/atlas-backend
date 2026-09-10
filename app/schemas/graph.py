from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.schemas.common import W3CProvenance

class GraphNode(BaseModel):
    id: str
    label: str
    category: str = Field(..., description="project | country | ministry | tech | policy | discrepancy | asset | institution | pillar | insight")
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
    isPrimaryBackbone: Optional[bool] = True
    evidenceQuote: Optional[str] = None
    pageNumber: Optional[int] = None

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
