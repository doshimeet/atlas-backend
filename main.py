"""
Root Entrypoint for Atlas Knowledge Backend.
Maintains 100% backward compatibility for processes running `uvicorn main:app`.
The production application logic is encapsulated inside `app.main`.
"""
from app.main import app, create_application

# Re-export commonly imported legacy symbols for root backward compatibility
from app.db.session import get_db, init_db, SessionLocal
from app.models import (
    DBKnowledgeAsset,
    DBDocumentChunk,
    DBGraphEntity,
    DBGraphRelationship,
    DBSemanticTriplet,
    DBIngestionManifest,
)
from app.schemas.graph import GraphData, GraphNode, GraphEdge
from app.services.ingest_service import HybridSemanticaIngestionWorker

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
