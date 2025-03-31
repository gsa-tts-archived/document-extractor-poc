import os
from decimal import Decimal
from typing import Any

import boto3
from boto3.dynamodb.types import TypeDeserializer
from types_boto3_dynamodb import DynamoDBClient

from src.database.database import Database


class DynamoDb(Database):
    def __init__(self) -> None:
        self.dynamodb_client: DynamoDBClient = boto3.client("dynamodb")
        self.table = os.getenv("DYNAMODB_TABLE")
        self.deserializer = TypeDeserializer()

    def get_document(self, document_id: str) -> dict[str, Any] | None:
        dynamodb_item = self.dynamodb_client.get_item(TableName=self.table, Key={"document_id": {"S": document_id}})

        if "Item" not in dynamodb_item:
            return None

        return self._unmarshal_dynamodb_json(dynamodb_item["Item"])

    def _unmarshal_dynamodb_json(self, dynamodb_data: dict[str, Any]) -> dict[str, Any]:
        """Converts DynamoDB JSON format to standard JSON using TypeDeserializer and handles Decimals."""
        deserialized_data = {k: self.deserializer.deserialize(v) for k, v in dynamodb_data.items()}
        # return self._convert_decimal(deserialized_data)
        return deserialized_data

    def _convert_decimal(self, value):
        """Recursively converts Decimal to float."""
        if isinstance(value, Decimal):
            return int(value) if value % 1 == 0 else float(value)
        elif isinstance(value, list):
            return [self._convert_decimal(v) for v in value]
        elif isinstance(value, dict):
            return {k: self._convert_decimal(v) for k, v in value.items()}
        return value
