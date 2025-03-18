import statistics
from typing import Any
from urllib import parse

import boto3
import botocore

from src.ocr import Ocr, OcrException


class Textract(Ocr):
    def __init__(self) -> None:
        try:
            self.textract_client = boto3.client("textract")
        except botocore.exceptions.NoRegionError:
            self.textract_client = boto3.client("textract", region_name="us-east-1")

    def _parse_s3_url(self, s3_url: str) -> tuple[str, str]:
        parsed_url = parse.urlparse(s3_url)

        if parsed_url.scheme != "s3":
            raise ValueError(f"Invalid S3 URL scheme: {parsed_url.scheme}. Expected 's3'.")

        bucket_name: str = parsed_url.netloc
        object_key: str = parsed_url.path.lstrip("/")

        if not bucket_name or not object_key:
            raise ValueError("Invalid S3 URL format. Expected 's3://bucket-name/key'.")

        return bucket_name, object_key

    def scan(self, s3_url: str, queries: list[str] | None = None) -> dict[str, dict[str, str | float]]:
        try:
            # Parse the S3 URL
            bucket_name, object_key = self._parse_s3_url(s3_url)

            if queries is None:
                print("Attempting AnalyzeDocument with forms and tables")
                response = self.textract_client.analyze_document(
                    Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
                    FeatureTypes=["FORMS", "TABLES"],
                )
                print("Parsing result")
                extracted_data = self._parse_textract_forms_and_tables(response)
            else:
                print("Attempting AnalyzeDocument with queries")
                queries_config = [{"Text": query, "Pages": ["*"]} for query in queries]
                response = self.textract_client.analyze_document(
                    Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
                    FeatureTypes=["QUERIES"],
                    QueriesConfig={"Queries": queries_config},
                )
                print("Parsing result")
                extracted_data = self._parse_textract_queries(response)

            return extracted_data

        except Exception as e:
            raise OcrException(f"Unable to OCR the image {s3_url}") from e

    def _parse_textract_forms_and_tables(self, response):
        """Parses structured data from AnalyzeDocument response into a simple key-value format."""
        extracted_data = {}
        block_map = {block["Id"]: block for block in response.get("Blocks", [])}

        # Extract form data
        for block in response.get("Blocks", []):
            if block["BlockType"] == "KEY_VALUE_SET" and "KEY" in block.get("EntityTypes", []):
                key_text, key_conf = self._get_text_from_relationship_blocks(block, block_map)
                value_text = ""
                for rel in block.get("Relationships", []):
                    if rel["Type"] == "VALUE":
                        for value_id in rel["Ids"]:
                            value_block = block_map.get(value_id)
                            if value_block:
                                value_text, value_conf = self._get_text_from_relationship_blocks(value_block, block_map)
                if key_text:
                    extracted_data[key_text] = {"value": value_text, "confidence": key_conf}

        return extracted_data

    def _get_text_from_relationship_blocks(self, block, block_map):
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

    def _get_text_and_confidence_from_relationship_blocks(
        self, block: Any, blocks: dict[str, Any], wanted_relationship: str
    ) -> tuple[str, float]:
        relationships = block.get("Relationships", [])

        values = []
        confidences = []

        for relationship in relationships:
            if relationship["Type"] != wanted_relationship:
                continue

            related_query_result_blocks = [
                blocks.get(related_block_id, {}) for related_block_id in relationship.get("Ids", [])
            ]

            relation_value = " ".join(
                [query_result_block["Text"] for query_result_block in related_query_result_blocks]
            )
            values.append(relation_value)

            relation_confidence = statistics.fmean(
                [query_result_block["Confidence"] for query_result_block in related_query_result_blocks]
            )
            confidences.append(relation_confidence)

        return " ".join(values), statistics.fmean(confidences)

    def _parse_textract_queries(self, textract_response):
        extracted_data = {}

        blocks = textract_response.get("Blocks", [])
        query_blocks = []
        query_result_blocks = {}

        for block in blocks:
            if block["BlockType"] == "QUERY":
                query_blocks.append(block)
            elif block["BlockType"] == "QUERY_RESULT":
                query_result_blocks[block["Id"]] = block

        for query_block in query_blocks:
            value, confidence = self._get_text_and_confidence_from_relationship_blocks(
                query_block, query_result_blocks, "ANSWER"
            )

            extracted_data[query_block["Query"]["Text"]] = {"value": value, "confidence": confidence}

        return extracted_data
