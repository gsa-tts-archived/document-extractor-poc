import asyncio
import os
import statistics
from typing import Any

import boto3
import iterator_chain
from types_boto3_textract import TextractClient

from src.external.aws.s3 import S3
from src.forms.form import Form
from src.ocr import Ocr, OcrException


class Textract(Ocr):
    def __init__(self) -> None:
        self.textract_client: TextractClient = boto3.client("textract")

    def scan(self, s3_url: str, form: Form) -> dict[str, dict[str, str | float]]:
        try:
            # Parse the S3 URL
            bucket_name, object_key = S3.parse_s3_url(s3_url)

            if form.queries() is None or len(form.queries()) == 0:
                print("Attempting AnalyzeDocument with forms and tables")
                response = self.textract_client.analyze_document(
                    Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
                    FeatureTypes=["FORMS"],
                )
                print("Parsing result")
                extracted_data = self._parse_textract_forms(response)
            else:
                print("Attempting AnalyzeDocument with queries")
                response_list = asyncio.run(self._paginated_textract_with_queries(form, bucket_name, object_key))
                print("Parsing result")
                extracted_data = (
                    iterator_chain.from_iterable(response_list)
                    .map(self._parse_textract_queries)
                    .reduce(lambda a_dict, b_dict: {**a_dict, **b_dict}, initial={})
                )

            return extracted_data

        except Exception as e:
            raise OcrException(f"Unable to OCR the image {s3_url}") from e

    def extract_raw_text(self, s3_url: str) -> list[str]:
        try:
            bucket_name, object_key = S3.parse_s3_url(s3_url)

            response = self.textract_client.detect_document_text(
                Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}}
            )

            return (
                iterator_chain.from_iterable(response.get("Blocks", []))
                .filter(lambda block: block["BlockType"] == "LINE")
                .filter(lambda block: "Text" in block)
                .map(lambda block: block["Text"])
                .list()
            )

        except Exception as e:
            raise OcrException(f"Failure while trying to detect the document type of {s3_url}") from e

    def _split_list_by_30(self, the_list: list[Any]) -> list[list[Any]]:
        sublist_size = 30
        return [the_list[i : i + sublist_size] for i in range(0, len(the_list), sublist_size)]

    async def _paginated_textract_with_queries(self, form, bucket_name, object_key) -> list[Any]:
        queries_config = [{"Text": query, "Pages": ["*"]} for query in form.queries()]
        paginated_queries_config = self._split_list_by_30(queries_config)

        tasks = [
            asyncio.create_task(
                self._call_textract_with_queries(
                    bucket_name,
                    object_key,
                    sub_queries_config,
                    os.environ.get(f"TEXTRACT_ADAPTER_ID_{form.identifier()}_{index}"),
                )
            )
            for index, sub_queries_config in enumerate(paginated_queries_config, start=0)
        ]
        results_list = await asyncio.gather(*tasks)

        return results_list

    def get_latest_adapter_version(self, adapter_id):
        response = self.textract_client.list_adapter_versions(AdapterId=adapter_id)
        adapter_versions = response["AdapterVersions"]
        if not adapter_versions:
            raise ValueError("No versions found for the specified adapter.")
        # Sort versions by CreationTime in descending order to get the latest version first
        latest_version = max(adapter_versions, key=lambda x: x["CreationTime"])
        return latest_version["AdapterVersion"]

    async def _call_textract_with_queries(self, bucket_name, object_key, queries_config, adapter_id):
        print("Initiating document analysis")
        if adapter_id is not None:
            initiate_response = self.textract_client.start_document_analysis(
                DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
                FeatureTypes=["QUERIES"],
                QueriesConfig={"Queries": queries_config},
                AdaptersConfig={
                    "Adapters": [
                        {
                            "AdapterId": adapter_id,
                            "Pages": ["*"],
                            "Version": self.get_latest_adapter_version(adapter_id),
                        }
                    ]
                },
            )
        else:
            # Can't seem to set `AdaptersConfig` to `None` if the size of `adapters_config` is 0.  Best thing to do is
            # just not pass it in.
            initiate_response = self.textract_client.start_document_analysis(
                DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
                FeatureTypes=["QUERIES"],
                QueriesConfig={"Queries": queries_config},
            )
        job_id = initiate_response["JobId"]
        response = self.textract_client.get_document_analysis(JobId=job_id)
        while response["JobStatus"] == "IN_PROGRESS":
            await asyncio.sleep(1)
            print(f"Checking if job {job_id} is complete")
            response = self.textract_client.get_document_analysis(JobId=job_id)

        print(f"Completed document analysis for job {job_id}")
        return response

    def _parse_textract_queries(self, textract_response):
        extracted_data = {}

        print(f"Attempting to extract block data from response: {textract_response}")

        blocks = textract_response.get("Blocks", [])
        query_blocks = []
        query_result_blocks = {}

        for block in blocks:
            print(f"Extracting block data: {block}")
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
