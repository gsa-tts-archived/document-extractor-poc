import base64
import os
import uuid

import boto3

from src import context
from src.external.aws.s3 import S3
from src.storage import CloudStorage

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "ocr-poc-flex")
DEFAULT_FOLDER = "input/"
appContext = context.ApplicationContext()
appContext.register(CloudStorage, S3())


def generate_secure_filename(original_filename):
    """
    Generate a secure filename while preserving extension and adding uniqueness.
    """
    ext = os.path.splitext(original_filename)[1].lower() if "." in original_filename else ""

    document_id = str(uuid.uuid4())

    return f"{document_id}{ext}", document_id


def generate_file_data(body):
    if not all(k in body for k in ["file_content", "file_name"]):
        raise Exception("Missing required fields")

    try:
        decoded_file_data = base64.b64decode(body["file_content"])
    except Exception as err:
        raise Exception("Invalid file content encoding") from err

    original_filename = body["file_name"]
    secure_filename, document_id = generate_secure_filename(original_filename)
    file_data = {
        "secure_filename": secure_filename,
        "original_filename": original_filename,
        "decoded_file_data": decoded_file_data,
        "document_id": document_id,
    }
    return file_data


def upload_to_s3(file_data: dict):
    s3_key = f"{DEFAULT_FOLDER}{file_data['secure_filename']}"
    put_object(
        BUCKET_NAME, s3_key, file_data["decoded_file_data"], {"original_filename": file_data["original_filename"]}
    )


@context.inject
def put_object(bucket_name, key, body, metadata, cloud_storage: CloudStorage = None):
    return cloud_storage.put_object(bucket_name, key, body, metadata)
