import json
import logging
import os

import boto3
from types_boto3_sqs import SQSClient

from src.context import ApplicationContext
from src.database.database import Database
from src.documents import write_document
from src.external.aws.dynamodb import DynamoDb

sqs_queue_url = os.environ["SQS_QUEUE_URL"]

appContext = ApplicationContext()
appContext.register(Database, DynamoDb())
appContext.register(SQSClient, boto3.client("sqs"))


def lambda_handler(event, context):
    failure = False
    exception_message = "An internal error happened while trying to save a document to the database"

    for record in event["Records"]:
        try:
            message_body = json.loads(record["body"])

            document_url = message_body["document_url"]
            document_type = message_body.get("document_type")
            extracted_data = message_body.get("extracted_data", {})

            write_document.write_document(document_url, document_type, extracted_data)

            sqs_client = appContext.implementation(SQSClient)
            sqs_client.delete_message(QueueUrl=sqs_queue_url, ReceiptHandle=record["receiptHandle"])
        except Exception as e:
            logging.error(exception_message)
            logging.exception(e)
            failure = True

    if failure:
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }

    return {
        "statusCode": 200,
        "body": json.dumps("Processing complete"),
    }
