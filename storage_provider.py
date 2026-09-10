"""
Legacy storage_provider module backward compatibility bridge.
Redirects imports to app.integrations.storage.
"""
from app.integrations.storage import (
    StorageProvider,
    LocalStorageProvider,
    AzureADLSGen2Provider,
    get_storage_provider,
)

__all__ = [
    "StorageProvider",
    "LocalStorageProvider",
    "AzureADLSGen2Provider",
    "get_storage_provider",
]
