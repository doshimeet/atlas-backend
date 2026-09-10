from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.logging import get_logger
from app.db.base import Base

logger = get_logger("database")

database_url = settings.DATABASE_URL

if database_url.startswith("sqlite"):
    db_path = database_url.replace("sqlite:///", "")
    parent_dir = Path(db_path).parent
    parent_dir.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    engine = create_engine(
        database_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=1800,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
    """
    Initializes database tables idempotently.
    """
    try:
        # Import models so they are registered with Base metadata
        import app.models  # noqa: F401
        Base.metadata.create_all(bind=engine)
        logger.info(f"Database initialized successfully at {database_url}")
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
