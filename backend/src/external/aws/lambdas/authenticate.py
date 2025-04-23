import logging
import os

import boto3
import jwt

client = boto3.client("secretsmanager")
ENVIRONMENT = os.environ["ENVIRONMENT"]


def lambda_handler(event, context):
    logging.info("Getting public key from AWS Secrets Manager")
    public_key = client.get_secret_value(SecretId=f"document-extractor-{ENVIRONMENT}-public-key")["SecretString"]

    token = event["authorizationToken"].replace("Bearer ", "")

    try:
        logging.info("Verifying JWT token")
        jwt.decode(token, public_key, algorithms=["RS512"])
        return generate_policy("user", "Allow", event["methodArn"])
    except Exception as e:
        exception_message = "Failed to authenticate token"
        logging.error(exception_message)
        logging.exception(e)
        return generate_policy("user", "Deny", event["methodArn"])


def generate_policy(principal_id, effect, resource):
    rest_api_arn = resource.split("/")[0]
    statement_one = {"Action": "execute-api:Invoke", "Effect": effect, "Resource": f"{rest_api_arn}/*"}
    policy_document = {"Version": "2012-10-17", "Statement": [statement_one]}
    auth_response = {"principalId": principal_id, "policyDocument": policy_document}

    return auth_response
