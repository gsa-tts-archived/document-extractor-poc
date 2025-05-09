import os
from urllib import parse

from src import context
from src.database.database import Database


@context.inject
def write_document(document_id: str, document_url: str, database: Database = None):
    document_to_store = {
        "document_id": document_id,
        "document_url": document_url,
        "status": "processing",
    }

    database.write_document(document_to_store)


@context.inject
def update_document(document_url: str, document_type: str | None, extracted_data: dict, database: Database = None):
    document_id = convert_document_url_to_id(document_url)

    document_to_store = {
        "document_id": document_id,
        "document_url": document_url,
        "document_type": document_type,
        "extracted_data": extracted_data,
        "status": "complete",
    }

    database.write_document(document_to_store)


def convert_document_url_to_id(document_url: str):
    parsed_url = parse.urlparse(document_url)
    document_key = parsed_url.path
    base = os.path.basename(document_key)
    return os.path.splitext(base)[0]
