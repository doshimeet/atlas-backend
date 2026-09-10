"""
Legacy semantica module backward compatibility bridge.
Redirects imports to app.services.semantica.
"""
from app.services.semantica import (
    compile_knowledge_graph,
    extract_semantica_triplets,
    get_node_icon,
    build_provenance,
    svg_to_data_uri,
    ICON_MAP,
)

__all__ = [
    "compile_knowledge_graph",
    "extract_semantica_triplets",
    "get_node_icon",
    "build_provenance",
    "svg_to_data_uri",
    "ICON_MAP",
]
