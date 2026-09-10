from datetime import datetime
from typing import Dict, Any
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.db.base import Base

class DBKnowledgeAsset(Base):
    """
    Ingests any document, publication, project dossier, or evaluation report.
    Single Source of Truth with W3C PROV-O cryptographic digests.
    """
    __tablename__ = "knowledge_assets"

    id = Column(String(64), primary_key=True)
    title = Column(String(512), nullable=False)
    doc_type = Column(String(128), default="Project Appraisal Document")
    country = Column(String(128), default="Global")
    region = Column(String(128), default="Global Multilateral Facility")
    sector = Column(String(128), default="Cross-Sectoral")
    project_id = Column(String(64), index=True, nullable=True)
    commitment_usd = Column(Float, default=0.0)
    disclosure_date = Column(String(32), default="")
    closing_date = Column(String(32), default="")
    status = Column(String(64), default="Active")
    abstract = Column(Text, nullable=True)
    pdf_url = Column(String(1024), nullable=True)
    local_pdf_path = Column(String(512), nullable=True)
    sha256_hash = Column(String(64), index=True, nullable=False)
    prov_activity = Column(String(128), default="W3C-PROV-INGESTION")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    chunks = relationship("DBDocumentChunk", back_populates="asset", cascade="all, delete-orphan")
    triplets = relationship("DBSemanticTriplet", back_populates="asset", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "docType": self.doc_type,
            "country": self.country,
            "region": self.region,
            "sector": self.sector,
            "projectId": self.project_id,
            "commitmentUSD": self.commitment_usd,
            "disclosureDate": self.disclosure_date,
            "closingDate": self.closing_date,
            "status": self.status,
            "abstract": self.abstract,
            "pdfUrl": self.pdf_url,
            "sha256Hash": self.sha256_hash,
            "provActivity": self.prov_activity,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }

class DBDocumentChunk(Base):
    """
    Granular parsed structural chunks (sections, tables, legal annexes) with exact page citations.
    """
    __tablename__ = "document_chunks"

    id = Column(String(64), primary_key=True)
    asset_id = Column(String(64), ForeignKey("knowledge_assets.id"), index=True, nullable=False)
    chunk_index = Column(Integer, default=0)
    section_title = Column(String(256), default="")
    page_number = Column(Integer, default=1)
    chunk_type = Column(String(32), default="text")  # text, table, covenant
    content = Column(Text, nullable=False)

    asset = relationship("DBKnowledgeAsset", back_populates="chunks")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "assetId": self.asset_id,
            "chunkIndex": self.chunk_index,
            "sectionTitle": self.section_title,
            "pageNumber": self.page_number,
            "chunkType": self.chunk_type,
            "content": self.content,
        }
