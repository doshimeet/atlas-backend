import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("storage")

class StorageProvider(ABC):
    """
    Abstract file storage interface supporting local filesystem and Azure ADLS Gen2.
    """
    @abstractmethod
    async def save_file(self, relative_path: str, content: bytes) -> str:
        """Saves file and returns internal URI or local path."""
        pass

    @abstractmethod
    async def get_file(self, relative_path: str) -> Optional[bytes]:
        """Retrieves raw file bytes."""
        pass

    @abstractmethod
    async def exists(self, relative_path: str) -> bool:
        """Checks if file exists in the storage repository."""
        pass

    @abstractmethod
    def get_url(self, relative_path: str) -> str:
        """Returns direct downloadable URL or local file path."""
        pass


class LocalStorageProvider(StorageProvider):
    """
    Local Lakehouse filesystem implementation for development.
    Stores files in configured lakehouse directory.
    """
    def __init__(self, base_dir: Optional[str] = None):
        target_dir = base_dir or settings.LAKEHOUSE_DIR
        self.base_dir = Path(target_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        # Ensure standard lakehouse subdirectories exist
        (self.base_dir / "raw_pdfs").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "parsed_layouts").mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, relative_path: str) -> Path:
        return self.base_dir / relative_path.lstrip("/")

    async def save_file(self, relative_path: str, content: bytes) -> str:
        file_path = self._resolve_path(relative_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(content)
        logger.info(f"Saved local lakehouse file: {file_path}")
        return str(file_path)

    async def get_file(self, relative_path: str) -> Optional[bytes]:
        file_path = self._resolve_path(relative_path)
        if not file_path.exists():
            return None
        with open(file_path, "rb") as f:
            return f.read()

    async def exists(self, relative_path: str) -> bool:
        return self._resolve_path(relative_path).exists()

    def get_url(self, relative_path: str) -> str:
        return str(self._resolve_path(relative_path))


class AzureADLSGen2Provider(StorageProvider):
    """
    Enterprise Azure Data Lake Storage Gen2 provider.
    Authenticates via Azure Entra ID Client Credentials (or DefaultAzureCredential).
    """
    def __init__(self):
        self.account_name = settings.AZURE_STORAGE_ACCOUNT
        self.file_system = settings.AZURE_STORAGE_CONTAINER
        self.tenant_id = settings.AZURE_TENANT_ID
        self.client_id = settings.AZURE_CLIENT_ID
        self.client_secret = settings.AZURE_CLIENT_SECRET
        self._client = None

    def _get_service_client(self):
        if self._client is None:
            try:
                from azure.identity import ClientSecretCredential, DefaultAzureCredential
                from azure.storage.filedatalake import DataLakeServiceClient

                if self.tenant_id and self.client_id and self.client_secret:
                    credential = ClientSecretCredential(
                        tenant_id=self.tenant_id,
                        client_id=self.client_id,
                        client_secret=self.client_secret,
                    )
                else:
                    credential = DefaultAzureCredential()

                account_url = f"https://{self.account_name}.dfs.core.windows.net"
                self._client = DataLakeServiceClient(account_url, credential=credential)
            except Exception as e:
                logger.error(f"Failed to initialize Azure ADLS Gen2 client: {e}")
                raise
        return self._client

    async def save_file(self, relative_path: str, content: bytes) -> str:
        service_client = self._get_service_client()
        fs_client = service_client.get_file_system_client(self.file_system)
        file_client = fs_client.get_file_client(relative_path)
        file_client.upload_data(content, overwrite=True)
        return f"https://{self.account_name}.dfs.core.windows.net/{self.file_system}/{relative_path}"

    async def get_file(self, relative_path: str) -> Optional[bytes]:
        service_client = self._get_service_client()
        fs_client = service_client.get_file_system_client(self.file_system)
        file_client = fs_client.get_file_client(relative_path)
        try:
            download = file_client.download_file()
            return download.readall()
        except Exception:
            return None

    async def exists(self, relative_path: str) -> bool:
        service_client = self._get_service_client()
        fs_client = service_client.get_file_system_client(self.file_system)
        file_client = fs_client.get_file_client(relative_path)
        try:
            file_client.get_file_properties()
            return True
        except Exception:
            return False

    def get_url(self, relative_path: str) -> str:
        return f"https://{self.account_name}.blob.core.windows.net/{self.file_system}/{relative_path}"


def get_storage_provider() -> StorageProvider:
    """
    Factory creating the active storage provider based on configuration.
    """
    provider_type = settings.STORAGE_PROVIDER.lower()
    if provider_type in ["azure", "azure_adls_gen2", "adls"]:
        return AzureADLSGen2Provider()
    return LocalStorageProvider()
