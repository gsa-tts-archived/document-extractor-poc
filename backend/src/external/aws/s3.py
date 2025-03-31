from urllib import parse

import boto3
from types_boto3_s3 import S3Client

from src.storage import CloudStorage


class S3(CloudStorage):
    def __init__(self) -> None:
        self.s3_client: S3Client = boto3.client("s3")

    @staticmethod
    def parse_s3_url(s3_url: str) -> tuple[str, str]:
        parsed_url = parse.urlparse(s3_url)

        if parsed_url.scheme != "s3":
            raise ValueError(f"Invalid S3 URL scheme: {parsed_url.scheme}. Expected 's3'.")

        bucket_name: str = parsed_url.netloc
        object_key: str = parsed_url.path.lstrip("/")

        if not bucket_name or not object_key:
            raise ValueError("Invalid S3 URL format. Expected 's3://bucket-name/key'.")

        return bucket_name, object_key

    def file_exists_and_allowed_to_access(self, remote_url: str) -> bool:
        bucket_name, object_key = self.parse_s3_url(remote_url)

        try:
            self.s3_client.head_object(Bucket=bucket_name, Key=object_key)
        except Exception as e:
            print(f"Failed to retrieve S3 object metadata, file doesn't exist or not allowed to access: {e}")
            return False

        return True

    def access_url(self, remote_url: str) -> str:
        bucket_name, object_key = self.parse_s3_url(remote_url)
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=3600,  # URL expires in 1 hour
        )

    def get_file(self, remote_url: str) -> bytes:
        bucket_name, object_key = self.parse_s3_url(remote_url)
        s3_object = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
        return s3_object["Body"].read()
