import base64
import os
import uuid

import boto3

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "ocr-poc-flex")
DEFAULT_FOLDER = "input/"


def generate_secure_filename(original_filename):
    """
    Generate a secure filename while preserving extension and adding uniqueness.
    """
    ext = os.path.splitext(original_filename)[1].lower() if "." in original_filename else ""

    document_id = str(uuid.uuid4())

    return f"{document_id}{ext}", document_id


# This method is doing two things
# Generates a Unique ID for the document name - another method that returns file name and id (generate_file_identifiers)
# Uploading a file into S3 - potential method (upload_to_s3)
# returns a unique document identifier
# I feel like we can split this helper into two methods that s3_file_upload calls for better clarity, thoughts?
def generate_file_id_and_upload_to_s3(body):
    if not all(k in body for k in ["file_content", "file_name"]):
        raise Exception("Missing required fields")

    try:
        file_data = base64.b64decode(body["file_content"])
    except Exception as err:
        raise Exception("Invalid file content encoding") from err

    original_filename = body["file_name"]
    secure_filename, document_id = generate_secure_filename(original_filename)

    s3_key = f"{DEFAULT_FOLDER}{secure_filename}"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=file_data,
        Metadata={"original_filename": original_filename},
    )

    return document_id
