"""
Legacy data module backward compatibility bridge.
Redirects imports to app.data.dossiers.
"""
from app.data.dossiers import VERIFIED_PROJECT_DOSSIERS

__all__ = ["VERIFIED_PROJECT_DOSSIERS"]
