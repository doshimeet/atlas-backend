from fastapi import APIRouter
from app.schemas.ingest import ExtractionRequest, ExtractionResponse
from app.services.semantica import extract_semantica_triplets

router = APIRouter()

@router.post("/extract", response_model=ExtractionResponse)
def extract_triplets(payload: ExtractionRequest) -> ExtractionResponse:
    """
    Extracts high-fidelity W3C PROV-O semantic triplets from raw document text.
    """
    return extract_semantica_triplets(
        text=payload.document_text,
        doc_id=payload.doc_id or "PAD-UPLOAD",
        country=payload.country or "Global"
    )
