import base64
import os
import uuid

from src import context
from src.storage import CloudStorage


@context.inject
def upload_file_data(
    file_name,
    file_content,
    bucket_name,
    default_folder,
    cloud_storage: CloudStorage = None,
) -> str:
    decoded_file_content = decode_file_content(file_content)
    secure_filename, document_id = generate_secure_filename(file_name)

    key = f"{default_folder}{secure_filename}"
    cloud_storage.put_object(bucket_name, key, decoded_file_content, {"original_filename": file_name})

    return document_id


def decode_file_content(file_content) -> bytes:
    try:
        decoded_file_data = base64.b64decode(file_content)
    except Exception as e:
        raise TypeError("Invalid file content encoding") from e
    return decoded_file_data


def generate_secure_filename(original_filename):
    """
    Generate a secure filename while preserving extension and adding uniqueness.
    """
    ext = os.path.splitext(original_filename)[1].lower() if "." in original_filename else ""

    document_id = str(uuid.uuid4())

    return f"{document_id}{ext}", document_id
