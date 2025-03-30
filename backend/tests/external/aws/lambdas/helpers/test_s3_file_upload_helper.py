import base64
from unittest import mock

from src import context
from src.external.aws.lambdas.helpers.s3_file_upload_helper import generate_file_data, upload_to_s3
from src.storage import CloudStorage

context = context.ApplicationContext()


def setup_function():
    context.reset()


# Cleanup
def teardown_function():
    context.reset()


# I have a developers itch of our put_object not returning anything.
# If I refactor generate_file_id_and_upload_to_s3 into two separate functions,
# this may be easier to test. I.E generate_file_id(body) and upload_to_s3(contents_from_generate_file_id)
def test_generating_file_data_with_generate_file_id():
    mock_file_content = b"Hello, this is a test file."
    encoded_content = base64.b64encode(mock_file_content).decode("utf-8")
    body = {
        "file_name": "mock_file",
        "file_content": encoded_content,
    }

    response = generate_file_data(body)

    assert response.get("secure_filename") is not None
    assert response.get("original_filename") == "mock_file"
    assert response.get("decoded_file_data") is not None
    assert response.get("document_id") is not None


def test_upload_to_s3():
    file_data = {
        "secure_filename": "secure_filename",
        "original_filename": "original_filename",
        "decoded_file_data": "decoded_file_data",
        "document_id": "document_id",
    }
    mock_cloud_storage = mock.MagicMock()
    mock_cloud_storage.put_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    context.register(CloudStorage, mock_cloud_storage)

    upload_to_s3(file_data)

    mock_cloud_storage.assert_called_once()
