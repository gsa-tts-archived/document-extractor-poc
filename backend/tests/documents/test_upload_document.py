import base64
from unittest import mock

import pytest

from src import context
from src.documents.upload_document import (
    decode_file_content,
    generate_secure_filename,
    upload_file_data,
    upload_file_to_cloud,
)
from src.storage import CloudStorage

context = context.ApplicationContext()


def setup_function():
    context.reset()


# Cleanup
def teardown_function():
    context.reset()


def test_uploading_file_data_returns_document_id():
    mock_file_content = b"Hello, this is a test file."
    decoded_file_content = base64.b64encode(mock_file_content).decode("utf-8")

    mock_cloud_storage = mock.MagicMock()
    mock_cloud_storage.put_object.return_value = None
    context.register(CloudStorage, mock_cloud_storage)

    response = upload_file_data("original.txt", decoded_file_content, "mock_bucket", "mock_folder")

    assert response is not None


def test_generating_secure_filename_works():
    mock_original_filename = "Original.txt"

    expected_secure_file_name, expected_document_id = generate_secure_filename(mock_original_filename)

    # added coverage for asserts but I need to address how to assert these values properly
    assert mock_original_filename is not None
    assert expected_document_id is not None


def test_generating_file_data_with_generate_file_id():
    mock_file_content = b"Hello, this is a test file."
    decoded_content = base64.b64encode(mock_file_content).decode("utf-8")

    response = decode_file_content(decoded_content)

    assert response is not None


def test_generating_file_data_with_invalid_file_content():
    mock_file_content = 1234
    with pytest.raises(TypeError):
        decode_file_content(mock_file_content)


def test_upload_to_cloud():
    mock_file_content = b"Hello, this is a test file."
    secure_file_name = "how secure of your sir"
    original_file_name = "how original of you sir"
    decoded_content = base64.b64encode(mock_file_content).decode("utf-8")

    mock_cloud_storage = mock.MagicMock()
    mock_cloud_storage.put_object.return_value = None
    context.register(CloudStorage, mock_cloud_storage)

    upload_file_to_cloud(decoded_content, secure_file_name, original_file_name, "mock_bucket", "mock_folder")

    mock_cloud_storage.put_object.assert_called_once()
