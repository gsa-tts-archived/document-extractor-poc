import base64
import json
import os
from datetime import UTC, datetime
from hashlib import sha256

import boto3

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "ocr-poc-flex")
DEFAULT_FOLDER = "input/"


def generate_secure_filename(original_filename):
    """
    Generate a secure filename while preserving extension and adding uniqueness.
    """
    ext = os.path.splitext(original_filename)[1].lower() if "." in original_filename else ""

    timestamp = datetime.now(UTC).isoformat()
    unique_string = f"{original_filename}{timestamp}".encode()

    file_hash = sha256(unique_string).hexdigest()[:12]  # Using first 12 chars for brevity

    return f"{file_hash}{ext}", file_hash


def lambda_handler(event, context):
    try:
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No file provided"}),
            }

        body = json.loads(event["body"])

        if not all(k in body for k in ["file_content", "file_name"]):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"}),
            }

        try:
            file_data = base64.b64decode(body["file_content"])
        except Exception:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid file content encoding"}),
            }

        original_filename = body["file_name"]
        secure_filename, document_id = generate_secure_filename(original_filename)

        s3_key = f"{DEFAULT_FOLDER}{secure_filename}"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_data,
            Metadata={"original_filename": original_filename},
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File uploaded successfully.", "documentId": document_id}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
