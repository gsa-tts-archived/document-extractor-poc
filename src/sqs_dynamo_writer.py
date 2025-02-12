import boto3
import json
import os
import uuid

# AWS clients
sqs_client = boto3.client('sqs')
dynamodb_client = boto3.resource('dynamodb')

# Environment variables
TABLE_NAME = os.environ['DYNAMODB_TABLE']
SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']

# Reference to the DynamoDB table
table = dynamodb_client.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Lambda function to read messages from SQS, process the extracted document data,
    and store it in DynamoDB.
    """
    for record in event['Records']:
        try:
            message_body = json.loads(record['body'])

            document_id = str(uuid.uuid4())  # Generate a unique ID
            document_key = message_body.get('document_key', 'Unknown')
            document_type = message_body.get('document_type', 'Unknown')
            extracted_data = message_body.get('extracted_data', {})

            table.put_item(Item={
                'document_id': document_id,
                'document_key': document_key,
                'document_type': document_type,
                'extracted_data': extracted_data
            })

            sqs_client.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=record['receiptHandle']
            )

            print(f"✅ Successfully processed and stored document {document_id}")

        except Exception as e:
            print(f"❌ Error processing document: {str(e)}")

    return {'statusCode': 200, 'body': json.dumps('Processing complete')}
