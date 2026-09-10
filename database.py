import os
import logging
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models_db import Base

logger = logging.getLogger("atlas.database")

def get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "sqlite:///./data/atlas_knowledge.db")
    return url

DATABASE_URL = get_database_url()

# Ensure local data directory exists for SQLite
if DATABASE_URL.startswith("sqlite"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    parent_dir = Path(db_path).parent
    parent_dir.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    # Enterprise Azure SQL / PostgreSQL Connection Pool
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=1800,  # recycle connections before Azure serverless idle timeout
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
    """
    Initializes database tables idempotently across SQLite and Azure SQL.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info(f"Database initialized successfully at {DATABASE_URL}")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency delivering thread-safe database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
