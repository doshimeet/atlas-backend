import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "Atlas Knowledge - World Bank Group Publications & Research Engine"
    PROJECT_DESCRIPTION: str = "Enterprise Multi-Modal Operational Knowledge Engine with Zero-Mock WDS Publications Ingestion"
    VERSION: str = "3.2.0"
    API_V1_STR: str = "/api"

    # Database
    DATABASE_URL: str = "sqlite:///./data/atlas_knowledge.db"

    # Storage
    STORAGE_PROVIDER: str = "local"  # local | azure
    LAKEHOUSE_DIR: str = "./data/lakehouse"

    # Azure ADLS Gen2 (optional in production)
    AZURE_STORAGE_ACCOUNT: str = "atlaslakehouse"
    AZURE_STORAGE_CONTAINER: str = "wbg-knowledge-lakehouse"
    AZURE_TENANT_ID: str = ""
    AZURE_CLIENT_ID: str = ""
    AZURE_CLIENT_SECRET: str = ""

    # Document Parser
    PARSER_PROVIDER: str = "local"  # local | azure

    # World Bank WDS API
    WBG_API_BASE_URL: str = "https://search.worldbank.org/api/v2/wds"
    DEFAULT_BOOTSTRAP_ROWS: int = 15

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

settings = Settings()
