from src import context
from src.documents import extract_text
from src.storage import CloudStorage

context = context.ApplicationContext()


def setup_function():
    context.reset()


def test_extract_text():
    context.register(CloudStorage, "lol")

    test_remote_file_url = "httpssss://a_sweet/file/location.txt"
    test_queue_url = "https://asdf/queue/url"

    lambda_response = extract_text.extract_text(test_remote_file_url, test_queue_url)
    assert lambda_response["statusCode"] == 200
