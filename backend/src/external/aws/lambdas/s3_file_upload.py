import json

from helpers.s3_file_upload_helper import generate_file_data, upload_to_s3


def lambda_handler(event, context):
    try:
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No file provided"}),
            }

        body = json.loads(event["body"])
        try:
            file_data = generate_file_data(body)
            upload_to_s3(file_data)
        except Exception as e:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": str(e)}),
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File uploaded successfully.", "documentId": file_data["document_id"]}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
