import json
import os

from src.documents.upload_document import upload_file_data


def lambda_handler(event, context):
    try:
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No file provided"}),
            }

        body = json.loads(event["body"])
        try:
            bucket_name = os.environ.get("S3_BUCKET_NAME", "ocr-poc-flex")
            default_folder = "input/"
            document_id = upload_file_data(body, bucket_name, default_folder)
        except Exception as e:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": str(e)}),
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File uploaded successfully.", "documentId": document_id}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
