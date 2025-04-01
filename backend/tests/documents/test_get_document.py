from unittest import mock

from src import context
from src.database.database import Database
from src.documents import get_document

context = context.ApplicationContext()


def setup_function():
    context.reset()


def test_get_document_no_document_exists():
    mock_database = mock.MagicMock()
    mock_database.get_document.return_value = None
    context.register(Database, mock_database)

    document_info, storage_access_url, document_data = get_document.get_document("document ID of wonder")

    assert document_info is None
    assert storage_access_url is None
    assert document_data is None


# def test_extract_text_with_no_form_identified():
#     mock_cloud_storage = mock.MagicMock()
#     mock_cloud_storage.file_exists_and_allowed_to_access.return_value = True
#     context.register(CloudStorage, mock_cloud_storage)
#
#     mock_ocr = mock.MagicMock()
#     mock_ocr.extract_raw_text.return_value = ["Don't", "put", "any", "identifying", "words", "here"]
#     mock_ocr.scan.return_value = {
#         "example key": {
#             "value": "example value",
#             "confidence": 1.0,
#         },
#     }
#     context.register(Ocr, mock_ocr)
#
#     mock_queue = mock.MagicMock()
#     context.register(SQSClient, mock_queue)
#
#     extract_text.extract_text("httpssss://a_sweet/file/location.txt", "https://asdf/queue/url")
#
#     mock_ocr.scan.assert_called_with(mock.ANY, queries=None)
#     args, kwargs = mock_queue.send_message.call_args
#     assert """"document_type": null""" in kwargs["MessageBody"]
