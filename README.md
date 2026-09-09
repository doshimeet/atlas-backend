# Atlas Knowledge - Standalone Python Backend

Dedicated FastAPI and Semantica backend service for the **Atlas Knowledge** platform.

## Architecture

- **Framework:** FastAPI / Uvicorn (Python 3.11+)
- **Data Models:** Pydantic v2
- **Provenance Standard:** W3C PROV-O (`wasGeneratedBy`, `wasDerivedFrom`, `documentSha256`)
- **Port:** `8000`

## Endpoints

- `GET /health`: Service health and capability check
- `GET /api/graph`: Returns the full 360° World Bank Group operational knowledge graph
- `GET /api/documents`: Returns verified project dossiers, approval records, and PAD URLs
- `GET /api/snapshot`: Institutional portfolio commitments and metrics
- `POST /api/extract`: Semantica natural language triplet extraction pipeline

## Running the Backend

```bash
cd "/Users/meetketankumardoshi/AI at Scale/atlas-backend"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
