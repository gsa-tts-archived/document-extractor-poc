import json
import os
from decimal import Decimal

import boto3

sqs_client = boto3.client("sqs")
dynamodb_client = boto3.resource("dynamodb")

TABLE_NAME = os.environ["DYNAMODB_TABLE"]
SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]

table = dynamodb_client.Table(TABLE_NAME)


def lambda_handler(event, context):
    """
    Lambda function to read messages from SQS, process the extracted document data,
    and store it in DynamoDB.
    """
    for record in event["Records"]:
        try:
            message_body = json.loads(record["body"])

            document_id = convert_document_key_to_id(message_body.get("document_key"))
            document_key = message_body.get("document_key", "Unknown")
            document_type = message_body.get("document_type", "Unknown")
            extracted_data = message_body.get("extracted_data", {})

            # Convert floats to Decimal for DynamoDB
            extracted_data = convert_floats_to_decimal(extracted_data)

            item_to_store = {
                "document_id": document_id,
                "document_key": document_key,
                "document_type": document_type,
            }

            if extracted_data:
                item_to_store["extracted_data"] = extracted_data

                # Store only non-empty data
                table.put_item(Item=item_to_store)

                # Delete processed message from SQS
                sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=record["receiptHandle"])

                print(f"✅ Successfully processed and stored document {document_id}")
            else:
                print(f"⚠️ No data to store for document {document_id}")

        except Exception as e:
            print(f"❌ Error processing document: {str(e)}")

    return {"statusCode": 200, "body": json.dumps("Processing complete")}


def convert_floats_to_decimal(data):
    """Recursively converts float values in a dictionary to Decimal for DynamoDB compatibility."""
    if isinstance(data, dict):
        return {k: convert_floats_to_decimal(v) for k, v in data.items() if v}
    elif isinstance(data, list):
        return [convert_floats_to_decimal(i) for i in data if i]
    elif isinstance(data, float):  # Convert only floats
        return Decimal(str(data))
    return data


def convert_document_key_to_id(document_key: str):
    """Converts the key in the form of `input/asdf.jgp` and returns `asdf`."""
    base = os.path.basename(document_key)
    return os.path.splitext(base)[0]
