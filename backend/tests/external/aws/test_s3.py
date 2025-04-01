import pytest

from src.external.aws.s3 import S3


def test_parse_s3_url_no_s3_scheme():
    """An exception is raised when the `s3://` is missing."""
    with pytest.raises(ValueError):
        S3.parse_s3_url("https://gsa.gov")


def test_parse_s3_url_no_bucket():
    """An exception is raised when the bucket name is missing."""
    with pytest.raises(ValueError):
        S3.parse_s3_url("s3:///key")


def test_parse_s3_url_no_object_key():
    """An exception is raised when the object key name is missing."""
    with pytest.raises(ValueError):
        S3.parse_s3_url("s3://bucket_name/")


def test_parse_s3_url_works():
    """Everything works as expected."""

    expected_bucket = "bucket_name"
    expected_object_key = "object_folder/object_key"

    actual_bucket, actual_object_key = S3.parse_s3_url(f"s3://{expected_bucket}/{expected_object_key}")

    assert actual_bucket == expected_bucket
    assert actual_object_key == expected_object_key
