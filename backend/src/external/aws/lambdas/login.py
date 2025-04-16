import datetime
import json
import os

import boto3
import jwt
from argon2 import PasswordHasher

# Use AWS secrets
client = boto3.client("secretsmanager")
ENVIRONMENT = os.environ["ENVIRONMENT"]
SECRET_KEY = client.get_secret_value(SecretId=f"document-extractor-{ENVIRONMENT}-private-key")["SecretString"]
ALGORITHM = "RS512"


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    ph = PasswordHasher()
    username = body.get("username")
    password = body.get("password")

    # AWS Secret Manager User Credentials
    stored_username = client.get_secret_value(SecretId=f"document-extractor-{ENVIRONMENT}-username")["SecretString"]
    stored_password = client.get_secret_value(SecretId=f"document-extractor-{ENVIRONMENT}-password")["SecretString"]

    # AWS Secret Manager to hold one user credential
    if username != stored_username or ph.verify(stored_password, password):
        return {"statusCode": 401, "body": json.dumps({"error": "Invalid credentials"})}

    # Create JWT token
    payload = {"sub": username, "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"statusCode": 200, "body": json.dumps({"access_token": token, "token_type": "bearer"})}
