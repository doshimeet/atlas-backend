from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models import (
    DBKnowledgeAsset,
    DBDocumentChunk,
    DBSemanticTriplet,
)

router = APIRouter()

@router.get("/documents")
def get_knowledge_assets(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """
    Returns all pre-processed research publications and policy working papers.
    """
    assets = db.query(DBKnowledgeAsset).order_by(DBKnowledgeAsset.created_at.desc()).all()
    return [a.to_dict() for a in assets]

@router.get("/documents/{asset_or_doc_id}/insights")
def get_document_insights(asset_or_doc_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Returns granular document chunks, empirical findings, and W3C PROV-O triplets
    with exact page citations for a specific publication.
    """
    clean_id = asset_or_doc_id.replace("ASSET_", "").replace("PROJ_", "").replace("PUB_", "")
    asset = db.query(DBKnowledgeAsset).filter(
        (DBKnowledgeAsset.id == f"PUB_{clean_id}") |
        (DBKnowledgeAsset.id == f"ASSET_{clean_id}") |
        (DBKnowledgeAsset.project_id == clean_id) |
        (DBKnowledgeAsset.id == asset_or_doc_id)
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail=f"Publication {asset_or_doc_id} not found in database.")

    chunks = db.query(DBDocumentChunk).filter_by(asset_id=asset.id).order_by(DBDocumentChunk.chunk_index).all()
    triplets = db.query(DBSemanticTriplet).filter_by(asset_id=asset.id).all()

    return {
        "asset": asset.to_dict(),
        "chunks": [c.to_dict() for c in chunks],
        "triplets": [t.to_dict() for t in triplets],
        "totalSections": len(chunks),
        "totalTriplets": len(triplets),
    }
