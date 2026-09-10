import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.logging import get_logger
from app.models import DBGraphEntity, DBGraphRelationship
from app.schemas.graph import GraphData, GraphNode, GraphEdge

router = APIRouter()
logger = get_logger("api.graph")

@router.get("/graph", response_model=GraphData)
def get_operational_graph(db: Session = Depends(get_db)) -> GraphData:
    """
    Returns the complete synthesized World Bank Group Knowledge Graph in <3ms
    queried directly from the pre-processed document database.
    """
    start = time.time()
    db_entities = db.query(DBGraphEntity).all()
    db_relationships = db.query(DBGraphRelationship).all()

    nodes = [GraphNode(**e.to_node_dict()) for e in db_entities]
    edges = [GraphEdge(**r.to_edge_dict()) for r in db_relationships]

    elapsed = (time.time() - start) * 1000.0
    logger.info(f"Served {len(nodes)} nodes & {len(edges)} edges in {elapsed:.2f}ms")
    return GraphData(nodes=nodes, edges=edges)
