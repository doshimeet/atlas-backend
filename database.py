"""
Legacy database module backward compatibility bridge.
Redirects imports to app.db.
"""
from app.db.session import engine, SessionLocal, init_db, get_db
from app.db.base import Base
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

__all__ = ["engine", "SessionLocal", "init_db", "get_db", "Base", "DATABASE_URL"]
