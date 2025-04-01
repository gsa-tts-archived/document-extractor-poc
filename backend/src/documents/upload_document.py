import base64
import os
import uuid

from src import context
from src.external.aws.s3 import S3
from src.storage import CloudStorage, CloudStorageException

appContext = context.ApplicationContext()
appContext.register(CloudStorage, S3())


def upload_file_data(body, bucket_name, default_folder) -> str:
    filedata = generate_file_data(body)
    upload_to_s3(filedata, bucket_name, default_folder)
    return filedata.get("document_id")


def generate_file_data(body):
    if not all(k in body for k in ["file_content", "file_name"]):
        raise ValueError("Missing required fields")

    try:
        decoded_file_data = base64.b64decode(body["file_content"])
    except Exception as e:
        raise TypeError("Invalid file content encoding") from e

    original_filename = body["file_name"]
    secure_filename, document_id = generate_secure_filename(original_filename)
    file_data = {
        "secure_filename": secure_filename,
        "original_filename": original_filename,
        "decoded_file_data": decoded_file_data,
        "document_id": document_id,
    }
    return file_data


def generate_secure_filename(original_filename):
    """
    Generate a secure filename while preserving extension and adding uniqueness.
    """
    ext = os.path.splitext(original_filename)[1].lower() if "." in original_filename else ""

    document_id = str(uuid.uuid4())

    return f"{document_id}{ext}", document_id


def upload_to_s3(file_data: dict, bucket_name, default_folder):
    try:
        s3_key = f"{default_folder}{file_data['secure_filename']}"
        put_object(
            bucket_name, s3_key, file_data["decoded_file_data"], {"original_filename": file_data["original_filename"]}
        )
    except CloudStorageException as e:
        raise CloudStorageException() from e


@context.inject
def put_object(bucket_name, key, body, metadata, cloud_storage: CloudStorage = None):
    return cloud_storage.put_object(bucket_name, key, body, metadata)
