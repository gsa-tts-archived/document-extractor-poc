from unittest import mock

from src.external.aws.lambdas.helpers.s3_file_upload_helper import upload_to_s3
from src.external.aws.s3 import S3
from src.storage import CloudStorage


class MockResponse:
    @staticmethod
    def put_object():
        return None


def my_function():
    return None


def test_upload_to_s3_with_monkey_patch(monkeypatch):
    file_data = {
        "secure_filename": "secure_filename",
        "original_filename": "original_filename",
        "decoded_file_data": "decoded_file_data",
        "document_id": "document_id",
    }
    mock_put_object = mock.MagicMock(returned_value=None)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(CloudStorage, "put_object", mock_put_object)

    # app.get_json, which contains requests.get, uses the monkeypatch
    upload_to_s3(file_data)

    mock_put_object.assert_called_once()


def test_monkeypatch_no_magicmock(monkeypatch):
    file_data = {
        "secure_filename": "secure_filename",
        "original_filename": "original_filename",
        "decoded_file_data": "decoded_file_data",
        "document_id": "document_id",
    }

    def mock_put_object(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(S3, "put_object", mock_put_object)

    result = upload_to_s3(file_data)
    assert result is None
