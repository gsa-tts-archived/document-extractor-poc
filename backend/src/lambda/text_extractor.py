import json
import os

import boto3

from src.external.ocr.tesseract import Tesseract

s3_client = boto3.client("s3")
textract_client = boto3.client("textract")
sqs_client = boto3.client("sqs")

SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]


def lambda_handler(event, context):
    record = event["Records"][0]
    bucket_name = record["s3"]["bucket"]["name"]
    document_key = record["s3"]["object"]["key"]

    print(f"Processing file: s3://{bucket_name}/{document_key}")

    try:
        metadata = s3_client.head_object(Bucket=bucket_name, Key=document_key)
        print("S3 Metadata Retrieved Successfully:")
        print(metadata)

    except Exception as e:
        print(f"Failed to retrieve S3 object metadata: {e}")
        return {
            "statusCode": 403,
            "body": json.dumps(
                "Failed to access S3 object. Check permissions or other issues with file or configurations."
            ),
        }

    try:
        tesseract = Tesseract()
        extracted_data = tesseract.scan(f"s3://{bucket_name}/{document_key}")
    except Exception as e:
        exception_message = f"Failed to extract text from S3 object s3://{bucket_name}/{document_key}: {e}"
        print(exception_message)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }

    print(f"Extracted Data: {json.dumps(extracted_data, indent=2)}")

    # Send extracted data to SQS
    try:
        sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(
                {
                    "document_key": document_key,
                    "extracted_data": extracted_data,
                }
            ),
        )
        print("Message sent to SQS successfully.")
    except Exception as sqs_error:
        print(f"Failed to send message to SQS: {sqs_error}")

    return {
        "statusCode": 200,
        "body": json.dumps("Document processed successfully and sent to SQS"),
    }


def parse_textract_response(response):
    """Parses structured data from AnalyzeDocument response into a simple key-value format."""
    extracted_data = {}
    block_map = {block["Id"]: block for block in response.get("Blocks", [])}

    # Extract form data
    for block in response.get("Blocks", []):
        if block["BlockType"] == "KEY_VALUE_SET" and "KEY" in block.get("EntityTypes", []):
            key_text, key_conf = get_text_from_block(block, block_map)
            value_text = ""
            for rel in block.get("Relationships", []):
                if rel["Type"] == "VALUE":
                    for value_id in rel["Ids"]:
                        value_block = block_map.get(value_id)
                        if value_block:
                            value_text, value_conf = get_text_from_block(value_block, block_map)
            if key_text:
                extracted_data[key_text] = {"value": value_text, "confidence": key_conf}

    return extracted_data


def parse_ocr_response(response):
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


def get_text_from_block(block, block_map):
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
