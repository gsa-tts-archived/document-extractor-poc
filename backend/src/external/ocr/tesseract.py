import io
import os
import sys
from typing import Any
from urllib.parse import urlparse

import boto3
import tesserocr
from botocore.exceptions import ClientError
from PIL import Image

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

from src.external.ocr import Ocr  # Import the interface we defined earlier


class Tesseract(Ocr):
    """
    Implementation of S3ScannerInterface that performs OCR on images stored in S3.
    """

    def __init__(self) -> None:
        """
        Initialize the OCR Scanner with AWS credentials and tesseract settings.

        Args:
            aws_access_key_id: AWS access key ID
            aws_secret_access_key: AWS secret access key
            region_name: AWS region name
            language: Tesseract language code (default: 'eng')
        """
        self.s3_client = boto3.client("s3")

        # Initialize tesserocr API
        self.api = tesserocr.PyTessBaseAPI(path="/opt/homebrew/share/tessdata")

    def _parse_s3_url(self, s3_url: str) -> tuple[str, str]:
        """
        Parse an S3 URL into bucket name and object key.

        Args:
            s3_url: The S3 URL to parse

        Returns:
            Tuple of (bucket_name, object_key)

        Raises:
            ValueError: If the URL format is invalid
        """
        parsed_url = urlparse(s3_url)

        if parsed_url.scheme != "s3":
            raise ValueError(f"Invalid S3 URL scheme: {parsed_url.scheme}. Expected 's3'.")

        bucket_name: str = parsed_url.netloc
        object_key: str = parsed_url.path.lstrip("/")

        if not bucket_name or not object_key:
            raise ValueError("Invalid S3 URL format. Expected 's3://bucket-name/key'.")

        return bucket_name, object_key

    def scan(self, s3_url: str) -> dict[str, Any]:
        """
        Download an image from S3 and perform OCR on it.

        Args:
            s3_url: The S3 URL of the image to scan

        Returns:
            Dictionary containing OCR results and metadata
        """
        try:
            # Parse the S3 URL
            bucket_name, object_key = self._parse_s3_url(s3_url)

            # Get object metadata
            response = self.s3_client.head_object(Bucket=bucket_name, Key=object_key)

            # Check if the object is an image
            content_type = response.get("ContentType", "")
            if not content_type.startswith("image/"):
                return {
                    "success": False,
                    "error": f"Object is not an image. Content type: {content_type}",
                    "metadata": {
                        "bucket": bucket_name,
                        "key": object_key,
                        "size": response.get("ContentLength", 0),
                        "last_modified": response.get("LastModified"),
                        "content_type": content_type,
                    },
                }

            # Download the image
            print(f"Downloading image from {s3_url}")
            file_obj = io.BytesIO()
            self.s3_client.download_fileobj(Bucket=bucket_name, Key=object_key, Fileobj=file_obj)
            file_obj.seek(0)

            # Open the image with PIL
            image = Image.open(file_obj)

            # Perform OCR
            print(f"Performing OCR on image from {s3_url}")
            self.api.SetImage(image)
            ocr_text = self.api.GetUTF8Text()
            confidence = self.api.MeanTextConf()

            boxes = self.api.GetComponentImages(tesserocr.RIL.BLOCK, True)
            print(f"Found {len(boxes)} textline image components.")
            for i, (im, box, _, _) in enumerate(boxes):
                # im is a PIL image object
                # box is a dict with x, y, w and h keys
                self.api.SetRectangle(box["x"], box["y"], box["w"], box["h"])
                ocrResult = self.api.GetUTF8Text()
                conf = self.api.MeanTextConf()
                print(
                    "Box[{0}]: x={x}, y={y}, w={w}, h={h}, confidence: {1}, text: {2}".format(i, conf, ocrResult, **box)
                )

            # Return the OCR results and metadata
            return {
                "success": True,
                "text": ocr_text.strip(),
                "confidence": confidence,
                "metadata": {
                    "bucket": bucket_name,
                    "key": object_key,
                    "size": response.get("ContentLength", 0),
                    "last_modified": response.get("LastModified"),
                    "content_type": content_type,
                    "image_size": f"{image.width}x{image.height}",
                    "image_format": image.format,
                    "image_mode": image.mode,
                },
            }

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code == "404":
                print(f"Object not found: {s3_url}")
                return {"success": False, "error": "Object not found"}
            elif error_code == "403":
                print(f"Access denied to object: {s3_url}")
                return {"success": False, "error": "Access denied"}
            else:
                print(f"Error scanning S3 URL: {e}")
                return {"success": False, "error": str(e)}

        except Exception as e:
            print(f"Unexpected error scanning S3 URL: {e}")
            return {"success": False, "error": str(e)}

    def __del__(self):
        """Clean up the Tesseract API when the object is destroyed."""
        self.api.End()


if __name__ == "__main__":
    # Example usage
    scanner = Tesseract()

    # Scan a single image
    result = scanner.scan("s3://document-extractor-gsa-dev-documents/test_ws.jpg")
    if result["success"]:
        print(f"OCR Text: {result['text']}")
        print(f"Confidence: {result['confidence']}%")
    else:
        print(f"Error: {result['error']}")
