import statistics
from typing import Any
from urllib import parse

import boto3

from src.ocr import Ocr, OcrException


class Textract(Ocr):
    def __init__(self) -> None:
        self.textract_client = boto3.client("textract")

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
                    FeatureTypes=["FORMS"],
                )
                print("Parsing result")
                extracted_data = self._parse_textract_forms(response)
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

    def _parse_textract_forms(self, response):
        """Parses structured data from AnalyzeDocument response into a simple key-value format."""
        extracted_data = {}
        block_map = {block["Id"]: block for block in response.get("Blocks", [])}

        for block in response.get("Blocks", []):
            if block["BlockType"] != "KEY_VALUE_SET" or "KEY" not in block.get("EntityTypes", []):
                continue

            key_text, key_confidence = self._get_text_and_confidence_from_relationship_blocks(block, block_map, "CHILD")

            relationships = block.get("Relationships", [])

            value_texts = []
            value_confidences = []

            for relationship in relationships:
                if relationship["Type"] != "VALUE":
                    continue

                for related_value_block_id in relationship["Ids"]:
                    value_block = block_map[related_value_block_id]
                    value_text, value_confidence = self._get_text_and_confidence_from_relationship_blocks(
                        value_block, block_map, "CHILD"
                    )

                    if value_text != "":
                        value_texts.append(value_text)
                        value_confidences.append(value_confidence)

            confidence = -1
            if len(value_texts) > 0:
                confidence = statistics.fmean(value_confidences)
            extracted_data[key_text] = {"value": " ".join(value_texts), "confidence": confidence}

        return extracted_data

    def _get_text_and_confidence_from_relationship_blocks(
        self, block: Any, blocks: dict[str, Any], wanted_relationship: str
    ) -> tuple[str, float]:
        relationships = block.get("Relationships", [])

        texts = []
        confidences = []

        for relationship in relationships:
            if relationship["Type"] != wanted_relationship:
                continue

            related_blocks = [blocks[related_block_id] for related_block_id in relationship.get("Ids", [])]

            relation_texts = []
            relation_confidences = []

            for related_block in related_blocks:
                if "Text" not in related_block:
                    continue

                relation_texts.append(related_block["Text"])
                relation_confidences.append(related_block["Confidence"])

            if len(relation_texts) > 0:
                relation_text = " ".join(relation_texts)
                texts.append(relation_text)

                relation_confidence = statistics.fmean(relation_confidences)
                confidences.append(relation_confidence)

        confidence = -1
        if len(confidences) > 0:
            confidence = statistics.fmean(confidences)

        return " ".join(texts), confidence
