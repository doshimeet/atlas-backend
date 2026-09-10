import httpx
import hashlib
import re
import time
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("atlas.wbg_client")

# Thematic practice classification keywords
THEMATIC_PRACTICES = {
    "THEME_CLIMATE": {
        "name": "Climate Action & Green Transition",
        "keywords": ["climate", "environment", "energy", "solar", "water", "flood", "adaptation", "biodiversity", "emission"],
        "color": "#10b981",
    },
    "THEME_DIGITAL": {
        "name": "Digital Economy & Infrastructure",
        "keywords": ["digital", "telecom", "ict", "broadband", "cyber", "technology", "artificial intelligence", "data"],
        "color": "#06b6d4",
    },
    "THEME_HUMAN": {
        "name": "Human Capital & Social Resilience",
        "keywords": ["gender", "poverty", "health", "education", "social", "labor", "employment", "welfare", "worker", "school"],
        "color": "#8b5cf6",
    },
    "THEME_MACRO": {
        "name": "Macroeconomics, Trade & Finance",
        "keywords": ["trade", "finance", "firm", "enterprise", "state", "fiscal", "economic", "market", "investment", "credit"],
        "color": "#f59e0b",
    },
}

def classify_thematic_practice(paper_dict: Dict[str, Any]) -> tuple:
    """
    Classifies a World Bank research publication into one of the 4 flagship Global Practices.
    Returns: (theme_id, theme_name, theme_color)
    """
    text_corpus = " ".join([
        paper_dict.get("docna", {}).get("0", {}).get("docna", ""),
        str(paper_dict.get("theme", "")),
        str(paper_dict.get("subsc", "")),
        str(paper_dict.get("topic", "")),
        str(paper_dict.get("prdln", "")),
    ]).lower()

    for theme_id, meta in THEMATIC_PRACTICES.items():
        if any(kw in text_corpus for kw in meta["keywords"]):
            return theme_id, meta["name"], meta["color"]

    return "THEME_MACRO", THEMATIC_PRACTICES["THEME_MACRO"]["name"], THEMATIC_PRACTICES["THEME_MACRO"]["color"]

async def fetch_live_wbg_publications(rows: int = 15, query: str = "") -> List[Dict[str, Any]]:
    """
    Queries the official World Bank Documents & Reports (WDS) API
    for live Policy Research Working Papers and Flagship Research Publications.
    """
    base_url = "https://search.worldbank.org/api/v2/wds"
    params = {
        "format": "json",
        "rows": str(rows),
        "docty": "Policy Research Working Paper",
    }
    if query:
        params["qterm"] = query

    headers = {
        "User-Agent": "AtlasKnowledge-ResearchEngine/3.0 (World Bank Open Knowledge Repository)",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
        try:
            resp = await client.get(base_url, params=params)
            if resp.status_code != 200:
                logger.error(f"WDS API responded with status {resp.status_code}")
                return []

            data = resp.json()
            documents_map = data.get("documents", {})
            valid_papers = []
            for doc_key, doc_val in documents_map.items():
                if doc_key == "facets" or not isinstance(doc_val, dict):
                    continue
                # Must have title and pdfurl
                title_obj = doc_val.get("docna", {}).get("0", {}) if isinstance(doc_val.get("docna"), dict) else {}
                title = title_obj.get("docna", "").replace("\n", " ").strip() if isinstance(title_obj, dict) else str(doc_val.get("docna", "")).replace("\n", " ").strip()
                pdf_url = doc_val.get("pdfurl")

                if title and pdf_url:
                    doc_val["clean_title"] = title
                    theme_id, theme_name, theme_color = classify_thematic_practice(doc_val)
                    doc_val["thematic_id"] = theme_id
                    doc_val["thematic_name"] = theme_name
                    doc_val["thematic_color"] = theme_color
                    valid_papers.append(doc_val)

            logger.info(f"Successfully retrieved {len(valid_papers)} live publications from WDS API.")
            return valid_papers
        except Exception as e:
            logger.error(f"Failed to query live WDS API: {e}")
            return []
