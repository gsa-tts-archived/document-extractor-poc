import io
from typing import Any
from urllib.parse import urlparse

import boto3
from paddleocr import PaddleOCR
from PIL import Image

from src.external.ocr import Ocr, OcrException


class Paddle(Ocr):
    def __init__(self) -> None:
        self.s3_client = boto3.client("s3")

        # Initialize tesserocr API
        self.api = PaddleOCR(use_angle_cls=True, lang="en")

    def _parse_s3_url(self, s3_url: str) -> tuple[str, str]:
        parsed_url = urlparse(s3_url)

        if parsed_url.scheme != "s3":
            raise ValueError(f"Invalid S3 URL scheme: {parsed_url.scheme}. Expected 's3'.")

        bucket_name: str = parsed_url.netloc
        object_key: str = parsed_url.path.lstrip("/")

        if not bucket_name or not object_key:
            raise ValueError("Invalid S3 URL format. Expected 's3://bucket-name/key'.")

        return bucket_name, object_key

    def scan(self, s3_url: str) -> dict[str, dict[str, Any]]:
        try:
            # Parse the S3 URL
            bucket_name, object_key = self._parse_s3_url(s3_url)

            # Download the image
            print(f"Downloading image from {s3_url}")
            file_obj = io.BytesIO()
            self.s3_client.download_fileobj(Bucket=bucket_name, Key=object_key, Fileobj=file_obj)
            file_obj.seek(0)

            # Open the image with PIL
            image = Image.open(file_obj)

            # Perform OCR
            print(f"Performing OCR on image from {s3_url}")

            results = {}

            results = self.api.ocr(image)

            return results

        except Exception as e:
            raise OcrException(f"Unable to OCR the image {s3_url}") from e

    def __del__(self):
        self.api.End()
