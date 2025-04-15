import datetime
import json

import boto3
import jwt
from argon2 import PasswordHasher

# Use AWS secrets
client = boto3.client("secretsmanager")
# SECRET_KEY = os.environ.get("JWT_SECRET", "super-duper-secrets-are-just-legend")
SECRET_KEY = client.get_secret_value(SecretId="JWT_SECRET")["SecretString"]
ALGORITHM = "HS256"


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    ph = PasswordHasher()
    username = body.get("username")
    password = ph.hash(body.get("password"))

    # AWS Secret Manager User Credentials
    user_credentials_json = json.loads(client.get_secret_value(SecretId="USER_CREDENTIALS"))
    stored_username = user_credentials_json["username"]
    stored_password = user_credentials_json["password"]

    # Dummy user validation (replace with DynamoDB or other source)
    if username != stored_username or ph.verify(password, stored_password):
        return {"statusCode": 401, "body": json.dumps({"error": "Invalid credentials"})}

    # Create JWT token
    payload = {"sub": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"statusCode": 200, "body": json.dumps({"access_token": token, "token_type": "bearer"})}
