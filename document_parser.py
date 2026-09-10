"""
Legacy document_parser module backward compatibility bridge.
Redirects imports to app.services.document_parser.
"""
from app.services.document_parser import (
    ParsedSection,
    ParsedDocument,
    DocumentParserProvider,
    DoclingParserProvider,
    get_document_parser,
)

__all__ = [
    "ParsedSection",
    "ParsedDocument",
    "DocumentParserProvider",
    "DoclingParserProvider",
    "get_document_parser",
]
