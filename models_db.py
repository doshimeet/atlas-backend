"""
Legacy models_db module backward compatibility bridge.
Redirects imports to app.models.
"""
from app.db.base import Base
from app.models import (
    DBKnowledgeAsset,
    DBDocumentChunk,
    DBGraphEntity,
    DBGraphRelationship,
    DBSemanticTriplet,
    DBIngestionManifest,
)

__all__ = [
    "Base",
    "DBKnowledgeAsset",
    "DBDocumentChunk",
    "DBGraphEntity",
    "DBGraphRelationship",
    "DBSemanticTriplet",
    "DBIngestionManifest",
]
