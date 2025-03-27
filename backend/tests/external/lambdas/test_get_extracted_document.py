import pytest

from src.external.lambdas.get_extracted_document import lambda_handler

# pytest.fixtures is used to generalize tests that use the same data


@pytest.fixture
def mock_s3_client(mocker):
    return mocker.MagicMock()


def test_upload_with_injected_client(mock_s3_client):
    event = {"action": "upload", "bucket": "mock-bucket", "key": "mock-key", "content": "mock-content"}

    mock_s3_client.put_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    response = lambda_handler(event, None, s3_client=mock_s3_client)

    assert response["status"] == "success"
    mock_s3_client.put_object.assert_called_once_with(Bucket="mock-bucket", Key="mock-key", Body="mock-content")
