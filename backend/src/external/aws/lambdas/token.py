import datetime
import json
import logging
import os

import bcrypt
import boto3
import jwt

client = boto3.client("secretsmanager")
environment = os.environ["ENVIRONMENT"]


def lambda_handler(event, context):
    logging.info("Getting private key from AWS Secrets Manager")
    private_key = client.get_secret_value(SecretId=f"document-extractor-{environment}-private-key")["SecretString"]

    logging.info("Getting username and password from request body")
    try:
        body = json.loads(event["body"])
        username = body["username"]
        password = body["password"]
    except Exception:
        logging.warning("Credentials missing in request body")
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Credentials missing in request body.  Please provide 'username' and 'password'."}
            ),
        }

    try:
        logging.info("Getting username from AWS Secrets Manager")
        stored_username = client.get_secret_value(SecretId=f"document-extractor-{environment}-username")["SecretString"]
        logging.info("Getting password from AWS Secrets Manager")
        stored_password = client.get_secret_value(SecretId=f"document-extractor-{environment}-password")["SecretString"]
    except Exception as e:
        exception_message = "Failed to retrieve the secrets"
        logging.error(exception_message)
        logging.exception(e)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }

    # AWS Secret Manager to hold one user credential
    logging.info("Validating credentials")
    if username != stored_username or not bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
        logging.warning("Invalid credentials")
        return {"statusCode": 401, "body": json.dumps({"error": "Invalid credentials"})}

    # Create JWT token
    try:
        logging.info("Generating JWT")
        payload = {"sub": username, "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)}
        token = jwt.encode(payload, private_key, algorithm="RS512")
    except Exception as e:
        exception_message = "Failed to generate token"
        logging.error(exception_message)
        logging.exception(e)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }

    return {"statusCode": 200, "body": json.dumps({"access_token": token, "token_type": "bearer"})}
