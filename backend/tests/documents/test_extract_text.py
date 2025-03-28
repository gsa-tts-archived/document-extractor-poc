from unittest.mock import MagicMock

import pytest

from src import context
from src.documents import extract_text
from src.storage import CloudStorage

context = context.ApplicationContext()


def setup_function():
    context.reset()


def test_extract_text_bad_file():
    mock_cloud_storage = MagicMock()
    mock_cloud_storage.file_exists_and_allowed_to_access.return_value = False
    context.register(CloudStorage, mock_cloud_storage)

    with pytest.raises(FileNotFoundError):
        extract_text.extract_text("httpssss://a_sweet/file/location.txt", "https://asdf/queue/url")


# def test_extract_text():
#     mock_cloud_storage = MagicMock()
#     mock_cloud_storage.file_exists_and_allowed_to_access.return_value = True
#     context.register(CloudStorage, mock_cloud_storage)
#
#     test_remote_file_url = "httpssss://a_sweet/file/location.txt"
#     test_queue_url = "https://asdf/queue/url"
#
#     extract_text.extract_text(test_remote_file_url, test_queue_url)
