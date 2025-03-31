from types_boto3_dynamodb import DynamoDBClient

from src import context
from src.storage import CloudStorage


@context.inject
def get_document(document_id: str, database: DynamoDBClient = None, cloud_storage: CloudStorage = None):
    pass
