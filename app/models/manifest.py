from datetime import datetime
from typing import Dict, Any
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
)
from app.db.base import Base

class DBIngestionManifest(Base):
    """
    Tracks asynchronous ETL ingestion status with audit trail and heartbeat recovery.
    """
    __tablename__ = "ingestion_manifest"

    id = Column(String(64), primary_key=True)
    asset_id = Column(String(64), index=True, nullable=False)
    status = Column(String(32), default="PENDING")  # PENDING, ACQUIRING, PARSING, EXTRACTING, COMMITTED, FAILED
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "assetId": self.asset_id,
            "status": self.status,
            "errorMessage": self.error_message,
            "startedAt": self.started_at.isoformat() if self.started_at else None,
            "completedAt": self.completed_at.isoformat() if self.completed_at else None,
        }
