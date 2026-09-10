"""
Legacy models module backward compatibility bridge.
Redirects imports to app.schemas.
"""
from app.schemas import (
    W3CProvenance,
    GraphNode,
    GraphEdge,
    GraphData,
    AppraisalRating,
    MetricsDiff,
    WbgDocument,
    ExtractionRequest,
    SemanticTriplet,
    ExtractionResponse,
)

__all__ = [
    "W3CProvenance",
    "GraphNode",
    "GraphEdge",
    "GraphData",
    "AppraisalRating",
    "MetricsDiff",
    "WbgDocument",
    "ExtractionRequest",
    "SemanticTriplet",
    "ExtractionResponse",
]
