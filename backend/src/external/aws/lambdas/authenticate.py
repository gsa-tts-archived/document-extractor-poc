import json
import logging
import os

import boto3
import jwt

client = boto3.client("secretsmanager")
ENVIRONMENT = os.environ["ENVIRONMENT"]
PUBLIC_KEY = client.get_secret_value(SecretId=f"document-extractor-{ENVIRONMENT}-public-key")["SecretString"]


def lambda_handler(event, context):
    token = event["headers"].get("Authorization", "").replace("Bearer ", "")
    try:
        jwt.decode(token, PUBLIC_KEY, algorithms=["HS256"])
        return generatePolicy("user", "Allow", event["methodArn"])
    except Exception as e:
        exception_message = "Failed to authenticate token"
        logging.error(exception_message)
        logging.exception(e)
        return generatePolicy("user", "Deny", event["methodArn"])


def generatePolicy(principalId, effect, resource):
    authResponse = {}
    authResponse["principalId"] = principalId
    if effect and resource:
        policyDocument = {}
        policyDocument["Version"] = "2012-10-17"
        policyDocument["Statement"] = []
        statementOne = {}
        statementOne["Action"] = "execute-api:Invoke"
        statementOne["Effect"] = effect
        statementOne["Resource"] = resource
        policyDocument["Statement"] = [statementOne]
        authResponse["policyDocument"] = policyDocument
    return json.dumps(authResponse)
