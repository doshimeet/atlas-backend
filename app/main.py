import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.db.session import init_db, SessionLocal
from app.models import DBKnowledgeAsset
from app.services.ingest_service import HybridSemanticaIngestionWorker
from app.api.v1.api_router import api_router
from app.api.v1.endpoints.health import router as root_health_router

setup_logging()
logger = get_logger("api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    db = SessionLocal()
    try:
        count = db.query(DBKnowledgeAsset).count()
        logger.info(f"Atlas Knowledge Engine active. Pre-processed Research Assets in DB: {count}")
        if count == 0:
            logger.info("Database is empty. Triggering autonomous zero-touch bootstrap ingestion...")
            worker = HybridSemanticaIngestionWorker()
            asyncio.create_task(worker.ingest_live_publications_batch(rows=settings.DEFAULT_BOOTSTRAP_ROWS))
    finally:
        db.close()
    
    yield
    # Shutdown logic if needed
    logger.info("Atlas Knowledge Engine shutting down.")

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS Configuration
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Root health endpoint (accessible at /health)
    application.include_router(root_health_router)

    # API v1 routes (accessible at /api/...)
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
