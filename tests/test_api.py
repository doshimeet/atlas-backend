import pytest

@pytest.mark.anyio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert data["database"]["knowledgeAssets"] >= 0

@pytest.mark.anyio
async def test_api_graph(client):
    response = await client.get("/api/graph")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
    assert isinstance(data["nodes"], list)
    assert isinstance(data["edges"], list)

@pytest.mark.anyio
async def test_api_documents(client):
    response = await client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.anyio
async def test_api_snapshot(client):
    response = await client.get("/api/snapshot")
    assert response.status_code == 200
    data = response.json()
    assert "totalPublications" in data
    assert "thematicDomainsCount" in data
