from typing import Any
from urllib import parse

import boto3

from src.ocr import Ocr, OcrException


class Textract(Ocr):
    def __init__(self) -> None:
        self.textract_client = boto3.client("textract")

    def detect_document_type(self, s3_url: str) -> str | None:
        try:
            bucket_name, object_key = self._parse_s3_url(s3_url)

            response = self.textract_client.detect_document_text(
                Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}}
            )

            document_type = None

            for block in response.get("Blocks", []):
                if block.get("BlockType") != "WORD" and block.get("BlockType") != "LINE":
                    continue

                if block.get("Text") == "W-2":
                    document_type = "W2"
                    break
                elif block.get("Text") == "1099-NEC":
                    document_type = "1099-NEC"
                    break
                elif block.get("Text").startswith("DD FORM 214"):
                    document_type = "DD214"
                    break

        except Exception as e:
            raise OcrException(f"Failure while trying to detect the document type of {s3_url}") from e

        return document_type

    def _parse_s3_url(self, s3_url: str) -> tuple[str, str]:
        parsed_url = parse.urlparse(s3_url)

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
            print("Attempting AnalyzeDocument (Structured Mode)...")
            response = self.textract_client.analyze_document(
                Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
                FeatureTypes=["FORMS", "TABLES"],
            )
            extracted_data = self._parse_textract_analyze_document_response(response)

            # Check if AnalyzeDocument works
            if not extracted_data:
                print("AnalyzeDocument yielded no data. Falling back to DetectDocumentText...")
                response = self.textract_client.detect_document_text(
                    Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}}
                )
                extracted_data = self._parse_ocr_response(response)

            return extracted_data

        except Exception as e:
            raise OcrException(f"Unable to OCR the image {s3_url}") from e

    def _parse_textract_analyze_document_response(self, response):
        """Parses structured data from AnalyzeDocument response into a simple key-value format."""
        extracted_data = {}
        block_map = {block["Id"]: block for block in response.get("Blocks", [])}

        # Extract form data
        for block in response.get("Blocks", []):
            if block["BlockType"] == "KEY_VALUE_SET" and "KEY" in block.get("EntityTypes", []):
                key_text, key_conf = self._get_text_from_block(block, block_map)
                value_text = ""
                for rel in block.get("Relationships", []):
                    if rel["Type"] == "VALUE":
                        for value_id in rel["Ids"]:
                            value_block = block_map.get(value_id)
                            if value_block:
                                value_text, value_conf = self._get_text_from_block(value_block, block_map)
                if key_text:
                    extracted_data[key_text] = {"value": value_text, "confidence": key_conf}

        return extracted_data

    def _get_text_from_block(self, block, block_map):
        """Helper to extract text from a block."""
        text = ""
        confidence = block.get("Confidence", 0.0)
        if "Relationships" in block:
            for rel in block["Relationships"]:
                if rel["Type"] == "CHILD":
                    for child_id in rel["Ids"]:
                        word_block = block_map.get(child_id)
                        if word_block and word_block.get("Text"):
                            text += word_block["Text"] + " "
        return text.strip(), confidence

    def _parse_ocr_response(self, response):
        """Parses text from DetectDocumentText response with pseudo-keys based on content."""
        extracted_data = {}
        line_count = 1

        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                line_text = block.get("DetectedText", "")
                confidence = block.get("Confidence", 0.0)

                # Generate a key based on the first 3 words
                words = line_text.split()[:3]
                key = "_".join(words).replace(":", "").replace(".", "").strip() or f"Line_{line_count}"

                # Ensure key uniqueness
                while key in extracted_data:
                    key += f"_{line_count}"

                extracted_data[key] = {"value": line_text, "confidence": confidence}
                line_count += 1

        return extracted_data
