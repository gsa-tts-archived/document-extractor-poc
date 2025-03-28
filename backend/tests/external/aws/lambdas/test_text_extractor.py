from aws_lambda_typing import events

from src import context
from src.external.aws.lambdas import text_extractor

context = context.ApplicationContext()


def setup_function():
    context.reset()


def test_text_extractor():
    test_bucket_name = "DogCow"
    test_file_key = "Moof.txt"

    lambda_response = text_extractor.lambda_handler(_test_s3_event(test_bucket_name, test_file_key), None)
    assert lambda_response["statusCode"] == 200


def _test_s3_event(bucket_name: str, file_key: str) -> events.S3Event:
    return {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": bucket_name,
                    },
                    "object": {
                        "key": file_key,
                    },
                },
            }
        ],
    }
