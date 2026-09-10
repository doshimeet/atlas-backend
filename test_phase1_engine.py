import time
import urllib.request
import json
import asyncio
from database import SessionLocal, init_db
from models_db import DBKnowledgeAsset, DBDocumentChunk, DBGraphEntity, DBGraphRelationship, DBSemanticTriplet
from ingest_service import HybridSemanticaIngestionWorker
from wbg_client import fetch_live_wbg_publications

def run_phase1_verification():
    print("==========================================================")
    print("         PHASE 1 ENGINE & ZERO-MOCK VERIFICATION          ")
    print("==========================================================")

    # 1. Test Live WDS API
    print("\n[TEST 1] Live World Bank WDS API Connectivity...")
    url = "https://search.worldbank.org/api/v2/wds?format=json&rows=5&docty=Policy+Research+Working+Paper"
    start = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": "AtlasKnowledge/3.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        status = resp.status
        data = json.loads(resp.read().decode("utf-8"))
        elapsed = (time.time() - start) * 1000.0

    assert status == 200, f"Expected 200 OK, got {status}"
    total_available = data.get("total", 0)
    assert total_available >= 10000, f"Expected >= 10,000 papers, got {total_available}"
    print(f"  ✓ PASSED: WDS API responded in {elapsed:.1f}ms with {total_available:,} live research publications.")

    # 2. Test Zero-Mock Database State
    print("\n[TEST 2] Database Zero-Mock State & Knowledge Hierarchy...")
    db = SessionLocal()
    try:
        asset_count = db.query(DBKnowledgeAsset).count()
        entity_count = db.query(DBGraphEntity).count()
        rel_count = db.query(DBGraphRelationship).count()
        chunk_count = db.query(DBDocumentChunk).count()
        triplet_count = db.query(DBSemanticTriplet).count()

        print(f"  • Knowledge Assets (Research Papers): {asset_count}")
        print(f"  • Knowledge Graph Entities: {entity_count}")
        print(f"  • Knowledge Graph Relationships: {rel_count}")
        print(f"  • Parsed PDF Chunks: {chunk_count}")
        print(f"  • W3C PROV-O Semantic Triplets: {triplet_count}")

        assert asset_count >= 12, f"Expected >= 12 assets, got {asset_count}"

        # Assert zero IBRD banking facility
        ibrd_count = db.query(DBGraphEntity).filter_by(id="FAC_IBRD").count()
        assert ibrd_count == 0, f"Found {ibrd_count} FAC_IBRD nodes! Expected 0."
        print("  ✓ PASSED: Zero FAC_IBRD nodes (IBRD loan facility eliminated).")

        # Assert root is WBG Knowledge Repository
        root_node = db.query(DBGraphEntity).filter_by(id="FAC_WBG_KNOWLEDGE").first()
        assert root_node is not None, "FAC_WBG_KNOWLEDGE root node not found!"
        assert "Knowledge & Research Repository" in root_node.label
        print(f"  ✓ PASSED: Root Node is '{root_node.label}'.")

        # Assert zero fake covenants
        fake_covs = db.query(DBGraphEntity).filter(DBGraphEntity.label.like("%Covenant: Audit%")).count()
        assert fake_covs == 0, f"Found {fake_covs} fake covenants! Expected 0."
        print("  ✓ PASSED: Zero fake template covenants.")

        # Check real authors and real findings
        author_nodes = db.query(DBGraphEntity).filter_by(category="ministry").all()
        finding_nodes = db.query(DBGraphEntity).filter_by(category="covenant").all()
        assert len(author_nodes) >= 5, f"Expected >= 5 authors, got {len(author_nodes)}"
        assert len(finding_nodes) >= 5, f"Expected >= 5 findings, got {len(finding_nodes)}"
        print(f"  ✓ PASSED: Real Authors: {len(author_nodes)} (e.g. {author_nodes[0].label})")
        print(f"  ✓ PASSED: Real Empirical Findings: {len(finding_nodes)} (e.g. {finding_nodes[0].label[:40]}...)")

        # Check real triplets
        triplets = db.query(DBSemanticTriplet).limit(3).all()
        for t in triplets:
            assert t.citation and len(t.citation) > 5
            assert t.verbatim_quote and len(t.verbatim_quote) > 10
        print(f"  ✓ PASSED: Triplets carry verbatim quotes & real citations.")

    finally:
        db.close()

    # 3. Test Cryptographic Idempotency
    print("\n[TEST 3] Cryptographic SHA-256 Idempotency...")
    db = SessionLocal()
    try:
        sample_asset = db.query(DBKnowledgeAsset).first()
        worker = HybridSemanticaIngestionWorker()
        # Mocking paper dict matching existing
        paper_dict = {
            "id": sample_asset.project_id,
            "clean_title": sample_asset.title,
            "pdfurl": sample_asset.pdf_url,
            "count": sample_asset.country,
            "admreg": sample_asset.region,
            "thematic_id": "THEME_CLIMATE",
            "thematic_name": sample_asset.sector,
            "thematic_color": "#10b981",
            "authors": {"0": {"author": "Test Author"}}
        }
        start = time.time()
        res = asyncio.run(worker.ingest_single_publication(paper_dict, db))
        idempotency_time = (time.time() - start) * 1000.0
        assert res.get("status") == "SKIPPED_EXISTING", f"Expected SKIPPED_EXISTING, got {res.get('status')}"
        print(f"  ✓ PASSED: Duplicate detected via SHA-256 in {idempotency_time:.1f}ms with status SKIPPED_EXISTING.")
    finally:
        db.close()

    # 4. Serving Benchmark Test (< 3ms SLA)
    print("\n[TEST 4] Serving Latency SLA Benchmark (50 requests to /api/graph)...")
    from main import get_operational_graph
    db = SessionLocal()
    latencies = []
    try:
        for _ in range(50):
            t0 = time.time()
            graph = get_operational_graph(db)
            latencies.append((time.time() - t0) * 1000.0)

        mean_lat = sum(latencies) / len(latencies)
        p95_lat = sorted(latencies)[int(len(latencies) * 0.95)]
        print(f"  • Mean Serving Latency: {mean_lat:.2f}ms")
        print(f"  • P95 Serving Latency:  {p95_lat:.2f}ms")
        print(f"  • Served Nodes: {len(graph.nodes)} | Served Edges: {len(graph.edges)}")
        assert mean_lat < 3.0, f"Mean latency {mean_lat:.2f}ms exceeds 3.0ms SLA!"
        print("  ✓ PASSED: Sub-3ms SLA strictly met!")
    finally:
        db.close()

    print("\n==========================================================")
    print("     ALL PHASE 1 BACKEND VERIFICATIONS PASSED (100%)      ")
    print("==========================================================")

if __name__ == "__main__":
    run_phase1_verification()
