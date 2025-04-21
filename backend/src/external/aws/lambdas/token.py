import datetime
import json
import logging
import os

import bcrypt
import boto3
import jwt

# Use AWS secrets
client = boto3.client("secretsmanager")
ENVIRONMENT = os.environ["ENVIRONMENT"]
SECRET_KEY = client.get_secret_value(SecretId=f"document-extractor-{ENVIRONMENT}-private-key")["SecretString"]
ALGORITHM = "RS512"


def lambda_handler(event, context):
    if "body" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No credentials provided"}),
        }
    body = json.loads(event["body"])
    # AWS Secret Manager User Credentials
    try:
        username = body["username"]
        password = body["password"]

        stored_username = client.get_secret_value(SecretId=f"document-extractor-{ENVIRONMENT}-username")["SecretString"]
        stored_password = client.get_secret_value(SecretId=f"document-extractor-{ENVIRONMENT}-password")["SecretString"]
    except Exception as e:
        exception_message = "Failed to retrieve the secrets"
        logging.error(exception_message)
        logging.exception(e)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }

    # AWS Secret Manager to hold one user credential
    if username != stored_username or not bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
        return {"statusCode": 401, "body": json.dumps({"error": "Invalid credentials"})}

    # Create JWT token
    try:
        payload = {"sub": username, "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        exception_message = "Failed to generate token"
        logging.error(exception_message)
        logging.exception(e)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }

    return {"statusCode": 200, "body": json.dumps({"access_token": token, "token_type": "bearer"})}
