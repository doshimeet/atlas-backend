"""
Legacy wbg_client module backward compatibility bridge.
Redirects imports to app.integrations.wbg_client.
"""
from app.integrations.wbg_client import (
    fetch_live_wbg_publications,
    classify_thematic_practice,
    THEMATIC_PRACTICES,
)

__all__ = [
    "fetch_live_wbg_publications",
    "classify_thematic_practice",
    "THEMATIC_PRACTICES",
]
